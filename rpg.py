import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PLAYER_SPEED = 5

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple RPG Game")
clock = pygame.time.Clock()

# Player settings
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
player_color = (0, 0, 255)

# Treasure settings
num_treasures = 5
treasures = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 20, 20) for _ in range(num_treasures)]
treasure_color = (255, 215, 0)

# Score
score = 0
font = pygame.font.Font(None, 36)

running = True
while running:
    screen.fill(WHITE)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player.y += PLAYER_SPEED

    # Boundaries check
    if player.x < 0: player.x = 0
    if player.x > WIDTH - player.width: player.x = WIDTH - player.width
    if player.y < 0: player.y = 0
    if player.y > HEIGHT - player.height: player.y = HEIGHT - player.height

    # Collision detection with treasures
    for treasure in treasures[:]:
        if player.colliderect(treasure):
            treasures.remove(treasure)
            score += 10

    # Drawing player and treasures
    pygame.draw.rect(screen, player_color, player)
    for treasure in treasures:
        pygame.draw.rect(screen, treasure_color, treasure)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
pygame.quit()
