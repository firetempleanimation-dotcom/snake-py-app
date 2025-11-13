import pygame
import random
import sys

# Constants
GRID_SIZE = 20
CELL_SIZE = 30  # Increased by 50% for larger game field
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE  # 600
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE  # 600
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (160, 160, 160)
YELLOW = (255, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.cell_size = CELL_SIZE
        self.fps = FPS
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.center_x = self.screen_width // 2
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 28)
        self.instr_font = pygame.font.Font(None, 20)
        # Menu / Game Over buttons
        btn_w, btn_h = 120, 50
        self.start_rect = pygame.Rect(self.center_x - btn_w // 2, 250, btn_w, btn_h)
        self.restart_rect = pygame.Rect(self.center_x - btn_w // 2, 310, btn_w, btn_h)
        # In-game buttons
        gb_w, gb_h = 110, 35
        self.pause_rect = pygame.Rect(self.screen_width - 130, 10, gb_w, gb_h)
        self.game_restart_rect = pygame.Rect(self.screen_width - 130, 55, gb_w, gb_h)
        self.state = 'menu'  # 'menu', 'playing', 'paused', 'game_over'
        self.high_score = 0
        self.load_high_score()
        self.reset_game()
        self.instr_surf = self.instr_font.render("Arrow keys: move | P: pause/resume | ESC: quit", True, WHITE)

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def generate_food(self):
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food

    def reset_game(self):
        center = self.grid_size // 2
        self.snake = [(center, center - 2), (center, center - 1), (center, center)]
        self.direction = RIGHT
        self.food = self.generate_food()
        self.score = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif self.state in ['playing', 'paused']:
                    if event.key == pygame.K_p:
                        self.state = 'paused' if self.state == 'playing' else 'playing'
                    elif self.state == 'playing':
                        if event.key == pygame.K_UP and self.direction != DOWN:
                            self.direction = UP
                        elif event.key == pygame.K_DOWN and self.direction != UP:
                            self.direction = DOWN
                        elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                            self.direction = LEFT
                        elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                            self.direction = RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.state == 'menu' and self.start_rect.collidepoint(pos):
                    self.reset_game()
                    self.state = 'playing'
                elif self.state == 'game_over' and self.restart_rect.collidepoint(pos):
                    self.reset_game()
                    self.state = 'playing'
                elif self.state in ['playing', 'paused']:
                    if self.pause_rect.collidepoint(pos):
                        self.state = 'paused' if self.state == 'playing' else 'playing'
                    elif self.game_restart_rect.collidepoint(pos):
                        self.reset_game()
                        self.state = 'playing'

    def move(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.grid_size, (head_y + dy) % self.grid_size)
        will_grow = new_head == self.food
        tail = self.snake[-1]
        if new_head in self.snake and not (new_head == tail and not will_grow):
            self.state = 'game_over'
            self.update_high_score()
            return
        self.snake.insert(0, new_head)
        if will_grow:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw_button(self, rect, text, hover_color=LIGHT_GRAY, base_color=GRAY, text_color=BLACK, border_color=WHITE, border_width=2):
        mouse_pos = pygame.mouse.get_pos()
        color = hover_color if rect.collidepoint(mouse_pos) else base_color
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, border_color, rect, border_width)
        btn_surf = self.button_font.render(text, True, text_color)
        btn_rect = btn_surf.get_rect(center=rect.center)
        self.screen.blit(btn_surf, btn_rect)

    def draw(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        if self.state == 'menu':
            # Title
            title_surf = self.title_font.render("Snake Game", True, WHITE)
            title_rect = title_surf.get_rect(center=(self.center_x, 150))
            self.screen.blit(title_surf, title_rect)
            # High score
            high_surf = self.button_font.render(f"High Score: {self.high_score}", True, WHITE)
            high_rect = high_surf.get_rect(center=(self.center_x, 200))
            self.screen.blit(high_surf, high_rect)
            # Start button
            self.draw_button(self.start_rect, "Start Game")
            # Instructions
            instr_rect = self.instr_surf.get_rect(center=(self.center_x, 380))
            self.screen.blit(self.instr_surf, instr_rect)
        elif self.state == 'game_over':
            # Game Over
            go_surf = self.title_font.render("Game Over!", True, WHITE)
            go_rect = go_surf.get_rect(center=(self.center_x, 120))
            self.screen.blit(go_surf, go_rect)
            # Your score and high score
            score_surf = self.button_font.render(f"Your Score: {self.score} | High Score: {self.high_score}", True, WHITE)
            score_rect = score_surf.get_rect(center=(self.center_x, 210))
            self.screen.blit(score_surf, score_rect)
            # Restart button
            self.draw_button(self.restart_rect, "Restart")
        else:  # playing or paused
            # Snake
            for seg in self.snake:
                rect = (seg[0] * self.cell_size, seg[1] * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GREEN, rect)
            # Food
            frect = (self.food[0] * self.cell_size, self.food[1] * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, RED, frect)
            # Score
            sc_surf = self.font.render(f"Score: {self.score} | High: {self.high_score}", True, WHITE)
            self.screen.blit(sc_surf, (10, 10))
            # Pause / Resume button
            p_text = "Resume" if self.state == 'paused' else "Pause"
            self.draw_button(self.pause_rect, p_text)
            # Restart button
            self.draw_button(self.game_restart_rect, "Restart")
            if self.state == 'paused':
                # Paused overlay
                pause_overlay = self.title_font.render("PAUSED", True, YELLOW)
                po_rect = pause_overlay.get_rect(center=(self.center_x, self.screen_height // 2 - 30))
                self.screen.blit(pause_overlay, po_rect)
                cont_surf = self.font.render("Click Resume or Press P", True, WHITE)
                cont_rect = cont_surf.get_rect(center=(self.center_x, self.screen_height // 2 + 30))
                self.screen.blit(cont_surf, cont_rect)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            if self.state == 'playing':
                self.move()
            self.draw()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.run()