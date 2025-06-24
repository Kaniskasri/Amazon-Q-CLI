#!/usr/bin/env python3
"""
Memory Matrix - Show a number pattern briefly and ask user to recall it
"""

import pygame
import random
import sys
import time

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

class MemoryMatrix:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memory Matrix")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.grid_size = 3  # Start with 3x3 grid
        self.level = 1
        self.score = 0
        self.lives = 3
        
        self.game_state = "menu"  # menu, showing, input, result
        self.pattern = []
        self.user_input = []
        self.show_start_time = 0
        self.show_duration = 3000  # 3 seconds
        
        self.selected_row = 0
        self.selected_col = 0
        
        self.generate_pattern()
    
    def generate_pattern(self):
        """Generate a random pattern for the current level"""
        self.pattern = []
        pattern_length = min(self.level + 2, self.grid_size * self.grid_size)
        
        # Generate unique positions
        positions = []
        for _ in range(pattern_length):
            while True:
                pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
                if pos not in positions:
                    positions.append(pos)
                    break
        
        # Assign numbers to positions
        for i, pos in enumerate(positions):
            self.pattern.append((pos[0], pos[1], i + 1))
        
        self.user_input = []
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Memory Matrix", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Remember the number sequence and positions!",
            "Numbers will appear briefly on the grid.",
            "Then click on the positions in the correct order.",
            "",
            "Press SPACE to start",
            "Use arrow keys and ENTER to select positions",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Level and score info
        level_text = f"Level: {self.level} | Score: {self.score} | Lives: {self.lives}"
        level_surface = self.font_medium.render(level_text, True, BLUE)
        level_rect = level_surface.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(level_surface, level_rect)
    
    def draw_grid(self, show_pattern=False):
        """Draw the game grid"""
        grid_start_x = (SCREEN_WIDTH - self.grid_size * 80) // 2
        grid_start_y = 200
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = grid_start_x + col * 80
                y = grid_start_y + row * 80
                
                # Determine cell color
                cell_color = WHITE
                if self.game_state == "input" and row == self.selected_row and col == self.selected_col:
                    cell_color = LIGHT_BLUE
                
                # Draw cell
                pygame.draw.rect(self.screen, cell_color, (x, y, 70, 70))
                pygame.draw.rect(self.screen, BLACK, (x, y, 70, 70), 2)
                
                # Show pattern numbers if in showing phase
                if show_pattern:
                    for pattern_row, pattern_col, number in self.pattern:
                        if pattern_row == row and pattern_col == col:
                            num_text = self.font_large.render(str(number), True, RED)
                            num_rect = num_text.get_rect(center=(x + 35, y + 35))
                            self.screen.blit(num_text, num_rect)
                
                # Show user input
                if self.game_state == "input":
                    for i, (input_row, input_col) in enumerate(self.user_input):
                        if input_row == row and input_col == col:
                            num_text = self.font_medium.render(str(i + 1), True, GREEN)
                            num_rect = num_text.get_rect(center=(x + 35, y + 35))
                            self.screen.blit(num_text, num_rect)
    
    def draw_showing_phase(self):
        self.screen.fill(WHITE)
        
        # Title and level info
        title_text = self.font_large.render("Memory Matrix", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        level_text = f"Level {self.level} - Memorize the sequence!"
        level_surface = self.font_medium.render(level_text, True, BLACK)
        level_rect = level_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(level_surface, level_rect)
        
        # Timer
        elapsed = pygame.time.get_ticks() - self.show_start_time
        remaining = max(0, self.show_duration - elapsed) / 1000
        timer_text = f"Time remaining: {remaining:.1f}s"
        timer_surface = self.font_small.render(timer_text, True, RED)
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(timer_surface, timer_rect)
        
        # Draw grid with pattern
        self.draw_grid(show_pattern=True)
        
        # Check if time is up
        if elapsed >= self.show_duration:
            self.game_state = "input"
    
    def draw_input_phase(self):
        self.screen.fill(WHITE)
        
        # Title and instructions
        title_text = self.font_large.render("Memory Matrix", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        instruction_text = "Click the positions in the correct order (1, 2, 3...)"
        instruction_surface = self.font_small.render(instruction_text, True, BLACK)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Progress
        progress_text = f"Progress: {len(self.user_input)}/{len(self.pattern)}"
        progress_surface = self.font_medium.render(progress_text, True, BLUE)
        progress_rect = progress_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(progress_surface, progress_rect)
        
        # Draw grid
        self.draw_grid(show_pattern=False)
        
        # Navigation instructions
        nav_text = "Use arrow keys to move, ENTER to select, BACKSPACE to undo"
        nav_surface = self.font_small.render(nav_text, True, GRAY)
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(nav_surface, nav_rect)
    
    def draw_result_phase(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Memory Matrix", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Check if user got it right
        correct = self.check_answer()
        
        if correct:
            result_text = "Correct! Well done!"
            result_color = GREEN
            self.score += self.level * 10
            self.level += 1
            if self.level % 3 == 0:  # Increase grid size every 3 levels
                self.grid_size = min(5, self.grid_size + 1)
        else:
            result_text = "Incorrect! Try again."
            result_color = RED
            self.lives -= 1
        
        result_surface = self.font_large.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(result_surface, result_rect)
        
        # Show correct pattern
        pattern_text = "Correct sequence was: " + " → ".join([f"({r+1},{c+1})" for r, c, n in sorted(self.pattern, key=lambda x: x[2])])
        pattern_surface = self.font_small.render(pattern_text, True, BLACK)
        pattern_rect = pattern_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(pattern_surface, pattern_rect)
        
        # Score and level info
        info_text = f"Score: {self.score} | Level: {self.level} | Lives: {self.lives}"
        info_surface = self.font_medium.render(info_text, True, BLUE)
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(info_surface, info_rect)
        
        # Game over check
        if self.lives <= 0:
            game_over_text = "Game Over! Final Score: " + str(self.score)
            game_over_surface = self.font_large.render(game_over_text, True, RED)
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(game_over_surface, game_over_rect)
            
            restart_text = "Press R to restart or ESC to quit"
            restart_surface = self.font_small.render(restart_text, True, BLACK)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
            self.screen.blit(restart_surface, restart_rect)
        else:
            continue_text = "Press SPACE to continue"
            continue_surface = self.font_small.render(continue_text, True, BLACK)
            continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
            self.screen.blit(continue_surface, continue_rect)
    
    def check_answer(self):
        """Check if user input matches the pattern"""
        if len(self.user_input) != len(self.pattern):
            return False
        
        # Sort pattern by number order
        sorted_pattern = sorted(self.pattern, key=lambda x: x[2])
        
        for i, (pattern_row, pattern_col, _) in enumerate(sorted_pattern):
            if i >= len(self.user_input):
                return False
            user_row, user_col = self.user_input[i]
            if user_row != pattern_row or user_col != pattern_col:
                return False
        
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "showing"
                        self.show_start_time = pygame.time.get_ticks()
                elif self.game_state == "input":
                    if event.key == pygame.K_UP:
                        self.selected_row = (self.selected_row - 1) % self.grid_size
                    elif event.key == pygame.K_DOWN:
                        self.selected_row = (self.selected_row + 1) % self.grid_size
                    elif event.key == pygame.K_LEFT:
                        self.selected_col = (self.selected_col - 1) % self.grid_size
                    elif event.key == pygame.K_RIGHT:
                        self.selected_col = (self.selected_col + 1) % self.grid_size
                    elif event.key == pygame.K_RETURN:
                        pos = (self.selected_row, self.selected_col)
                        if pos not in self.user_input:
                            self.user_input.append(pos)
                            if len(self.user_input) == len(self.pattern):
                                self.game_state = "result"
                    elif event.key == pygame.K_BACKSPACE and self.user_input:
                        self.user_input.pop()
                elif self.game_state == "result":
                    if self.lives <= 0:
                        if event.key == pygame.K_r:
                            self.restart_game()
                    else:
                        if event.key == pygame.K_SPACE:
                            self.generate_pattern()
                            self.game_state = "showing"
                            self.show_start_time = pygame.time.get_ticks()
        return True
    
    def restart_game(self):
        self.grid_size = 3
        self.level = 1
        self.score = 0
        self.lives = 3
        self.game_state = "menu"
        self.generate_pattern()
    
    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "showing":
            self.draw_showing_phase()
        elif self.game_state == "input":
            self.draw_input_phase()
        elif self.game_state == "result":
            self.draw_result_phase()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = MemoryMatrix()
    game.run()
