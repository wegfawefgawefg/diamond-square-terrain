import math
import random
from pprint import pprint

import pygame

FPS = 60
WIDTH, HEIGHT = 800, 800
SIZE = int(math.pow(8, 2) + 1)
ground_WIDTH, ground_HEIGHT = (SIZE, SIZE)
MAX = SIZE - 1
ROUGHNESS = 0.7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Terrain")
clock = pygame.time.Clock()

print(f"ground dims: ({ground_WIDTH}, {ground_HEIGHT})")
ground = []
for _ in range(ground_HEIGHT):
    row = [random.random() for _ in range(ground_WIDTH)]
    ground.append(row)

ground[0][0] = MAX / 2
ground[-1][0] = MAX / 2
ground[0][-1] = MAX / 2
ground[-1][-1] = MAX / 2


def redraw():
    screen.fill((0, 0, 0))
    low = min([min(row) for row in ground])
    high = max([max(row) for row in ground])
    square_dims = (WIDTH // ground_WIDTH, HEIGHT // ground_HEIGHT)
    for y in range(ground_HEIGHT):
        for x in range(ground_WIDTH):
            # draw rect
            base_x = x * WIDTH // ground_WIDTH
            base_y = y * HEIGHT // ground_HEIGHT
            val = ground[y][x]
            val = fground(val, low, high, 0, 255)
            #print(val)
            pygame.draw.rect(
                screen,
                (val, val, val),
                (base_x, base_y,
                    square_dims[0], square_dims[1]),
            )
    pygame.display.flip()

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
    redraw()

def square(ground, x, y, size, offset):
    avg = (
        ground[y-size][x-size] +
        ground[y+size][x-size] +
        ground[y-size][x+size] +
        ground[y+size][x+size]
    ) / 4
    ground[y][x] = avg + offset
    redraw()

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

def main():
    iter_size = MAX

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
        div(ground, iter_size)
        iter_size = iter_size // 2


        # draw
        

    pygame.quit()

main()

    