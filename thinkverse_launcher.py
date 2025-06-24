#!/usr/bin/env python3
"""
ThinkVerse Game Launcher
A pygame-based game launcher with multiple mini-games
"""

import pygame
import sys
import subprocess
import os
import math
from pathlib import Path

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (41, 128, 185)
DARK_BLUE = (52, 73, 94)
LIGHT_BLUE = (174, 214, 241)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
GRAY = (149, 165, 166)
LIGHT_GRAY = (236, 240, 241)
DARK_GRAY = (127, 140, 141)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

class GameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ThinkVerse - Game Launcher")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Game list with their corresponding script files and colors
        self.games = [
            {
                "name": "Code Breaker", 
                "file": "code_breaker.py", 
                "desc": "Logic puzzle - guess the secret code with hints",
                "category": "Puzzle",
                "color": BLUE
            },
            {
                "name": "AI Dungeon Quest", 
                "file": "ai_dungeon_quest.py", 
                "desc": "Text adventure with branching story choices",
                "category": "Adventure",
                "color": PURPLE
            },
            {
                "name": "Memory Matrix", 
                "file": "memory_matrix.py", 
                "desc": "Remember and recall number patterns",
                "category": "Memory",
                "color": GREEN
            },
            {
                "name": "Mystery Sound", 
                "file": "mystery_sound.py", 
                "desc": "Guess objects from visual sound clues",
                "category": "Audio",
                "color": ORANGE
            },
            {
                "name": "Escape 404", 
                "file": "escape_404.py", 
                "desc": "Digital escape room with coding puzzles",
                "category": "Puzzle",
                "color": RED
            },
            {
                "name": "Quantum Dice", 
                "file": "quantum_dice.py", 
                "desc": "Strategic dice with probability choices",
                "category": "Strategy",
                "color": DARK_BLUE
            },
            {
                "name": "Quiz Master", 
                "file": "quiz_master.py", 
                "desc": "Test your knowledge with trivia questions",
                "category": "Trivia",
                "color": PURPLE
            },
            {
                "name": "Snake Classic", 
                "file": "snake_classic.py", 
                "desc": "Classic snake game with modern twists",
                "category": "Arcade",
                "color": GREEN
            }
        ]
        
        self.selected_game = 0
        self.running = True
        self.animation_time = 0
        self.hover_animation = {}
        
        # Initialize hover animations
        for i in range(len(self.games)):
            self.hover_animation[i] = 0
        
    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(44 + (52 - 44) * ratio)
            g = int(62 + (73 - 62) * ratio)
            b = int(80 + (94 - 80) * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Animated particles
        for i in range(20):
            x = (i * 50 + self.animation_time * 0.5) % (SCREEN_WIDTH + 100) - 50
            y = 100 + math.sin(self.animation_time * 0.01 + i) * 50
            size = 2 + math.sin(self.animation_time * 0.02 + i) * 1
            alpha = int(100 + math.sin(self.animation_time * 0.015 + i) * 50)
            
            # Create surface for alpha blending
            particle_surf = pygame.Surface((size * 2, size * 2))
            particle_surf.set_alpha(alpha)
            particle_surf.fill(LIGHT_BLUE)
            self.screen.blit(particle_surf, (x, y))
    
    def draw_header(self):
        """Draw the header section"""
        # Main title with glow effect
        title_text = "ThinkVerse"
        
        # Glow effect
        for offset in range(3, 0, -1):
            glow_surface = self.font_title.render(title_text, True, LIGHT_BLUE)
            glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH//2 + offset, 80 + offset))
            glow_surface.set_alpha(30)
            self.screen.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = self.font_title.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Game Collection"
        subtitle_surface = self.font_medium.render(subtitle_text, True, LIGHT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Decorative line
        line_y = 150
        pygame.draw.line(self.screen, LIGHT_BLUE, (200, line_y), (SCREEN_WIDTH - 200, line_y), 2)
    
    def draw_game_icon(self, game_name, x, y, size, color):
        """Draw custom game icons using simple graphics"""
        center_x, center_y = x, y
        
        if "Code Breaker" in game_name:
            # Draw a lock icon
            pygame.draw.rect(self.screen, color, (center_x - size//3, center_y - size//6, size//1.5, size//2), 3)
            pygame.draw.circle(self.screen, color, (center_x, center_y - size//3), size//4, 3)
            
        elif "AI Dungeon" in game_name:
            # Draw a castle icon
            points = [(center_x - size//2, center_y + size//3), 
                     (center_x - size//2, center_y - size//3),
                     (center_x - size//4, center_y - size//3),
                     (center_x - size//4, center_y - size//6),
                     (center_x, center_y - size//6),
                     (center_x, center_y - size//3),
                     (center_x + size//4, center_y - size//3),
                     (center_x + size//4, center_y - size//6),
                     (center_x + size//2, center_y - size//6),
                     (center_x + size//2, center_y + size//3)]
            pygame.draw.polygon(self.screen, color, points, 3)
            
        elif "Memory Matrix" in game_name:
            # Draw a brain/grid icon
            for i in range(3):
                for j in range(3):
                    rect_x = center_x - size//3 + i * size//3
                    rect_y = center_y - size//3 + j * size//3
                    pygame.draw.rect(self.screen, color, (rect_x, rect_y, size//4, size//4), 2)
                    
        elif "Mystery Sound" in game_name:
            # Draw sound waves
            for i in range(3):
                radius = size//4 + i * size//8
                pygame.draw.circle(self.screen, color, (center_x, center_y), radius, 2)
                
        elif "Escape 404" in game_name:
            # Draw a computer/terminal icon
            pygame.draw.rect(self.screen, color, (center_x - size//2, center_y - size//3, size, size//1.5), 3)
            pygame.draw.rect(self.screen, color, (center_x - size//3, center_y - size//6, size//1.5, size//3))
            pygame.draw.line(self.screen, color, (center_x - size//4, center_y), (center_x + size//4, center_y), 2)
            
        elif "Quantum Dice" in game_name:
            # Draw dice
            pygame.draw.rect(self.screen, color, (center_x - size//3, center_y - size//3, size//1.5, size//1.5), 3)
            # Draw dots
            pygame.draw.circle(self.screen, color, (center_x - size//6, center_y - size//6), 3)
            pygame.draw.circle(self.screen, color, (center_x + size//6, center_y + size//6), 3)
            
        elif "Quiz Master" in game_name:
            # Draw question mark
            pygame.draw.circle(self.screen, color, (center_x, center_y - size//4), size//3, 3)
            pygame.draw.circle(self.screen, color, (center_x, center_y + size//4), size//8)
            
        elif "Snake Classic" in game_name:
            # Draw snake
            snake_segments = [(center_x - size//2, center_y), (center_x - size//4, center_y), 
                            (center_x, center_y), (center_x + size//4, center_y - size//4)]
            for i, pos in enumerate(snake_segments):
                radius = size//6 if i == 0 else size//8
                pygame.draw.circle(self.screen, color, pos, radius)
                if i < len(snake_segments) - 1:
                    pygame.draw.line(self.screen, color, pos, snake_segments[i + 1], size//8)
        else:
            # Default icon - simple circle
            pygame.draw.circle(self.screen, color, (center_x, center_y), size//2, 3)

    def draw_game_card(self, game, index, x, y, width, height):
        """Draw an individual game card"""
        # Update hover animation
        if index == self.selected_game:
            self.hover_animation[index] = min(1.0, self.hover_animation[index] + 0.1)
        else:
            self.hover_animation[index] = max(0.0, self.hover_animation[index] - 0.1)
        
        # Calculate animation values
        hover_offset = int(self.hover_animation[index] * 10)
        card_y = y - hover_offset
        
        # Card shadow
        shadow_rect = pygame.Rect(x + 5, card_y + 5, width, height)
        shadow_surf = pygame.Surface((width, height))
        shadow_surf.set_alpha(50)
        shadow_surf.fill(BLACK)
        self.screen.blit(shadow_surf, shadow_rect)
        
        # Main card background
        card_rect = pygame.Rect(x, card_y, width, height)
        if index == self.selected_game:
            # Selected card with gradient
            for i in range(height):
                ratio = i / height
                base_color = game["color"]
                highlight_color = tuple(min(255, c + 30) for c in base_color)
                r = int(base_color[0] + (highlight_color[0] - base_color[0]) * ratio)
                g = int(base_color[1] + (highlight_color[1] - base_color[1]) * ratio)
                b = int(base_color[2] + (highlight_color[2] - base_color[2]) * ratio)
                pygame.draw.line(self.screen, (r, g, b), (x, card_y + i), (x + width, card_y + i))
        else:
            pygame.draw.rect(self.screen, WHITE, card_rect)
        
        # Card border
        border_color = game["color"] if index == self.selected_game else LIGHT_GRAY
        border_width = 3 if index == self.selected_game else 1
        pygame.draw.rect(self.screen, border_color, card_rect, border_width)
        
        # Game icon (custom drawn)
        icon_y = card_y + 35
        self.draw_game_icon(game["name"], x + width//2, icon_y, 30, game["color"])
        
        # Game name
        name_color = WHITE if index == self.selected_game else BLACK
        name_surface = self.font_medium.render(game["name"], True, name_color)
        name_rect = name_surface.get_rect(center=(x + width//2, card_y + 80))
        self.screen.blit(name_surface, name_rect)
        
        # Game category
        category_color = LIGHT_GRAY if index == self.selected_game else GRAY
        category_surface = self.font_small.render(game["category"], True, category_color)
        category_rect = category_surface.get_rect(center=(x + width//2, card_y + 105))
        self.screen.blit(category_surface, category_rect)
        
        # Game description (wrapped)
        desc_lines = self.wrap_text(game["desc"], width - 20, self.font_tiny)
        desc_color = LIGHT_GRAY if index == self.selected_game else DARK_GRAY
        for i, line in enumerate(desc_lines[:2]):  # Max 2 lines
            desc_surface = self.font_tiny.render(line, True, desc_color)
            desc_rect = desc_surface.get_rect(center=(x + width//2, card_y + 130 + i * 16))
            self.screen.blit(desc_surface, desc_rect)
        
        # Game number
        number_text = str(index + 1)
        number_surface = self.font_small.render(number_text, True, WHITE if index == self.selected_game else game["color"])
        number_rect = pygame.Rect(x + width - 25, card_y + 5, 20, 20)
        pygame.draw.circle(self.screen, game["color"] if index == self.selected_game else LIGHT_GRAY, 
                          (x + width - 15, card_y + 15), 12)
        number_rect = number_surface.get_rect(center=(x + width - 15, card_y + 15))
        self.screen.blit(number_surface, number_rect)
    
    def wrap_text(self, text, max_width, font):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw_game_grid(self):
        """Draw the grid of game cards"""
        cards_per_row = 4
        card_width = 200
        card_height = 180
        padding = 20
        
        start_x = (SCREEN_WIDTH - (cards_per_row * card_width + (cards_per_row - 1) * padding)) // 2
        start_y = 200
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = start_x + col * (card_width + padding)
            y = start_y + row * (card_height + padding)
            
            self.draw_game_card(game, i, x, y, card_width, card_height)
    
    def draw_footer(self):
        """Draw the footer with instructions"""
        footer_y = SCREEN_HEIGHT - 80
        
        # Background bar
        footer_rect = pygame.Rect(0, footer_y, SCREEN_WIDTH, 80)
        footer_surf = pygame.Surface((SCREEN_WIDTH, 80))
        footer_surf.set_alpha(150)
        footer_surf.fill(BLACK)
        self.screen.blit(footer_surf, (0, footer_y))
        
        # Instructions
        instructions = [
            "Navigation: ← → ↑ ↓ Arrow Keys  |  Launch: ENTER or Number Keys (1-8)  |  Quit: ESC",
            "Select a game and press ENTER to launch, or use number keys for direct access"
        ]
        
        for i, instruction in enumerate(instructions):
            color = WHITE if i == 0 else LIGHT_GRAY
            font = self.font_small if i == 0 else self.font_tiny
            
            instruction_surface = font.render(instruction, True, color)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, footer_y + 25 + i * 25))
            self.screen.blit(instruction_surface, instruction_rect)
    
    def draw_selected_game_info(self):
        """Draw detailed info for selected game"""
        if not self.games:
            return
        
        selected_game = self.games[self.selected_game]
        
        # Info panel background
        panel_width = 300
        panel_height = 120
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = 180
        
        panel_surf = pygame.Surface((panel_width, panel_height))
        panel_surf.set_alpha(200)
        panel_surf.fill(BLACK)
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Border
        pygame.draw.rect(self.screen, selected_game["color"], 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Selected game title
        title_surface = self.font_medium.render("Selected Game", True, WHITE)
        self.screen.blit(title_surface, (panel_x + 10, panel_y + 10))
        
        # Game name
        name_surface = self.font_large.render(selected_game["name"], True, selected_game["color"])
        self.screen.blit(name_surface, (panel_x + 10, panel_y + 35))
        
        # Full description
        desc_lines = self.wrap_text(selected_game["desc"], panel_width - 20, self.font_small)
        for i, line in enumerate(desc_lines[:3]):  # Max 3 lines
            desc_surface = self.font_small.render(line, True, LIGHT_GRAY)
            self.screen.blit(desc_surface, (panel_x + 10, panel_y + 70 + i * 18))
    
    def draw_menu(self):
        """Draw the complete menu"""
        self.draw_background()
        self.draw_header()
        self.draw_game_grid()
        self.draw_selected_game_info()
        self.draw_footer()
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    if self.selected_game >= 4:
                        self.selected_game -= 4
                elif event.key == pygame.K_DOWN:
                    if self.selected_game < len(self.games) - 4:
                        self.selected_game += 4
                elif event.key == pygame.K_LEFT:
                    self.selected_game = (self.selected_game - 1) % len(self.games)
                elif event.key == pygame.K_RIGHT:
                    self.selected_game = (self.selected_game + 1) % len(self.games)
                elif event.key == pygame.K_RETURN:
                    self.launch_game()
                elif event.key >= pygame.K_1 and event.key <= pygame.K_8:
                    # Direct number selection
                    game_num = event.key - pygame.K_1
                    if game_num < len(self.games):
                        self.selected_game = game_num
                        self.launch_game()
    
    def launch_game(self):
        game_file = self.games[self.selected_game]['file']
        game_path = Path(__file__).parent / game_file
        
        if game_path.exists():
            try:
                # Launch the game as a separate process
                subprocess.Popen([sys.executable, str(game_path)])
                print(f"Launched: {self.games[self.selected_game]['name']}")
            except Exception as e:
                print(f"Error launching game: {e}")
        else:
            print(f"Game file not found: {game_file}")
    
    def run(self):
        while self.running:
            self.animation_time += 1
            self.handle_events()
            self.draw_menu()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()
