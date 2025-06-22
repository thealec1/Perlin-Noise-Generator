import pygame as pg
import random
import math
import time

display = pg.display.set_mode((500, 500))
WIDTH, HEIGHT = display.get_width(), display.get_height()
pg.display.set_caption("Perlin Noise Generator")

GRID_SIZE = 512
SQUARE_SIZE = 64
# random.seed(7)

def smoothstep (edge0, edge1, x):
   x = clamp((x - edge0) / (edge1 - edge0))
   return x * x * (3 - 2 * x)

def clamp(x, lowerlimit=0, upperlimit=1):
  if (x < lowerlimit): return lowerlimit
  if (x > upperlimit): return upperlimit
  return x

def lerp(p, n1, n2):
    return n1 + smoothstep(0, 1, p) * (n2-n1)

def get_dot_product(v1x, v1y, v2x, v2y, angle):
    va = v1x-v2x
    vb = v1y-v2y
    return (va * math.cos(math.radians(angle))) + (vb * math.sin(math.radians(angle)))

def generate_vector_field(size, cell_size):
    point_count = (size//cell_size)+1
    vector_field = []
    for row in range(point_count):
        new_row = []
        for col in range(point_count):
            new_row.append([col, row, random.randint(0, 360)])
        if len(new_row) != 0:
            vector_field.append(new_row)
    return vector_field

def set_noise_values(size, tile_size, noise_map, vector_field):
    ts = tile_size
    for row in range(size):
        for col in range(size):
            x, y = (1/ts)*col, (1/ts)*row
            
            xl = col//SQUARE_SIZE
            xr = xl+1
            yt = row//SQUARE_SIZE
            yb = yt+1
            
            top_left = get_dot_product(xl, yt, x, y, vector_field[yt][xl][2])
            top_right = get_dot_product(xr, yt, x, y, vector_field[yt][xr][2])
            btm_left = get_dot_product(xl, yb, x, y, vector_field[yb][xl][2])
            btm_right = get_dot_product(xr, yb, x, y, vector_field[yb][xr][2])

            horiz_vector_mag = x-xl
            vert_vector_mag = y-yt

            top_lerp = lerp(horiz_vector_mag, top_left, top_right)
            btm_lerp = lerp(horiz_vector_mag, btm_left, btm_right)
            noise_value = lerp(vert_vector_mag, top_lerp, btm_lerp)
            
            cm = (1/2)*(noise_value) + (1/2)
            colour = (255*cm, 255*cm, 255*cm)

            # if 0 <= cm < 0.25:
            #     colour = (200*cm, 200*cm, 200*cm)
            # elif 0.25 <= cm < 0.5:
            #     colour = (255*cm, 123*cm, 0*cm)
            # elif 0.5 <= cm < 0.75:
            #     colour = (50*cm, 50*cm, 50*cm)
            # elif 0.75 <= cm <= 1:
            #     colour = (255*cm, 123*cm, 0*cm)
            
            noise_map[col, row] = colour


def add_maps(map_a, map_b, ):
    pass

vector_field = generate_vector_field(GRID_SIZE, SQUARE_SIZE)
point_count = (GRID_SIZE//SQUARE_SIZE)+1

def rotate():
    for row in range(point_count):
        for col in range(point_count):
            vector_field[row][col][2] = (vector_field[row][col][2] + 1) % 361

def generate_noise_map():
    global noise_surface
    global n_width, n_height
    noise_map = pg.PixelArray(pg.Surface((GRID_SIZE, GRID_SIZE)) )
    set_noise_values(GRID_SIZE, SQUARE_SIZE, noise_map, vector_field)

    noise_surface = noise_map.surface
    noise_surface = pg.transform.scale(noise_surface, (400, 400))
    noise_map.close()
    n_width, n_height = noise_surface.get_width(), noise_surface.get_height()

generate_noise_map()

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # then = time.time()
                generate_noise_map()
                # print(1000*(time.time() - then))

    rotate()
    generate_noise_map()

    clock.tick(60)

    display.fill((0, 0, 0))
    display.blit(noise_surface, (WIDTH//2-(n_width//2), HEIGHT//2-(n_height)//2))
    pg.display.update()

pg.quit()
