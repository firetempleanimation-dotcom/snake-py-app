import curses
import random

GRID_HEIGHT = 20
GRID_WIDTH = 40
SNAKE_CHAR = '#'
FOOD_CHAR = 'O'
BORDER_OFFSET = 1  # For the border around the grid

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
        if food not in snake:
            return food

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)
    stdscr.timeout(100)  # 100ms timeout for getch (10 FPS)

    # Create a window with borders
    win = curses.newwin(GRID_HEIGHT + 2, GRID_WIDTH + 2, 0, 0)
    win.keypad(True)
    win.border(0)
    win.timeout(100)

    # Initial snake position (list of (y, x) tuples)
    snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2 + i) for i in range(3, 0, -1)]
    direction = (0, 1)  # (dy, dx) - right
    food = generate_food(snake)
    score = 0

    # Direction mappings
    directions = {
        curses.KEY_UP: (-1, 0),
        curses.KEY_DOWN: (1, 0),
        curses.KEY_LEFT: (0, -1),
        curses.KEY_RIGHT: (0, 1)
    }

    while True:
        # Handle input
        key = win.getch()
        if key in directions:
            new_dir = directions[key]
            # Prevent reversing direction
            if new_dir != (-direction[0], -direction[1]):
                direction = new_dir

        # Move snake
        head_y, head_x = snake[0]
        dy, dx = direction
        new_head = ((head_y + dy) % GRID_HEIGHT, (head_x + dx) % GRID_WIDTH)

        # Check self-collision
        if new_head in snake:
            break  # Game over

        # Insert new head
        snake.insert(0, new_head)

        # Check if ate food
        if new_head == food:
            score += 1
            food = generate_food(snake)
        else:
            # Remove tail
            snake.pop()

        # Clear window and redraw border
        win.clear()
        win.border(0)

        # Draw score
        win.addstr(0, 2, f"Score: {score}")

        # Draw snake
        for y, x in snake:
            win.addch(y + BORDER_OFFSET, x + BORDER_OFFSET, SNAKE_CHAR)

        # Draw food
        win.addch(food[0] + BORDER_OFFSET, food[1] + BORDER_OFFSET, FOOD_CHAR)

        win.refresh()

    # Game over
    win.addstr(GRID_HEIGHT // 2, GRID_WIDTH // 2 - 5, "Game Over!")
    win.refresh()
    win.nodelay(False)
    win.getch()

if __name__ == "__main__":
    curses.wrapper(main)