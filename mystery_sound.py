#!/usr/bin/env python3
"""
Mystery Sound - Play sound-based clues and let player guess the object
Note: This version uses visual representations of sounds since actual audio files aren't available
"""

import pygame
import random
import sys
import math

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
PURPLE = (128, 0, 128)

class MysterySound:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mystery Sound")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Sound objects with visual representations and clues
        self.sound_objects = [
            {
                "name": "RAIN",
                "clues": ["Pitter-patter on the roof", "Water falling from sky", "Makes plants grow"],
                "visual": "rain_drops",
                "frequency": "medium",
                "pattern": "random_drops"
            },
            {
                "name": "CLOCK",
                "clues": ["Tick-tock rhythm", "Measures time", "Has hands that move"],
                "visual": "clock_ticking",
                "frequency": "steady",
                "pattern": "metronome"
            },
            {
                "name": "OCEAN",
                "clues": ["Waves crashing", "Salty water", "Seagulls nearby"],
                "visual": "wave_motion",
                "frequency": "low",
                "pattern": "wave_cycle"
            },
            {
                "name": "FIRE",
                "clues": ["Crackling and popping", "Warm and bright", "Needs wood to burn"],
                "visual": "flame_flicker",
                "frequency": "variable",
                "pattern": "random_crackle"
            },
            {
                "name": "BIRD",
                "clues": ["Chirping melody", "Has feathers and wings", "Builds nests in trees"],
                "visual": "sound_waves",
                "frequency": "high",
                "pattern": "chirp_sequence"
            },
            {
                "name": "TRAIN",
                "clues": ["Choo-choo sound", "Runs on tracks", "Carries passengers"],
                "visual": "train_rhythm",
                "frequency": "low",
                "pattern": "locomotive"
            },
            {
                "name": "WIND",
                "clues": ["Whooshing through trees", "Invisible but felt", "Makes leaves rustle"],
                "visual": "wind_lines",
                "frequency": "variable",
                "pattern": "wind_gusts"
            },
            {
                "name": "BELL",
                "clues": ["Ding-dong sound", "Made of metal", "Rings to get attention"],
                "visual": "bell_rings",
                "frequency": "clear",
                "pattern": "bell_toll"
            }
        ]
        
        self.current_object = None
        self.current_clue_index = 0
        self.score = 0
        self.round_number = 1
        self.max_rounds = 8
        self.game_state = "menu"  # menu, playing, guessing, result, game_over
        self.user_guess = ""
        self.animation_time = 0
        self.clues_revealed = 0
        self.max_clues = 3
        
        self.start_new_round()
    
    def start_new_round(self):
        """Start a new round with a random sound object"""
        if self.round_number <= self.max_rounds:
            self.current_object = random.choice(self.sound_objects)
            self.current_clue_index = 0
            self.clues_revealed = 0
            self.user_guess = ""
            self.animation_time = 0
            if self.game_state != "menu":
                self.game_state = "playing"
        else:
            self.game_state = "game_over"
    
    def draw_visual_sound(self):
        """Draw visual representation of the current sound"""
        if not self.current_object:
            return
        
        center_x, center_y = SCREEN_WIDTH // 2, 250
        self.animation_time += 1
        
        visual_type = self.current_object["visual"]
        
        if visual_type == "rain_drops":
            # Draw falling rain drops
            for i in range(20):
                x = 100 + (i * 30) % 600
                y = (100 + (self.animation_time + i * 10) % 300) % 200 + 150
                pygame.draw.circle(self.screen, BLUE, (x, y), 3)
        
        elif visual_type == "clock_ticking":
            # Draw clock with moving hand
            pygame.draw.circle(self.screen, BLACK, (center_x, center_y), 80, 3)
            angle = (self.animation_time * 2) % 360
            end_x = center_x + 60 * math.cos(math.radians(angle))
            end_y = center_y + 60 * math.sin(math.radians(angle))
            pygame.draw.line(self.screen, RED, (center_x, center_y), (end_x, end_y), 3)
        
        elif visual_type == "wave_motion":
            # Draw ocean waves
            for x in range(0, SCREEN_WIDTH, 10):
                wave_height = 20 * math.sin((x + self.animation_time * 2) * 0.02)
                y = center_y + wave_height
                pygame.draw.circle(self.screen, BLUE, (x, int(y)), 5)
        
        elif visual_type == "flame_flicker":
            # Draw flickering flame
            for i in range(5):
                flicker = random.randint(-10, 10)
                x = center_x + i * 10 - 20
                y = center_y + flicker
                color = (255, random.randint(100, 255), 0)  # Orange-red flame
                pygame.draw.circle(self.screen, color, (x, y), random.randint(5, 15))
        
        elif visual_type == "sound_waves":
            # Draw sound wave circles
            for i in range(3):
                radius = (self.animation_time + i * 20) % 100 + 20
                pygame.draw.circle(self.screen, GREEN, (center_x, center_y), radius, 2)
        
        elif visual_type == "train_rhythm":
            # Draw train wheel motion
            wheel_angle = (self.animation_time * 5) % 360
            for i in range(3):
                wheel_x = center_x + (i - 1) * 60
                pygame.draw.circle(self.screen, BLACK, (wheel_x, center_y), 30, 3)
                spoke_x = wheel_x + 20 * math.cos(math.radians(wheel_angle))
                spoke_y = center_y + 20 * math.sin(math.radians(wheel_angle))
                pygame.draw.line(self.screen, BLACK, (wheel_x, center_y), (spoke_x, spoke_y), 2)
        
        elif visual_type == "wind_lines":
            # Draw wind motion lines
            for i in range(10):
                x1 = 50 + i * 70
                y1 = center_y + 20 * math.sin((self.animation_time + i * 30) * 0.1)
                x2 = x1 + 50
                y2 = y1 + 10 * math.sin((self.animation_time + i * 30) * 0.1)
                pygame.draw.line(self.screen, GRAY, (x1, int(y1)), (x2, int(y2)), 2)
        
        elif visual_type == "bell_rings":
            # Draw bell with ring waves
            pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), 40)
            pygame.draw.circle(self.screen, BLACK, (center_x, center_y), 40, 3)
            if self.animation_time % 60 < 30:  # Ring effect
                for i in range(2):
                    radius = 50 + i * 20
                    pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), radius, 2)
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Mystery Sound", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Listen to the visual sound clues!",
            "Watch the animation and read the hints.",
            "Type your guess for what makes this sound.",
            "",
            "You get up to 3 clues per round.",
            "Score points for correct guesses!",
            "",
            "Press SPACE to start playing",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200 + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_playing(self):
        self.screen.fill(WHITE)
        
        # Title and round info
        title_text = self.font_large.render("Mystery Sound", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(title_text, title_rect)
        
        round_text = f"Round {self.round_number}/{self.max_rounds} | Score: {self.score}"
        round_surface = self.font_medium.render(round_text, True, BLACK)
        round_rect = round_surface.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(round_surface, round_rect)
        
        # Visual sound representation
        self.draw_visual_sound()
        
        # Clues section
        clues_y = 350
        clue_title = self.font_medium.render("Sound Clues:", True, PURPLE)
        self.screen.blit(clue_title, (50, clues_y))
        
        # Show revealed clues
        for i in range(self.clues_revealed):
            if i < len(self.current_object["clues"]):
                clue_text = f"{i+1}. {self.current_object['clues'][i]}"
                clue_surface = self.font_small.render(clue_text, True, BLACK)
                self.screen.blit(clue_surface, (70, clues_y + 30 + i * 25))
        
        # Instructions
        if self.clues_revealed < self.max_clues:
            instruction_text = f"Press SPACE for next clue ({self.clues_revealed}/{self.max_clues} revealed)"
            instruction_surface = self.font_small.render(instruction_text, True, GRAY)
            self.screen.blit(instruction_surface, (50, clues_y + 120))
        
        guess_instruction = "Press G to make your guess"
        guess_surface = self.font_small.render(guess_instruction, True, BLUE)
        self.screen.blit(guess_surface, (50, clues_y + 145))
    
    def draw_guessing(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Make Your Guess!", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Show all clues
        clues_y = 150
        for i, clue in enumerate(self.current_object["clues"]):
            clue_text = f"{i+1}. {clue}"
            clue_surface = self.font_small.render(clue_text, True, BLACK)
            self.screen.blit(clue_surface, (100, clues_y + i * 25))
        
        # Input field
        input_y = 300
        input_text = "Your guess: " + self.user_guess + "_"
        input_surface = self.font_medium.render(input_text, True, BLACK)
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH//2, input_y))
        self.screen.blit(input_surface, input_rect)
        
        # Instructions
        instruction_text = "Type your answer and press ENTER to submit"
        instruction_surface = self.font_small.render(instruction_text, True, GRAY)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def draw_result(self):
        self.screen.fill(WHITE)
        
        # Check if guess is correct
        correct = self.user_guess.upper() == self.current_object["name"]
        
        if correct:
            result_text = "Correct!"
            result_color = GREEN
            points = max(10, 30 - (self.clues_revealed * 5))  # More points for fewer clues
            self.score += points
            score_text = f"+{points} points!"
        else:
            result_text = "Incorrect!"
            result_color = RED
            score_text = "No points this round."
        
        # Display result
        result_surface = self.font_large.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(result_surface, result_rect)
        
        # Show correct answer
        answer_text = f"The answer was: {self.current_object['name']}"
        answer_surface = self.font_medium.render(answer_text, True, BLACK)
        answer_rect = answer_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(answer_surface, answer_rect)
        
        # Show score
        score_surface = self.font_medium.render(score_text, True, BLUE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(score_surface, score_rect)
        
        # Total score
        total_text = f"Total Score: {self.score}"
        total_surface = self.font_medium.render(total_text, True, BLACK)
        total_rect = total_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(total_surface, total_rect)
        
        # Continue instruction
        if self.round_number < self.max_rounds:
            continue_text = "Press SPACE to continue to next round"
        else:
            continue_text = "Press SPACE to see final results"
        
        continue_surface = self.font_small.render(continue_text, True, GRAY)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(continue_surface, continue_rect)
    
    def draw_game_over(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Game Complete!", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Final score
        final_score_text = f"Final Score: {self.score}/{self.max_rounds * 30}"
        final_score_surface = self.font_large.render(final_score_text, True, GREEN)
        final_score_rect = final_score_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(final_score_surface, final_score_rect)
        
        # Performance rating
        percentage = (self.score / (self.max_rounds * 30)) * 100
        if percentage >= 80:
            rating = "Excellent! You have great sound recognition skills!"
        elif percentage >= 60:
            rating = "Good job! You did well identifying the sounds."
        elif percentage >= 40:
            rating = "Not bad! Keep practicing your listening skills."
        else:
            rating = "Keep trying! Sound recognition takes practice."
        
        rating_surface = self.font_medium.render(rating, True, BLACK)
        rating_rect = rating_surface.get_rect(center=(SCREEN_WIDTH//2, 320))
        self.screen.blit(rating_surface, rating_rect)
        
        # Restart option
        restart_text = "Press R to play again or ESC to quit"
        restart_surface = self.font_small.render(restart_text, True, GRAY)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(restart_surface, restart_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                elif self.game_state == "playing":
                    if event.key == pygame.K_SPACE and self.clues_revealed < self.max_clues:
                        self.clues_revealed += 1
                    elif event.key == pygame.K_g:
                        self.game_state = "guessing"
                elif self.game_state == "guessing":
                    if event.key == pygame.K_RETURN:
                        if self.user_guess.strip():
                            self.game_state = "result"
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_guess = self.user_guess[:-1]
                    else:
                        # Add character to guess
                        if event.unicode.isalpha() or event.unicode.isspace():
                            self.user_guess += event.unicode.upper()
                elif self.game_state == "result":
                    if event.key == pygame.K_SPACE:
                        self.round_number += 1
                        self.start_new_round()
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart_game()
        return True
    
    def restart_game(self):
        self.score = 0
        self.round_number = 1
        self.game_state = "menu"
        self.start_new_round()
    
    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "guessing":
            self.draw_guessing()
        elif self.game_state == "result":
            self.draw_result()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = MysterySound()
    game.run()
