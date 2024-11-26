import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
bg_color = (0, 0, 0)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)

# Snake dimensions
block_size = 20

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, snake_color, (segment[0], segment[1], block_size, block_size))

def draw_food(food_position):
    pygame.draw.rect(screen, food_color, (food_position[0], food_position[1], block_size, block_size))

def create_food(snake):
    while True:
        x = random.randrange(0, width - block_size, block_size)
        y = random.randrange(0, height - block_size, block_size)
        food_position = (x, y)
        if food_position not in snake:
            return food_position

def check_collision(snake):
    head = snake[0]
    if (head[0] < 0 or head[0] >= width or 
        head[1] < 0 or head[1] >= height or
        head in snake[1:]):
        return True
    return False

def game_over():
    screen.fill(bg_color)
    font = pygame.font.Font(None, 50)
    text = font.render('Game Over!', True, food_color)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

def main():
    global direction
    direction = RIGHT

    snake = [(width // 2, height // 2)]
    food_position = create_food(snake)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        head = snake[0]
        new_head = (head[0] + direction[0] * block_size, head[1] + direction[1] * block_size)
        snake.insert(0, new_head)

        if new_head == food_position:
            food_position = create_food(snake)
        else:
            snake.pop()

        screen.fill(bg_color)
        draw_snake(snake)
        draw_food(food_position)
        pygame.display.update()

        if check_collision(snake):
            game_over()
            running = False

        clock.tick(5)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()