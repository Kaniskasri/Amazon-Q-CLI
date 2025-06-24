#!/usr/bin/env python3
"""
Escape 404 - A puzzle game simulating a digital escape room
"""

import pygame
import random
import sys
import time

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
DARK_GRAY = (64, 64, 64)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

class Escape404:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Escape 404 - Digital Escape Room")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_mono = pygame.font.Font(None, 20)  # Monospace-like font
        
        self.game_state = "intro"  # intro, room1, room2, room3, victory
        self.current_puzzle = 0
        self.puzzles_solved = []
        self.inventory = []
        self.time_start = time.time()
        self.hints_used = 0
        
        # Room 1: Binary Code Puzzle
        self.binary_code = "01001000 01100101 01101100 01110000"  # "Help" in binary
        self.binary_input = ""
        
        # Room 2: Network Routing Puzzle
        self.network_grid = self.generate_network_grid()
        self.network_path = []
        self.network_start = (0, 0)
        self.network_end = (4, 4)
        
        # Room 3: Password Cracking
        self.password_clues = [
            "First pet's name backwards",
            "Birth year + favorite number",
            "Childhood street + lucky number"
        ]
        self.correct_password = "TIGER2023"
        self.password_input = ""
        
        # Terminal simulation
        self.terminal_lines = [
            "SYSTEM BOOT SEQUENCE INITIATED...",
            "ERROR 404: REALITY NOT FOUND",
            "ENTERING DIGITAL ESCAPE PROTOCOL",
            "OBJECTIVE: SOLVE PUZZLES TO ESCAPE",
            "",
            "Type 'help' for available commands"
        ]
        self.terminal_input = ""
        self.terminal_cursor = True
        self.cursor_timer = 0
    
    def generate_network_grid(self):
        """Generate a 5x5 network grid with obstacles"""
        grid = [[0 for _ in range(5)] for _ in range(5)]
        
        # Add some obstacles (1 = obstacle, 0 = free path)
        obstacles = [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)]
        for x, y in obstacles:
            grid[y][x] = 1
        
        return grid
    
    def draw_intro(self):
        self.screen.fill(BLACK)
        
        # Simulate terminal boot screen
        y_offset = 50
        for i, line in enumerate(self.terminal_lines):
            color = GREEN if "ERROR" not in line else RED
            if "404" in line:
                color = YELLOW
            
            text_surface = self.font_mono.render(line, True, color)
            self.screen.blit(text_surface, (50, y_offset + i * 25))
        
        # Blinking cursor
        self.cursor_timer += 1
        if self.cursor_timer % 60 < 30:  # Blink every second
            cursor_text = "> " + self.terminal_input + "_"
        else:
            cursor_text = "> " + self.terminal_input + " "
        
        cursor_surface = self.font_mono.render(cursor_text, True, GREEN)
        self.screen.blit(cursor_surface, (50, y_offset + len(self.terminal_lines) * 25 + 20))
        
        # Instructions
        instruction_text = "Type 'start' to begin the escape sequence"
        instruction_surface = self.font_small.render(instruction_text, True, GRAY)
        self.screen.blit(instruction_surface, (50, SCREEN_HEIGHT - 50))
    
    def draw_room1_binary(self):
        self.screen.fill(DARK_GRAY)
        
        # Room title
        title_text = "ROOM 1: BINARY DECODER"
        title_surface = self.font_large.render(title_text, True, CYAN)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Puzzle description
        desc_lines = [
            "SYSTEM MESSAGE: Decode the binary message to proceed",
            "The message contains a cry for help from the previous user",
            "",
            "Binary Code:",
            self.binary_code,
            "",
            "Enter the decoded message:"
        ]
        
        for i, line in enumerate(desc_lines):
            color = WHITE
            if "Binary Code:" in line:
                color = YELLOW
            elif line == self.binary_code:
                color = GREEN
            
            text_surface = self.font_medium.render(line, True, color)
            self.screen.blit(text_surface, (100, 120 + i * 30))
        
        # Input field
        input_text = "Decoded: " + self.binary_input + "_"
        input_surface = self.font_medium.render(input_text, True, WHITE)
        self.screen.blit(input_surface, (100, 350))
        
        # Hint
        if self.hints_used == 0:
            hint_text = "HINT: Each 8-bit sequence represents one ASCII character (Press H for hint)"
            hint_surface = self.font_small.render(hint_text, True, GRAY)
            self.screen.blit(hint_surface, (100, 400))
        
        # Progress
        progress_text = f"Puzzles Solved: {len(self.puzzles_solved)}/3"
        progress_surface = self.font_small.render(progress_text, True, BLUE)
        self.screen.blit(progress_surface, (100, SCREEN_HEIGHT - 50))
    
    def draw_room2_network(self):
        self.screen.fill(DARK_GRAY)
        
        # Room title
        title_text = "ROOM 2: NETWORK ROUTING"
        title_surface = self.font_large.render(title_text, True, CYAN)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Description
        desc_text = "Route data packets from START to END avoiding firewalls (red blocks)"
        desc_surface = self.font_medium.render(desc_text, True, WHITE)
        self.screen.blit(desc_surface, (100, 100))
        
        # Draw network grid
        grid_start_x = 200
        grid_start_y = 150
        cell_size = 60
        
        for y in range(5):
            for x in range(5):
                rect_x = grid_start_x + x * cell_size
                rect_y = grid_start_y + y * cell_size
                
                # Determine cell color
                if (x, y) == self.network_start:
                    color = GREEN  # Start
                elif (x, y) == self.network_end:
                    color = BLUE   # End
                elif self.network_grid[y][x] == 1:
                    color = RED    # Obstacle/Firewall
                elif (x, y) in self.network_path:
                    color = YELLOW # Path
                else:
                    color = WHITE  # Free space
                
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, cell_size-2, cell_size-2))
                pygame.draw.rect(self.screen, BLACK, (rect_x, rect_y, cell_size-2, cell_size-2), 2)
                
                # Labels
                if (x, y) == self.network_start:
                    label = "S"
                elif (x, y) == self.network_end:
                    label = "E"
                elif self.network_grid[y][x] == 1:
                    label = "X"
                else:
                    label = ""
                
                if label:
                    label_surface = self.font_medium.render(label, True, BLACK)
                    label_rect = label_surface.get_rect(center=(rect_x + cell_size//2, rect_y + cell_size//2))
                    self.screen.blit(label_surface, label_rect)
        
        # Instructions
        instruction_lines = [
            "Click on cells to create a path from START (S) to END (E)",
            "Avoid red firewall blocks (X)",
            "Right-click to clear path and start over"
        ]
        
        for i, line in enumerate(instruction_lines):
            text_surface = self.font_small.render(line, True, WHITE)
            self.screen.blit(text_surface, (100, 500 + i * 20))
        
        # Check if path is valid
        if self.is_valid_path():
            success_text = "Valid path found! Press ENTER to proceed."
            success_surface = self.font_medium.render(success_text, True, GREEN)
            self.screen.blit(success_surface, (100, 580))
    
    def draw_room3_password(self):
        self.screen.fill(DARK_GRAY)
        
        # Room title
        title_text = "ROOM 3: PASSWORD AUTHENTICATION"
        title_surface = self.font_large.render(title_text, True, CYAN)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Description
        desc_text = "Final security layer: Crack the admin password using the clues"
        desc_surface = self.font_medium.render(desc_text, True, WHITE)
        self.screen.blit(desc_surface, (100, 100))
        
        # Password clues
        clue_title = "RECOVERED DATA FRAGMENTS:"
        clue_title_surface = self.font_medium.render(clue_title, True, YELLOW)
        self.screen.blit(clue_title_surface, (100, 150))
        
        clues = [
            "Personal file: 'My first pet was a tiger named Regit'",
            "Calendar entry: 'Born in 1995, lucky number is 28'",
            "Note: 'Grew up on Elm Street, apartment #7'"
        ]
        
        for i, clue in enumerate(clues):
            clue_surface = self.font_small.render(clue, True, WHITE)
            self.screen.blit(clue_surface, (120, 180 + i * 25))
        
        # Password input
        input_y = 300
        input_label = "ADMIN PASSWORD: "
        input_text = input_label + "*" * len(self.password_input) + "_"
        input_surface = self.font_medium.render(input_text, True, GREEN)
        self.screen.blit(input_surface, (100, input_y))
        
        # Actual input (for debugging - remove in production)
        debug_text = f"Debug: {self.password_input}"
        debug_surface = self.font_small.render(debug_text, True, GRAY)
        self.screen.blit(debug_surface, (100, input_y + 30))
        
        # Hint
        hint_text = "HINT: Look for patterns in the personal information"
        hint_surface = self.font_small.render(hint_text, True, GRAY)
        self.screen.blit(hint_surface, (100, 400))
        
        # Instructions
        instruction_text = "Type the password and press ENTER"
        instruction_surface = self.font_small.render(instruction_text, True, WHITE)
        self.screen.blit(instruction_surface, (100, 450))
    
    def draw_victory(self):
        self.screen.fill(BLACK)
        
        # Victory message
        victory_lines = [
            "SYSTEM BREACH SUCCESSFUL",
            "ESCAPE PROTOCOL COMPLETED",
            "",
            "CONGRATULATIONS!",
            "You have successfully escaped the digital prison.",
            "",
            f"Time taken: {int(time.time() - self.time_start)} seconds",
            f"Hints used: {self.hints_used}",
            f"Puzzles solved: {len(self.puzzles_solved)}/3",
            "",
            "SYSTEM SHUTTING DOWN...",
            "",
            "Press R to restart or ESC to quit"
        ]
        
        for i, line in enumerate(victory_lines):
            color = GREEN
            if "CONGRATULATIONS" in line:
                color = YELLOW
            elif "SYSTEM" in line:
                color = CYAN
            elif line.startswith("Time") or line.startswith("Hints") or line.startswith("Puzzles"):
                color = WHITE
            
            text_surface = self.font_medium.render(line, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, 100 + i * 30))
            self.screen.blit(text_surface, text_rect)
    
    def is_valid_path(self):
        """Check if the network path is valid"""
        if not self.network_path:
            return False
        
        # Check if path starts at start and ends at end
        if self.network_path[0] != self.network_start or self.network_path[-1] != self.network_end:
            return False
        
        # Check if path is continuous and doesn't go through obstacles
        for i in range(len(self.network_path) - 1):
            current = self.network_path[i]
            next_pos = self.network_path[i + 1]
            
            # Check if next position is adjacent
            dx = abs(current[0] - next_pos[0])
            dy = abs(current[1] - next_pos[1])
            if dx + dy != 1:  # Not adjacent
                return False
            
            # Check if next position is not an obstacle
            if self.network_grid[next_pos[1]][next_pos[0]] == 1:
                return False
        
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_state == "intro":
                    if event.key == pygame.K_RETURN:
                        if self.terminal_input.lower() == "start":
                            self.game_state = "room1"
                        elif self.terminal_input.lower() == "help":
                            self.terminal_lines.append("Available commands: start, help")
                        self.terminal_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.terminal_input = self.terminal_input[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.terminal_input += event.unicode
                
                elif self.game_state == "room1":
                    if event.key == pygame.K_RETURN:
                        if self.binary_input.upper() == "HELP":
                            self.puzzles_solved.append("binary")
                            self.game_state = "room2"
                        else:
                            # Wrong answer feedback
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        self.binary_input = self.binary_input[:-1]
                    elif event.key == pygame.K_h:
                        self.hints_used += 1
                        # Show binary to ASCII conversion hint
                    else:
                        if event.unicode.isalpha():
                            self.binary_input += event.unicode.upper()
                
                elif self.game_state == "room2":
                    if event.key == pygame.K_RETURN:
                        if self.is_valid_path():
                            self.puzzles_solved.append("network")
                            self.game_state = "room3"
                
                elif self.game_state == "room3":
                    if event.key == pygame.K_RETURN:
                        if self.password_input.upper() == self.correct_password:
                            self.puzzles_solved.append("password")
                            self.game_state = "victory"
                    elif event.key == pygame.K_BACKSPACE:
                        self.password_input = self.password_input[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.password_input += event.unicode.upper()
                
                elif self.game_state == "victory":
                    if event.key == pygame.K_r:
                        self.restart_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "room2":
                # Handle network grid clicking
                mouse_x, mouse_y = event.pos
                grid_start_x = 200
                grid_start_y = 150
                cell_size = 60
                
                # Calculate grid position
                grid_x = (mouse_x - grid_start_x) // cell_size
                grid_y = (mouse_y - grid_start_y) // cell_size
                
                if 0 <= grid_x < 5 and 0 <= grid_y < 5:
                    pos = (grid_x, grid_y)
                    
                    if event.button == 1:  # Left click
                        if self.network_grid[grid_y][grid_x] == 0:  # Not an obstacle
                            if pos not in self.network_path:
                                self.network_path.append(pos)
                    elif event.button == 3:  # Right click
                        self.network_path = []  # Clear path
        
        return True
    
    def restart_game(self):
        self.game_state = "intro"
        self.puzzles_solved = []
        self.binary_input = ""
        self.network_path = []
        self.password_input = ""
        self.terminal_input = ""
        self.time_start = time.time()
        self.hints_used = 0
    
    def draw(self):
        if self.game_state == "intro":
            self.draw_intro()
        elif self.game_state == "room1":
            self.draw_room1_binary()
        elif self.game_state == "room2":
            self.draw_room2_network()
        elif self.game_state == "room3":
            self.draw_room3_password()
        elif self.game_state == "victory":
            self.draw_victory()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Escape404()
    game.run()
