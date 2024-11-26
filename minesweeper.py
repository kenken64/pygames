import pygame
import sys
import random

# Constants
GRID_SIZE = 10  # Number of rows and columns
CELL_SIZE = 40  # Size of each cell in pixels
NUM_MINES = 15  # Total number of mines
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Calculate window dimensions
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Fonts
FONT = pygame.font.Font(None, CELL_SIZE // 2)

# Helper functions
def create_grid(grid_size, num_mines):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    mines = random.sample(range(grid_size * grid_size), num_mines)
    for mine in mines:
        row, col = divmod(mine, grid_size)
        grid[row][col] = -1
        for r in range(max(0, row - 1), min(grid_size, row + 2)):
            for c in range(max(0, col - 1), min(grid_size, col + 2)):
                if grid[r][c] != -1:
                    grid[r][c] += 1
    return grid

def draw_grid(screen, grid, revealed, flagged):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE, row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if (row, col) in flagged:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            elif revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                elif grid[row][col] > 0:
                    text = FONT.render(str(grid[row][col]), True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))

def reveal_cell(grid, revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True
    if grid[row][col] == 0:
        for r in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
            for c in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                if not revealed[r][c]:
                    reveal_cell(grid, revealed, r, c)

# Game state
grid = create_grid(GRID_SIZE, NUM_MINES)
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flagged = set()
game_over = False

# Game loop
clock = pygame.time.Clock()

while True:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if event.button == 1:  # Left click
                if grid[row][col] == -1:
                    game_over = True
                else:
                    reveal_cell(grid, revealed, row, col)
            elif event.button == 3:  # Right click
                if (row, col) in flagged:
                    flagged.remove((row, col))
                else:
                    flagged.add((row, col))

    draw_grid(screen, grid, revealed, flagged)

    if game_over:
        text = FONT.render("Game Over!", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(30)
