import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Number of cells in grid (20x20)
CELL_SIZE = 20  # Size of each cell in pixels
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 10  # Frames per second (snake speed)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score and game over
font = pygame.font.Font(None, 36)

class SnakeGame:
    def __init__(self):
        self.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]  # Starting position (array of positions)
        self.direction = RIGHT  # Initial direction
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def move(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_SIZE, (head_y + dy) % GRID_SIZE)  # Wrap around walls

        # Check self-collision
        if new_head in self.snake:
            self.game_over = True
            return

        # Insert new head
        self.snake.insert(0, new_head)

        # Check if ate food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            # Remove tail
            self.snake.pop()

    def draw(self):
        screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, (self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            if not self.game_over:
                self.move()
            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()