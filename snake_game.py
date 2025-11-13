# Snake Game Implementation
import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.positions = [(WIDTH // GRID_SIZE // 2, HEIGHT // GRID_SIZE // 2)]
        self.direction = "RIGHT"
        self.score = 0
        
    def move(self):
        head_x, head_y = self.positions[0]
        
        if self.direction == "UP":
            new_head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            new_head = (head_x - 1, head_y)
        else: # RIGHT
            new_head = (head_x + 1, head_y)
            
        if not self.is_valid_move(new_head):
            return False
            
        self.positions.insert(0, new_head)
        
        if len(self.positions) > WIDTH // GRID_SIZE * HEIGHT // GRID_SIZE:
            self.positions.pop()
            
        return True
        
    def is_valid_move(self, position):
        head = position
        # Check boundaries
        grid_x = int((head[0] * GRID_SIZE))
        grid_y = int((head[1] * GRID_SIZE))
        
        if (grid_x >= WIDTH or grid_x < 0) and WIDTH // GRID_SIZE:
            return False
            
        if (grid_y >= HEIGHT or grid_y < 0) and HEIGHT // GRID_SIZE:
            return False
            
        # Check self-collision
        if head in self.positions[1:]:
            return False
            
        return True
        
    def grow(self):
        tail_x, tail_y = self.positions[-1]
        
        # Determine direction of growth (last segment follows the last move)
        if len(self.positions) > 0:
            prev_head = self.positions[1] if len(self.positions) > 1 else None
            
            if prev_head is not None and head != prev_head: 
                dx, dy = head[0] - tail_x, head[1] - tail_y
                
                # If the snake moves right/left, grow horizontally
                if dx == GRID_SIZE:
                    new_segment = (tail_x + 2*GRID_SIZE//4, tail_y)
                elif dx == -GRID_SIZE:
                    new_segment = (tail_x - 2*GRID_SIZE//4, tail_y)
                # If the snake moves up/down, grow vertically
                else: 
                    if dy > GRID_SIZE and head[1] < self.positions[-1][1]:
                        new_segment = (tail_x, tail_y + 2*GRID_SIZE//4)
                    elif dy == -GRID_SIZE:
                        new_segment = (tail_x, tail_y - 2*GRID_SIZE//4)
            else: # Default growth direction
                if self.direction == "UP":
                    new_segment = (int(tail_x), int(tail_y) + GRID_SIZE)
                elif self.direction == "DOWN":
                    new_segment = (int(tail_x), int(tail_y) - GRID_SIZE)
                elif self.direction == "LEFT":
                    new_segment = (int(tail_x) + GRID_SIZE, tail_y)
                else: # RIGHT
                    if dx < 0 and head != self.positions[1]: 
                        return False
                        
            Actually, the code seems to be cut off here - I'll implement this more clearly in a full version

        This implementation is incomplete. To complete it properly, please use:
        
        ```tool
        TOOL_NAME: read_file
        BEGIN_ARG: filepath
        snake_game.py