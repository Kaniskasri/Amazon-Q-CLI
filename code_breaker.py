#!/usr/bin/env python3
"""
Code Breaker - Logic puzzle game
Guess the secret 4-digit code with color-coded hints
"""

import pygame
import random
import sys

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

class CodeBreaker:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Code Breaker")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.secret_code = [random.randint(1, 6) for _ in range(4)]
        self.current_guess = [0, 0, 0, 0]
        self.current_position = 0
        self.attempts = []
        self.max_attempts = 10
        self.game_won = False
        self.game_over = False
        
        print(f"Secret code (for testing): {self.secret_code}")
    
    def check_guess(self, guess):
        """Return (correct_position, correct_number) counts"""
        correct_position = 0
        correct_number = 0
        
        secret_copy = self.secret_code.copy()
        guess_copy = guess.copy()
        
        # Check for correct positions first
        for i in range(4):
            if guess[i] == self.secret_code[i]:
                correct_position += 1
                secret_copy[i] = -1  # Mark as used
                guess_copy[i] = -1   # Mark as used
        
        # Check for correct numbers in wrong positions
        for i in range(4):
            if guess_copy[i] != -1:  # Not already matched
                if guess_copy[i] in secret_copy:
                    correct_number += 1
                    secret_copy[secret_copy.index(guess_copy[i])] = -1
        
        return correct_position, correct_number
    
    def draw_game(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Code Breaker", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        if not self.game_over:
            inst_text = "Guess the 4-digit code (1-6). Use number keys and ENTER to submit."
            instruction = self.font_small.render(inst_text, True, BLACK)
            self.screen.blit(instruction, (50, 80))
        
        # Current guess input
        if not self.game_over:
            guess_y = 120
            for i in range(4):
                x = 250 + i * 80
                color = LIGHT_GRAY if i == self.current_position else WHITE
                pygame.draw.rect(self.screen, color, (x, guess_y, 60, 60))
                pygame.draw.rect(self.screen, BLACK, (x, guess_y, 60, 60), 2)
                
                if self.current_guess[i] > 0:
                    num_text = self.font_medium.render(str(self.current_guess[i]), True, BLACK)
                    num_rect = num_text.get_rect(center=(x + 30, guess_y + 30))
                    self.screen.blit(num_text, num_rect)
        
        # Previous attempts
        attempts_y = 200
        for i, (guess, correct_pos, correct_num) in enumerate(self.attempts):
            y = attempts_y + i * 40
            
            # Draw guess
            for j in range(4):
                x = 150 + j * 50
                pygame.draw.rect(self.screen, WHITE, (x, y, 40, 30))
                pygame.draw.rect(self.screen, BLACK, (x, y, 40, 30), 1)
                
                num_text = self.font_small.render(str(guess[j]), True, BLACK)
                num_rect = num_text.get_rect(center=(x + 20, y + 15))
                self.screen.blit(num_text, num_rect)
            
            # Draw feedback
            feedback_x = 400
            # Correct positions (green circles)
            for k in range(correct_pos):
                pygame.draw.circle(self.screen, GREEN, (feedback_x + k * 20, y + 15), 8)
            
            # Correct numbers (yellow circles)
            for k in range(correct_num):
                pygame.draw.circle(self.screen, YELLOW, (feedback_x + (correct_pos + k) * 20, y + 15), 8)
        
        # Game status
        if self.game_won:
            win_text = self.font_large.render("Congratulations! You broke the code!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(win_text, win_rect)
        elif self.game_over:
            lose_text = self.font_large.render("Game Over! Code was: " + "".join(map(str, self.secret_code)), True, RED)
            lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(lose_text, lose_rect)
        
        # Attempts remaining
        if not self.game_over:
            attempts_text = f"Attempts remaining: {self.max_attempts - len(self.attempts)}"
            attempts_surface = self.font_small.render(attempts_text, True, BLACK)
            self.screen.blit(attempts_surface, (50, 550))
        
        # Legend
        legend_y = 520
        legend_text = "Legend: Green = Correct position, Yellow = Correct number wrong position"
        legend_surface = self.font_small.render(legend_text, True, GRAY)
        self.screen.blit(legend_surface, (50, legend_y))
        
        if self.game_over:
            restart_text = "Press R to restart or ESC to quit"
            restart_surface = self.font_small.render(restart_text, True, BLACK)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, 550))
            self.screen.blit(restart_surface, restart_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif not self.game_over:
                    if event.key >= pygame.K_1 and event.key <= pygame.K_6:
                        digit = event.key - pygame.K_0
                        self.current_guess[self.current_position] = digit
                        self.current_position = (self.current_position + 1) % 4
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_position = (self.current_position - 1) % 4
                        self.current_guess[self.current_position] = 0
                    elif event.key == pygame.K_RETURN:
                        self.submit_guess()
        return True
    
    def submit_guess(self):
        if 0 not in self.current_guess:  # All positions filled
            correct_pos, correct_num = self.check_guess(self.current_guess)
            self.attempts.append((self.current_guess.copy(), correct_pos, correct_num))
            
            if correct_pos == 4:
                self.game_won = True
                self.game_over = True
            elif len(self.attempts) >= self.max_attempts:
                self.game_over = True
            
            # Reset current guess
            self.current_guess = [0, 0, 0, 0]
            self.current_position = 0
    
    def restart_game(self):
        self.secret_code = [random.randint(1, 6) for _ in range(4)]
        self.current_guess = [0, 0, 0, 0]
        self.current_position = 0
        self.attempts = []
        self.game_won = False
        self.game_over = False
        print(f"New secret code (for testing): {self.secret_code}")
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw_game()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = CodeBreaker()
    game.run()
