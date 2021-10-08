import math
import random
from pprint import pprint
import operator
from functools import reduce
import time

import pygame
from pygame import mouse

from vec3 import Vec3, Mat4


FPS = 60
WIDTH, HEIGHT = 1400, 1000
SIZE = int(math.pow(2, 6) + 1)
ground_WIDTH, ground_HEIGHT = (SIZE, SIZE)
MAX = SIZE - 1
ROUGHNESS = 0.7
random.seed(10)

def fground(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def hist_eq(nums, new_low, new_high):
    height = len(nums)
    width = len(nums[0])
    low = min([min(row) for row in nums])
    high = max([max(row) for row in nums])
    for y in range(height):
        for x in range(width):
            val = nums[y][x]
            histogram_equalized = fground(val, low, high, new_low, new_high)
            #nums[y][x] = histogram_equalized
            nums[y][x] = int(histogram_equalized)
    return nums

def diamond(ground, x, y, size, offset):
    avg = (
        ground[y-size][x] +
        ground[y+size][x] +
        ground[y][x+size] +
        ground[y][x-size]
    ) / 4
    ground[y][x] = avg + offset

def square(ground, x, y, size, offset):
    avg = (
        ground[y-size][x-size] +
        ground[y+size][x-size] +
        ground[y-size][x+size] +
        ground[y+size][x+size]
    ) / 4
    ground[y][x] = avg + offset

def div(ground, size):
    half = size // 2
    x = half
    y = half
    scale = ROUGHNESS * size
    if half < 1:
        return
    
    for y in range(half, MAX, size):
        for x in range(half, MAX, size):
            square(ground, x, y, half, random.random() * scale * 2 - scale)
    for y in range(0, MAX, half):
        for x in range((y + half)%size, MAX, size):
            diamond(ground, x, y, half, random.random() * scale * 2 - scale)
    div(ground, size // 2)

def main():
    pygame.init()
    main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # transparent surf from screen
    screen = pygame.Surface(main_screen.get_size(), pygame.SRCALPHA)

    pygame.display.set_caption("DSA Terrain")
    clock = pygame.time.Clock()


    print(f"ground dims: ({ground_WIDTH}, {ground_HEIGHT})")
    ground = []
    for _ in range(ground_HEIGHT):
        row = [random.random() for _ in range(ground_WIDTH)]
        ground.append(row)
    

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # update
        random.seed(10)
        ground = []
        for _ in range(ground_HEIGHT):
            row = [random.random() for _ in range(ground_WIDTH)]
            ground.append(row)

        # ground[0][0] =  MAX / 2
        mp = pygame.mouse.get_pos()
        mx, my = int(mp[0]), int(mp[1])
        x_mod = int(fground(mx, 0, WIDTH, 0, MAX))
        y_mod = int(fground(my, 0, HEIGHT, 0, MAX))
        ground[0][0]   = y_mod
        ground[-1][0]  = x_mod
        ground[0][-1]  = y_mod
        ground[-1][-1] = y_mod

        div(ground, MAX)
        ground = hist_eq(ground, 0, 20)

        # draw
        screen.fill((0, 0, 0, 0))

        angles = (38.1, 19.5)

        x_mod = mouse.get_pos()[0]
        y_mod = mouse.get_pos()[1]

        center = Vec3(WIDTH // 2, HEIGHT // 4, 0)
        start = Vec3(0, 0, 0)
        up = Vec3(0, -1, 0)
        right = Vec3(1, 0, 0)
        down = Vec3(0, 0, -1)
        #print(f"up: {up}, right: {right}, down: {down}")

        comb = reduce(operator.mul, 
            (
                Mat4.rot(*angles, 0),
                #Mat4.rot(x_mod/10, y_mod/10, 0),
                #Mat4.translate(center.x, center.y, center.z),
                #Mat4.translate(x_mod, y_mod, 0),
                Mat4.scale(*([13] * 3)),
                Mat4(),
            ), 
            Mat4())


        start = comb * start + center
        up = comb * up
        right = comb * right
        down = comb * down

        #print(f"angle: {x_mod/10}, {y_mod/10}")

        #scale = Mat4.scale(1, 1, 1)
        #trans = Mat4.translate(x_mod, y_mod, 0)   
        #comb = trans# * rot * scale
        #comb =  rot * trans * scale


        # draw up down right
        pygame.draw.line(screen, (255, 0, 0), (start.x, start.y), (start.x + up.x, start.y + up.y), 1)
        pygame.draw.line(screen, (0, 255, 0), (start.x, start.y), (start.x + right.x, start.y + right.y), 1)
        pygame.draw.line(screen, (255, 255, 255), (start.x, start.y), (start.x + down.x, start.y + down.y), 1)

        most_right = start + right * ground_WIDTH
        most_down = start + down * ground_HEIGHT

        pygame.draw.circle(screen, (255, 255, 255), (int(start.x), int(start.y)), 5)
        pygame.draw.line(screen, (255, 255, 255), (int(start.x), int(start.y)), (int(most_right.x), int(most_right.y)))
        pygame.draw.line(screen, (255, 255, 255), (int(start.x), int(start.y)), (int(most_down.x), int(most_down.y)))

        for y in range(ground_HEIGHT-1):
            for x in range(ground_WIDTH-1):
                height = ground[y][x]
                right_height = ground[y][x+1]
                down_height = ground[y+1][x]

                base = start + right * x + down * y
                p = base + up * height
                p_right = base + right + up * right_height
                p_down = base + down + up * down_height

                pygame.draw.line(screen, (255, 255, 255), (p.x, p.y), (p_right.x, p_right.y))
                pygame.draw.line(screen, (255, 255, 255), (p.x, p.y), (p_down.x, p_down.y))
        # draw right side
        for y in range(ground_HEIGHT-1):
            x = ground_WIDTH-1
            height = ground[y][x]
            down_height = ground[y+1][x]

            base = start + right * x + down * y
            p = base + up * height
            p_down = base + down + up * down_height

            pygame.draw.line(screen, (255, 255, 255), (p.x, p.y), (p_down.x, p_down.y))
        # draw down side
        for x in range(ground_WIDTH-1):
            y = ground_HEIGHT-1
            height = ground[y][x]
            right_height = ground[y][x+1]

            base = start + right * x + down * y
            p = base + up * height
            p_right = base + right + up * right_height

            pygame.draw.line(screen, (255, 255, 255), (p.x, p.y), (p_right.x, p_right.y))


                # draw rect from base to p
                #pygame.draw.line(screen, (255, 255, 255, 200), (base.x, base.y), (p.x, p.y), 2)
                #pygame.draw.circle(screen, (255, 255, 255, 255), (int(p.x), int(p.y)), 1)
                #pygame.draw.circle(screen, (255, 255, 255, 255), (int(base.x), int(base.y)), 1)



        #square_dims = (WIDTH // ground_WIDTH, HEIGHT // ground_HEIGHT)
        #for y in range(ground_HEIGHT):
        #    for x in range(ground_WIDTH):
        #        # draw rect
        #        base_x = x * WIDTH // ground_WIDTH
        #        base_y = y * HEIGHT // ground_HEIGHT
        #        val = ground[y][x]
        #        pygame.draw.rect(
        #            screen,
        #            (val, val, val),
        #            (base_x, base_y,
        #                square_dims[0], square_dims[1]),
        #        )

        main_screen.fill((0, 0, 0))
        main_screen.blit(screen, (0, 0))
        pygame.display.flip()
    pygame.quit()

main()

    