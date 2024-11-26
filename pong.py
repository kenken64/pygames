import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Paddle properties
paddle_width, paddle_height = 10, 60
player_paddle = pygame.Rect(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(width - 40, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball properties
ball_size = 15
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# Paddle speed
paddle_speed = 5

# Game clock
clock = pygame.time.Clock()

# Score
player_score = 0
opponent_score = 0

font = pygame.font.Font(None, 36)

def draw_paddle(paddle):
    pygame.draw.rect(screen, white, paddle)

def draw_ball(ball):
    pygame.draw.ellipse(screen, white, ball)

def draw_scores():
    player_text = font.render(str(player_score), True, white)
    opponent_text = font.render(str(opponent_score), True, white)
    screen.blit(player_text, (width // 4, 10))
    screen.blit(opponent_text, (3 * width // 4 - 20, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle.bottom < height:
        player_paddle.y += paddle_speed

    # Opponent paddle AI (simple)
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += paddle_speed
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= paddle_speed

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds (score)
    if ball.left <= 0:
        opponent_score += 1
        ball.center = (width // 2, height // 2)
        ball_speed_x *= -1
    elif ball.right >= width:
        player_score += 1
        ball.center = (width // 2, height // 2)
        ball_speed_x *= -1

    # Clear screen
    screen.fill(black)

    # Draw paddles and ball
    draw_paddle(player_paddle)
    draw_paddle(opponent_paddle)
    draw_ball(ball)

    # Draw scores
    draw_scores()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)