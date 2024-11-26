import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Game variables
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_width = 30
bird_height = 30
bird_velocity = 0
gravity = 0.5
flap_strength = -7  # Reduced jump height

pipe_width = 70
pipe_gap = 150
pipe_velocity = 3

# Initialize pipes
pipe_list = []
pipe_frequency = 1500  # in milliseconds
last_pipe = pygame.time.get_ticks()

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop flag
running = True
game_over = False


def draw_bird(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, bird_width, bird_height))


def draw_pipe(x, y, gap):
    # Top pipe
    pygame.draw.rect(screen, GREEN, (x, 0, pipe_width, y))
    # Bottom pipe
    pygame.draw.rect(screen, GREEN, (x, y + gap, pipe_width, SCREEN_HEIGHT - (y + gap)))


def check_collision(bird_rect, pipes):
    for pipe in pipes:
        top_pipe = pygame.Rect(pipe['x'], 0, pipe_width, pipe['height'])
        bottom_pipe = pygame.Rect(pipe['x'], pipe['height'] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe['height'] - pipe_gap)
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    # Check if the bird hits the ground or flies off-screen
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False


def display_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))


# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bird_velocity = flap_strength

    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe generation
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
            pipe_list.append({'x': SCREEN_WIDTH, 'height': pipe_height})
            last_pipe = current_time

        # Move pipes
        for pipe in pipe_list:
            pipe['x'] -= pipe_velocity

        # Remove off-screen pipes
        pipe_list = [pipe for pipe in pipe_list if pipe['x'] + pipe_width > 0]

        # Check for collisions
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        if check_collision(bird_rect, pipe_list):
            game_over = True

        # Update score
        for pipe in pipe_list:
            if pipe['x'] + pipe_width < bird_x and not pipe.get('scored', False):
                score += 1
                pipe['scored'] = True

        # Draw bird and pipes
        draw_bird(bird_x, bird_y)
        for pipe in pipe_list:
            draw_pipe(pipe['x'], pipe['height'], pipe_gap)

        # Display score
        display_score(score)

    else:
        # Game over screen
        text = font.render("Game Over", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
