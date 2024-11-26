import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 255, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],        # O
    [[0, 1, 0], [1, 1, 1]]   # T
]

# Helper functions
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    for x in range(COLS):
        pygame.draw.line(surface, WHITE, (x * GRID_SIZE, 0), (x * GRID_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, WHITE, (0, y * GRID_SIZE), (WIDTH, y * GRID_SIZE))

def draw_window(surface, grid):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    pygame.display.update()

def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= COLS or y + off_y >= ROWS:
                    return True
                if (x + off_x, y + off_y) in locked_positions:
                    return True
    return False

def clear_lines(grid, locked_positions):
    cleared = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(COLS):
                del locked_positions[(x, y)]
            for new_y in range(y, 0, -1):
                for x in range(COLS):
                    if (x, new_y - 1) in locked_positions:
                        locked_positions[(x, new_y)] = locked_positions.pop((x, new_y - 1))
    return cleared

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotated_shape(self):
        return [list(row) for row in zip(*self.shape[::-1])]

# Game variables
locked_positions = {}
grid = create_grid(locked_positions)
current_piece = Tetromino(COLS // 2 - 2, 0, random.choice(SHAPES))
next_piece = Tetromino(COLS // 2 - 2, 0, random.choice(SHAPES))
clock = pygame.time.Clock()
fall_time = 0

# Main loop
def main():
    global grid, locked_positions, current_piece, next_piece, fall_time

    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # Piece falling logic
        if fall_time / 1000 > 0.5:
            fall_time = 0
            current_piece.y += 1
            if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                current_piece.y -= 1
                for y, row in enumerate(current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + x, current_piece.y + y)] = current_piece.color
                current_piece = next_piece
                next_piece = Tetromino(COLS // 2 - 2, 0, random.choice(SHAPES))
                if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.shape = current_piece.rotated_shape()
                    if check_collision(current_piece.shape, (current_piece.x, current_piece.y)):
                        current_piece.shape = current_piece.rotated_shape()[-1::-1]

        shape_pos = [(current_piece.x + x, current_piece.y + y) for y, row in enumerate(current_piece.shape) for x, cell in enumerate(row) if cell]
        for x, y in shape_pos:
            if 0 <= y < ROWS and 0 <= x < COLS:
                grid[y][x] = current_piece.color

        clear_lines(grid, locked_positions)
        draw_window(win, grid)

    pygame.quit()

# Run game
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
main()
