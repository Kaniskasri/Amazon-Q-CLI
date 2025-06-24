#!/usr/bin/env python3
"""
Quantum Dice - A strategic dice game with probability-based choices
"""

import pygame
import random
import sys
import math

pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class QuantumDice:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Dice")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.game_state = "menu"  # menu, playing, quantum_choice, result, game_over
        self.player_score = 0
        self.ai_score = 0
        self.round_number = 1
        self.max_rounds = 10
        self.target_score = 100
        
        # Dice states
        self.player_dice = []
        self.ai_dice = []
        self.dice_count = 3
        self.rolling = False
        self.roll_animation_time = 0
        self.roll_duration = 60  # frames
        
        # Quantum mechanics
        self.quantum_energy = 3  # Player starts with 3 quantum uses
        self.quantum_active = False
        self.quantum_choice = ""
        self.probability_boost = 0
        
        # Game choices
        self.current_choice = 0
        self.choices = [
            {"name": "Standard Roll", "desc": "Roll dice normally", "cost": 0},
            {"name": "Quantum Entanglement", "desc": "Reroll lowest die (Cost: 1 energy)", "cost": 1},
            {"name": "Probability Wave", "desc": "Boost all dice by +1 (Cost: 2 energy)", "cost": 2},
            {"name": "Superposition", "desc": "Roll extra die, keep best 3 (Cost: 3 energy)", "cost": 3}
        ]
        
        # AI strategy
        self.ai_strategy = "balanced"  # conservative, balanced, aggressive
        
    def roll_dice(self, count=3):
        """Roll a specified number of dice"""
        return [random.randint(1, 6) for _ in range(count)]
    
    def calculate_score(self, dice):
        """Calculate score from dice with special combinations"""
        if not dice:
            return 0
        
        dice_sorted = sorted(dice, reverse=True)
        base_score = sum(dice_sorted)
        
        # Bonus scoring
        bonus = 0
        
        # Three of a kind
        if len(set(dice)) == 1:
            bonus += 20
        # Pair
        elif len(set(dice)) == 2:
            bonus += 10
        # Straight (1,2,3 or 4,5,6)
        elif sorted(dice) == [1, 2, 3] or sorted(dice) == [4, 5, 6]:
            bonus += 15
        # All high (4,5,6)
        elif all(d >= 4 for d in dice):
            bonus += 5
        
        return base_score + bonus
    
    def apply_quantum_effect(self, dice, effect):
        """Apply quantum effect to dice"""
        if effect == "entanglement":
            # Reroll the lowest die
            min_index = dice.index(min(dice))
            dice[min_index] = random.randint(1, 6)
        elif effect == "wave":
            # Boost all dice by 1 (max 6)
            dice = [min(6, d + 1) for d in dice]
        elif effect == "superposition":
            # Roll 4 dice, keep best 3
            extra_dice = self.roll_dice(4)
            dice = sorted(extra_dice, reverse=True)[:3]
        
        return dice
    
    def ai_make_choice(self):
        """AI makes strategic choice based on current situation"""
        # Simple AI strategy
        if self.ai_strategy == "conservative":
            return "standard"
        elif self.ai_strategy == "aggressive":
            # AI doesn't have quantum energy, so always standard
            return "standard"
        else:  # balanced
            return "standard"
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Title with quantum effect
        title_text = "QUANTUM DICE"
        title_surface = self.font_large.render(title_text, True, PURPLE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Strategic Dice Game with Probability Manipulation"
        subtitle_surface = self.font_medium.render(subtitle_text, True, BLUE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 140))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game rules
        rules = [
            "GAME RULES:",
            "• Roll 3 dice each turn to score points",
            "• First to 100 points wins (or highest after 10 rounds)",
            "• Use quantum energy for special abilities:",
            "  - Entanglement: Reroll lowest die (1 energy)",
            "  - Probability Wave: +1 to all dice (2 energy)",
            "  - Superposition: Roll 4, keep best 3 (3 energy)",
            "",
            "SCORING BONUSES:",
            "• Three of a kind: +20 points",
            "• Pair: +10 points",
            "• Straight (1,2,3 or 4,5,6): +15 points",
            "• All high dice (4,5,6): +5 points"
        ]
        
        for i, rule in enumerate(rules):
            color = BLUE if rule.startswith("•") or rule.startswith("  -") else BLACK
            if rule.startswith("GAME RULES:") or rule.startswith("SCORING BONUSES:"):
                color = PURPLE
            
            text_surface = self.font_small.render(rule, True, color)
            self.screen.blit(text_surface, (100, 200 + i * 25))
        
        # Start instruction
        start_text = "Press SPACE to start playing"
        start_surface = self.font_medium.render(start_text, True, GREEN)
        start_rect = start_surface.get_rect(center=(SCREEN_WIDTH//2, 600))
        self.screen.blit(start_surface, start_rect)
    
    def draw_dice(self, dice, x, y, size=60):
        """Draw dice at specified position"""
        for i, die_value in enumerate(dice):
            die_x = x + i * (size + 10)
            die_y = y
            
            # Draw die background
            pygame.draw.rect(self.screen, WHITE, (die_x, die_y, size, size))
            pygame.draw.rect(self.screen, BLACK, (die_x, die_y, size, size), 3)
            
            # Draw dots based on die value
            self.draw_die_dots(die_x, die_y, size, die_value)
    
    def draw_die_dots(self, x, y, size, value):
        """Draw dots on a die face"""
        dot_size = size // 8
        center_x = x + size // 2
        center_y = y + size // 2
        offset = size // 4
        
        # Dot positions
        positions = {
            1: [(center_x, center_y)],
            2: [(x + offset, y + offset), (x + size - offset, y + size - offset)],
            3: [(x + offset, y + offset), (center_x, center_y), (x + size - offset, y + size - offset)],
            4: [(x + offset, y + offset), (x + size - offset, y + offset), 
                (x + offset, y + size - offset), (x + size - offset, y + size - offset)],
            5: [(x + offset, y + offset), (x + size - offset, y + offset), (center_x, center_y),
                (x + offset, y + size - offset), (x + size - offset, y + size - offset)],
            6: [(x + offset, y + offset), (x + size - offset, y + offset),
                (x + offset, center_y), (x + size - offset, center_y),
                (x + offset, y + size - offset), (x + size - offset, y + size - offset)]
        }
        
        for dot_x, dot_y in positions.get(value, []):
            pygame.draw.circle(self.screen, BLACK, (int(dot_x), int(dot_y)), dot_size)
    
    def draw_playing(self):
        self.screen.fill(WHITE)
        
        # Title and round info
        title_text = f"Quantum Dice - Round {self.round_number}/{self.max_rounds}"
        title_surface = self.font_large.render(title_text, True, PURPLE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Scores
        score_y = 80
        player_score_text = f"Your Score: {self.player_score}"
        ai_score_text = f"AI Score: {self.ai_score}"
        
        player_score_surface = self.font_medium.render(player_score_text, True, BLUE)
        ai_score_surface = self.font_medium.render(ai_score_text, True, RED)
        
        self.screen.blit(player_score_surface, (100, score_y))
        self.screen.blit(ai_score_surface, (SCREEN_WIDTH - 200, score_y))
        
        # Quantum energy
        energy_text = f"Quantum Energy: {self.quantum_energy}"
        energy_surface = self.font_medium.render(energy_text, True, PURPLE)
        energy_rect = energy_surface.get_rect(center=(SCREEN_WIDTH//2, score_y))
        self.screen.blit(energy_surface, energy_rect)
        
        # Player dice
        if self.player_dice:
            player_label = "Your Dice:"
            player_label_surface = self.font_medium.render(player_label, True, BLUE)
            self.screen.blit(player_label_surface, (100, 150))
            
            if self.rolling:
                # Show random dice during animation
                animated_dice = [random.randint(1, 6) for _ in range(len(self.player_dice))]
                self.draw_dice(animated_dice, 100, 180)
            else:
                self.draw_dice(self.player_dice, 100, 180)
            
            # Show player score for this round
            round_score = self.calculate_score(self.player_dice)
            score_text = f"Round Score: {round_score}"
            score_surface = self.font_small.render(score_text, True, BLUE)
            self.screen.blit(score_surface, (100, 260))
        
        # AI dice
        if self.ai_dice:
            ai_label = "AI Dice:"
            ai_label_surface = self.font_medium.render(ai_label, True, RED)
            self.screen.blit(ai_label_surface, (500, 150))
            
            self.draw_dice(self.ai_dice, 500, 180)
            
            # Show AI score for this round
            ai_round_score = self.calculate_score(self.ai_dice)
            ai_score_text = f"Round Score: {ai_round_score}"
            ai_score_surface = self.font_small.render(ai_score_text, True, RED)
            self.screen.blit(ai_score_surface, (500, 260))
        
        # Quantum choices
        if not self.rolling and not self.player_dice:
            choice_y = 350
            choice_title = "Choose Your Strategy:"
            choice_title_surface = self.font_medium.render(choice_title, True, BLACK)
            self.screen.blit(choice_title_surface, (100, choice_y))
            
            for i, choice in enumerate(self.choices):
                y_pos = choice_y + 40 + i * 60
                
                # Check if player can afford this choice
                can_afford = self.quantum_energy >= choice["cost"]
                text_color = BLACK if can_afford else GRAY
                bg_color = LIGHT_GRAY if i == self.current_choice and can_afford else None
                
                # Draw background for selected choice
                if bg_color:
                    pygame.draw.rect(self.screen, bg_color, (90, y_pos - 5, 700, 50))
                
                # Choice text
                choice_text = f"{i+1}. {choice['name']} - {choice['desc']}"
                if choice["cost"] > 0:
                    choice_text += f" (Cost: {choice['cost']} energy)"
                
                choice_surface = self.font_small.render(choice_text, True, text_color)
                self.screen.blit(choice_surface, (100, y_pos))
            
            # Instructions
            instruction_text = "Use UP/DOWN to select, ENTER to choose, or press 1-4 for direct selection"
            instruction_surface = self.font_small.render(instruction_text, True, GRAY)
            self.screen.blit(instruction_surface, (100, 600))
        
        elif self.rolling:
            # Show rolling animation
            rolling_text = "Rolling dice..."
            rolling_surface = self.font_large.render(rolling_text, True, PURPLE)
            rolling_rect = rolling_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
            self.screen.blit(rolling_surface, rolling_rect)
        
        elif self.player_dice and self.ai_dice:
            # Show round results
            player_round_score = self.calculate_score(self.player_dice)
            ai_round_score = self.calculate_score(self.ai_dice)
            
            if player_round_score > ai_round_score:
                result_text = "You won this round!"
                result_color = GREEN
            elif ai_round_score > player_round_score:
                result_text = "AI won this round!"
                result_color = RED
            else:
                result_text = "Round tied!"
                result_color = YELLOW
            
            result_surface = self.font_large.render(result_text, True, result_color)
            result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
            self.screen.blit(result_surface, result_rect)
            
            continue_text = "Press SPACE to continue"
            continue_surface = self.font_medium.render(continue_text, True, BLACK)
            continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH//2, 450))
            self.screen.blit(continue_surface, continue_rect)
    
    def draw_game_over(self):
        self.screen.fill(WHITE)
        
        # Determine winner
        if self.player_score > self.ai_score:
            winner_text = "VICTORY!"
            winner_color = GREEN
            result_text = "You defeated the AI!"
        elif self.ai_score > self.player_score:
            winner_text = "DEFEAT!"
            winner_color = RED
            result_text = "The AI won this time!"
        else:
            winner_text = "TIE GAME!"
            winner_color = YELLOW
            result_text = "It's a perfect tie!"
        
        # Display results
        winner_surface = self.font_large.render(winner_text, True, winner_color)
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(winner_surface, winner_rect)
        
        result_surface = self.font_medium.render(result_text, True, BLACK)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(result_surface, result_rect)
        
        # Final scores
        final_scores = f"Final Score - You: {self.player_score}, AI: {self.ai_score}"
        scores_surface = self.font_medium.render(final_scores, True, BLUE)
        scores_rect = scores_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(scores_surface, scores_rect)
        
        # Game stats
        rounds_text = f"Rounds played: {self.round_number - 1}"
        rounds_surface = self.font_small.render(rounds_text, True, BLACK)
        rounds_rect = rounds_surface.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(rounds_surface, rounds_rect)
        
        # Restart option
        restart_text = "Press R to play again or ESC to quit"
        restart_surface = self.font_medium.render(restart_text, True, GRAY)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, 450))
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
                    if not self.rolling and not self.player_dice:
                        # Choice selection
                        if event.key == pygame.K_UP:
                            self.current_choice = (self.current_choice - 1) % len(self.choices)
                        elif event.key == pygame.K_DOWN:
                            self.current_choice = (self.current_choice + 1) % len(self.choices)
                        elif event.key == pygame.K_RETURN:
                            self.make_choice()
                        elif event.key >= pygame.K_1 and event.key <= pygame.K_4:
                            choice_num = event.key - pygame.K_1
                            if choice_num < len(self.choices):
                                self.current_choice = choice_num
                                self.make_choice()
                    elif self.player_dice and self.ai_dice:
                        if event.key == pygame.K_SPACE:
                            self.next_round()
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart_game()
        return True
    
    def make_choice(self):
        """Execute the player's choice"""
        choice = self.choices[self.current_choice]
        
        # Check if player can afford the choice
        if self.quantum_energy < choice["cost"]:
            return
        
        # Deduct quantum energy
        self.quantum_energy -= choice["cost"]
        
        # Start rolling animation
        self.rolling = True
        self.roll_animation_time = 0
        
        # Roll initial dice
        self.player_dice = self.roll_dice(self.dice_count)
        
        # Apply quantum effects
        if choice["name"] == "Quantum Entanglement":
            self.player_dice = self.apply_quantum_effect(self.player_dice, "entanglement")
        elif choice["name"] == "Probability Wave":
            self.player_dice = self.apply_quantum_effect(self.player_dice, "wave")
        elif choice["name"] == "Superposition":
            self.player_dice = self.apply_quantum_effect(self.player_dice, "superposition")
        
        # AI rolls
        self.ai_dice = self.roll_dice(self.dice_count)
    
    def next_round(self):
        """Proceed to next round"""
        # Add scores
        self.player_score += self.calculate_score(self.player_dice)
        self.ai_score += self.calculate_score(self.ai_dice)
        
        # Reset for next round
        self.player_dice = []
        self.ai_dice = []
        self.round_number += 1
        
        # Restore some quantum energy each round
        self.quantum_energy = min(3, self.quantum_energy + 1)
        
        # Check win conditions
        if (self.player_score >= self.target_score or 
            self.ai_score >= self.target_score or 
            self.round_number > self.max_rounds):
            self.game_state = "game_over"
    
    def restart_game(self):
        """Restart the game"""
        self.player_score = 0
        self.ai_score = 0
        self.round_number = 1
        self.quantum_energy = 3
        self.player_dice = []
        self.ai_dice = []
        self.rolling = False
        self.current_choice = 0
        self.game_state = "menu"
    
    def update(self):
        """Update game state"""
        if self.rolling:
            self.roll_animation_time += 1
            if self.roll_animation_time >= self.roll_duration:
                self.rolling = False
    
    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = QuantumDice()
    game.run()
