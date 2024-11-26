import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

# Initialize clock
clock = pygame.time.Clock()

# Initialize grid
def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

grid = create_grid()

# Randomize grid
def randomize_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = random.choice([0, 1])

# Draw grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# Draw cells
def draw_cells(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

# Count live neighbors
def count_neighbors(grid, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            count += grid[ny][nx]
    return count

# Update grid
def update_grid(grid):
    new_grid = create_grid()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            live_neighbors = count_neighbors(grid, x, y)
            if grid[y][x] == 1:  # Alive
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:  # Dead
                if live_neighbors == 3:
                    new_grid[y][x] = 1
    return new_grid

# Main loop
running = True
paused = True

while running:
    screen.fill(BLACK)
    draw_grid()
    draw_cells(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                grid = create_grid()
                randomize_grid(grid)
            if event.key == pygame.K_c:
                grid = create_grid()
        if pygame.mouse.get_pressed()[0]:  # Left click to toggle cells
            pos = pygame.mouse.get_pos()
            x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
            grid[y][x] = 1 - grid[y][x]

    if not paused:
        grid = update_grid(grid)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
