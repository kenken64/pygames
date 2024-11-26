import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)  # Sky blue

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario Game")

# Clock for managing the frame rate
clock = pygame.time.Clock()

# Mario character settings
mario = pygame.Rect(100, HEIGHT - 60, 40, 40)  # Simple rectangle as Mario
mario_color = (255, 0, 0)
mario_speed = 5
mario_jump_height = -15
gravity = 0.8
mario_velocity_y = 0
is_jumping = False

# Ground
ground = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

running = True
while running:
    screen.fill(BLUE)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Mario movement
    if keys[K_LEFT]:
        mario.x -= mario_speed
    if keys[K_RIGHT]:
        mario.x += mario_speed

    # Jumping
    if not is_jumping and keys[K_SPACE]:
        is_jumping = True
        mario_velocity_y = mario_jump_height

    # Gravity
    if is_jumping:
        mario.y += mario_velocity_y
        mario_velocity_y += gravity

        # Landing
        if mario.y >= HEIGHT - 60:
            mario.y = HEIGHT - 60
            is_jumping = False

    # Drawing
    pygame.draw.rect(screen, WHITE, ground)  # Ground
    pygame.draw.rect(screen, mario_color, mario)  # Mario

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
