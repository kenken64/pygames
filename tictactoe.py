import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 300, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Colors
bg_color = (255, 255, 255)
line_color = (0, 0, 0)
mark_color = (255, 0, 0)

# Board dimensions
board_size = 3
grid_width = width // board_size

# Game variables
board = [[None] * board_size for _ in range(board_size)]
current_player = 'X'

def draw_board():
    screen.fill(bg_color)
    pygame.draw.line(screen, line_color, (0, grid_width), (width, grid_width))
    pygame.draw.line(screen, line_color, (grid_width, 0), (grid_width, height))
    pygame.draw.line(screen, line_color, (0, 2 * grid_width), (width, 2 * grid_width))
    pygame.draw.line(screen, line_color, (2 * grid_width, 0), (2 * grid_width, height))

def draw_marks():
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 'X':
                pygame.draw.line(screen, mark_color, 
                                 (col * grid_width + 15, row * grid_width + 15), 
                                 ((col + 1) * grid_width - 15, (row + 1) * grid_width - 15), 
                                 20)
                pygame.draw.line(screen, mark_color, 
                                 ((col + 1) * grid_width - 15, row * grid_width + 15), 
                                 (col * grid_width + 15, (row + 1) * grid_width - 15), 
                                 20)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, mark_color, 
                                   (int((col + 0.5) * grid_width), int((row + 0.5) * grid_width)), 
                                   grid_width // 3, 20)

def check_winner():
    # Check rows
    for row in range(board_size):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    
    # Check columns
    for col in range(board_size):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None

def check_draw():
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] is None:
                return False
    return True

def reset_game():
    global board, current_player
    board = [[None] * board_size for _ in range(board_size)]
    current_player = 'X'

draw_board()
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not check_winner() and not check_draw():
            x, y = event.pos
            row = y // grid_width
            col = x // grid_width
            if board[row][col] is None:
                board[row][col] = current_player
                current_player = 'O' if current_player == 'X' else 'X'
    
    draw_board()
    draw_marks()
    pygame.display.update()

    winner = check_winner()
    if winner:
        screen.fill(bg_color)
        font = pygame.font.Font(None, 100)
        text = font.render(f'{winner} wins!', True, mark_color)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        reset_game()

    if check_draw():
        screen.fill(bg_color)
        font = pygame.font.Font(None, 100)
        text = font.render('Draw!', True, mark_color)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        reset_game()

pygame.quit()