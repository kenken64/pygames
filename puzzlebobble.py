import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUBBLE_RADIUS = 20
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Bobble")

# Clock
clock = pygame.time.Clock()

# Bubble class
class Bubble:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self.fixed = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BUBBLE_RADIUS)

    def move(self):
        if not self.fixed:
            self.x += self.velocity_x
            self.y += self.velocity_y

            # Bounce off the walls
            if self.x - BUBBLE_RADIUS < 0 or self.x + BUBBLE_RADIUS > SCREEN_WIDTH:
                self.velocity_x *= -1

            # Stop when it reaches the top
            if self.y - BUBBLE_RADIUS <= 0:
                self.fixed = True

# Helper functions
def check_collision(b1, b2):
    distance = math.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)
    return distance <= BUBBLE_RADIUS * 2

def find_matches(bubbles, current_bubble):
    """Find all connected bubbles of the same color."""
    stack = [current_bubble]
    visited = set()
    matches = []

    while stack:
        bubble = stack.pop()
        if bubble not in visited:
            visited.add(bubble)
            matches.append(bubble)
            # Add neighbors of the same color
            for other_bubble in bubbles:
                if other_bubble.color == bubble.color and check_collision(bubble, other_bubble):
                    stack.append(other_bubble)

    return matches

# Game variables
bubbles = []
current_bubble = Bubble(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, random.choice(COLORS))
next_bubble = Bubble(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, random.choice(COLORS))

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not current_bubble.fixed:
                # Shoot bubble
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - current_bubble.y, mouse_x - current_bubble.x)
                current_bubble.velocity_x = math.cos(angle) * 10
                current_bubble.velocity_y = math.sin(angle) * 10

    # Move the current bubble
    if not current_bubble.fixed:
        current_bubble.move()

    # Check for collisions with other bubbles
    for bubble in bubbles:
        if check_collision(current_bubble, bubble) and not current_bubble.fixed:
            current_bubble.fixed = True
            current_bubble.velocity_x = 0
            current_bubble.velocity_y = 0
            bubbles.append(current_bubble)

            # Check for matches
            matches = find_matches(bubbles, current_bubble)
            if len(matches) >= 3:
                for match in matches:
                    bubbles.remove(match)

            # Generate a new bubble
            current_bubble = next_bubble
            next_bubble = Bubble(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, random.choice(COLORS))
            break

    # Draw bubbles
    for bubble in bubbles:
        bubble.draw(screen)

    # Draw the current bubble
    current_bubble.draw(screen)

    # Draw the next bubble
    pygame.draw.circle(screen, next_bubble.color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80), BUBBLE_RADIUS)

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
