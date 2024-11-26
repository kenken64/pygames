import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 10, 4
CIRCLE_RADIUS = 20
MARGIN = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]  # Red, Green, Blue, Yellow, Orange, Purple

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# Fonts
font = pygame.font.Font(None, 36)

# Generate a random code
def generate_code():
    return [random.choice(COLORS) for _ in range(COLS)]

# Draw circles for the board
def draw_board(guesses, feedback, current_row):
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 100, WIDTH, 100))  # Feedback area

    # Draw guesses and feedback
    for row in range(ROWS):
        y = row * (CIRCLE_RADIUS * 2 + MARGIN) + MARGIN
        for col in range(COLS):
            x = col * (CIRCLE_RADIUS * 2 + MARGIN) + MARGIN
            color = guesses[row][col] if guesses[row][col] else GRAY
            pygame.draw.circle(screen, color, (x + CIRCLE_RADIUS, y + CIRCLE_RADIUS), CIRCLE_RADIUS)

        # Draw feedback
        feedback_x = WIDTH - (CIRCLE_RADIUS * 2 + MARGIN) * COLS
        for i in range(len(feedback[row])):
            fx = feedback_x + (i * (CIRCLE_RADIUS + 5))
            fy = y
            feedback_color = BLACK if feedback[row][i] == "B" else WHITE
            pygame.draw.circle(screen, feedback_color, (fx + CIRCLE_RADIUS, fy + CIRCLE_RADIUS), CIRCLE_RADIUS // 2)

    # Highlight current row
    if current_row < ROWS:
        y = current_row * (CIRCLE_RADIUS * 2 + MARGIN) + MARGIN
        pygame.draw.rect(screen, (200, 200, 200), (0, y, WIDTH, CIRCLE_RADIUS * 2 + MARGIN), 2)

# Get feedback (Black = correct position, White = correct color)
def get_feedback(code, guess):
    code_copy = code[:]
    guess_copy = guess[:]
    feedback = []

    # Black feedback for correct positions
    for i in range(len(guess)):
        if guess[i] == code[i]:
            feedback.append("B")
            code_copy[i] = None
            guess_copy[i] = None

    # White feedback for correct colors
    for g in guess_copy:
        if g and g in code_copy:
            feedback.append("W")
            code_copy[code_copy.index(g)] = None

    return feedback

# Main function
def main():
    code = generate_code()
    guesses = [[None] * COLS for _ in range(ROWS)]
    feedback = [[] for _ in range(ROWS)]
    current_row = 0
    running = True

    selected_color = 0

    while running:
        draw_board(guesses, feedback, current_row)

        # Draw color selection
        for i, color in enumerate(COLORS):
            x = i * (CIRCLE_RADIUS * 2 + MARGIN) + MARGIN
            y = HEIGHT - 70
            pygame.draw.circle(screen, color, (x + CIRCLE_RADIUS, y + CIRCLE_RADIUS), CIRCLE_RADIUS)
            if i == selected_color:
                pygame.draw.circle(screen, BLACK, (x + CIRCLE_RADIUS, y + CIRCLE_RADIUS), CIRCLE_RADIUS + 2, 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_color = (selected_color - 1) % len(COLORS)
                elif event.key == pygame.K_RIGHT:
                    selected_color = (selected_color + 1) % len(COLORS)
                elif event.key == pygame.K_RETURN:
                    if None not in guesses[current_row]:
                        feedback[current_row] = get_feedback(code, guesses[current_row])
                        if feedback[current_row] == ["B"] * COLS:
                            print("You won!")
                            running = False
                        else:
                            current_row += 1
                            if current_row == ROWS:
                                print("You lost! The code was:", code)
                                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < HEIGHT - 100:
                    col = x // (CIRCLE_RADIUS * 2 + MARGIN)
                    if col < COLS:
                        guesses[current_row][col] = COLORS[selected_color]

    pygame.quit()

if __name__ == "__main__":
    main()
