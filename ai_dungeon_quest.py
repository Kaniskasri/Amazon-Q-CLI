#!/usr/bin/env python3
"""
AI Dungeon Quest - Text-based adventure game with branching choices
"""

import pygame
import sys
import textwrap

pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (230, 230, 230)

class AIDungeonQuest:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Dungeon Quest")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        self.current_scene = "start"
        self.selected_choice = 0
        self.game_over = False
        self.inventory = []
        self.health = 100
        self.score = 0
        
        # Game story data
        self.scenes = {
            "start": {
                "text": "You wake up in a mysterious forest clearing. Ancient ruins loom ahead, partially covered by twisted vines. A strange blue glow emanates from within the ruins. You hear distant howling in the darkness behind you.",
                "choices": [
                    ("Enter the glowing ruins", "ruins_entrance"),
                    ("Investigate the howling sounds", "forest_path"),
                    ("Search the clearing for supplies", "clearing_search")
                ]
            },
            "ruins_entrance": {
                "text": "The ruins are filled with ancient technology humming with energy. Holographic symbols float in the air. You see three passages: one leads down into darkness, another glows with warm light, and the third crackles with electrical energy.",
                "choices": [
                    ("Descend into the dark passage", "dark_passage"),
                    ("Follow the warm, glowing passage", "light_passage"),
                    ("Enter the electrical passage", "electric_passage")
                ]
            },
            "forest_path": {
                "text": "Following the howls, you discover a pack of robotic wolves with glowing red eyes. They seem to be guarding something. Behind them, you spot a crashed spaceship with its cargo bay open.",
                "choices": [
                    ("Try to sneak past the robot wolves", "sneak_attempt"),
                    ("Attempt to communicate with them", "communicate_wolves"),
                    ("Look for another way around", "alternate_route")
                ]
            },
            "clearing_search": {
                "text": "Searching the clearing, you find an old backpack containing a energy scanner, some rations, and a mysterious crystal that pulses with inner light. The scanner beeps, detecting multiple energy signatures nearby.",
                "choices": [
                    ("Use the scanner to track the strongest signal", "scanner_track"),
                    ("Examine the crystal more closely", "crystal_examine"),
                    ("Head toward the ruins with your new equipment", "equipped_ruins")
                ]
            },
            "dark_passage": {
                "text": "The passage leads to an underground chamber filled with sleeping pods. Most are empty, but one contains a figure in a strange suit. A control panel nearby shows various readings. Suddenly, alarms start blaring!",
                "choices": [
                    ("Try to wake the figure in the pod", "wake_figure"),
                    ("Examine the control panel", "control_panel"),
                    ("Flee back to the surface", "flee_surface")
                ]
            },
            "light_passage": {
                "text": "You enter a beautiful garden chamber with bioluminescent plants and a clear pool of water. An AI hologram appears, speaking in an ancient language. It gestures toward three glowing orbs on pedestals.",
                "choices": [
                    ("Touch the blue orb", "blue_orb"),
                    ("Touch the green orb", "green_orb"),
                    ("Try to communicate with the AI", "ai_communicate")
                ]
            },
            "electric_passage": {
                "text": "The electrical energy courses through your body, but instead of harm, it grants you enhanced abilities! You can now interface with the ancient technology. A massive door opens, revealing a control room.",
                "choices": [
                    ("Access the main computer", "main_computer"),
                    ("Check the security systems", "security_systems"),
                    ("Look for the power source", "power_source")
                ]
            },
            "main_computer": {
                "text": "The computer reveals this is an ancient research station studying interdimensional travel. A portal is nearly complete, but it needs a power crystal to activate. You realize the crystal from the clearing might work!",
                "choices": [
                    ("Activate the portal (if you have crystal)", "portal_activate"),
                    ("Study the research data first", "research_data"),
                    ("Look for alternative power sources", "alt_power")
                ]
            },
            "portal_activate": {
                "text": "The portal springs to life! You can see three different dimensions through swirling energy: a peaceful world of floating islands, a high-tech cyberpunk city, and a realm of pure energy beings.",
                "choices": [
                    ("Enter the floating islands dimension", "floating_islands"),
                    ("Step into the cyberpunk city", "cyberpunk_city"),
                    ("Merge with the energy beings", "energy_beings")
                ]
            },
            "floating_islands": {
                "text": "You emerge on a beautiful floating island where friendly beings welcome you as a prophesied traveler. They offer to teach you their ancient wisdom and make you a guardian of their realm.",
                "choices": [
                    ("Accept their offer and stay", "peaceful_ending"),
                    ("Ask to return home with their knowledge", "wisdom_return"),
                    ("Request to explore more dimensions", "dimension_explorer")
                ]
            },
            "peaceful_ending": {
                "text": "You become a guardian of the floating islands, spending your days learning ancient wisdom and protecting this peaceful realm. Your adventure ends in harmony and enlightenment. VICTORY!",
                "choices": [("Play again", "start")]
            }
        }
        
        # Add inventory tracking
        if self.current_scene == "clearing_search":
            self.inventory.extend(["Energy Scanner", "Rations", "Crystal"])
    
    def get_current_scene(self):
        return self.scenes.get(self.current_scene, self.scenes["start"])
    
    def draw_game(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("AI Dungeon Quest", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Status bar
        status_y = 70
        health_text = f"Health: {self.health}"
        score_text = f"Score: {self.score}"
        inventory_text = f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}"
        
        health_surface = self.font_small.render(health_text, True, RED if self.health < 50 else BLACK)
        score_surface = self.font_small.render(score_text, True, BLACK)
        inventory_surface = self.font_small.render(inventory_text, True, GRAY)
        
        self.screen.blit(health_surface, (20, status_y))
        self.screen.blit(score_surface, (150, status_y))
        self.screen.blit(inventory_surface, (20, status_y + 25))
        
        # Main story text
        scene = self.get_current_scene()
        story_y = 120
        
        # Wrap text to fit screen
        wrapped_text = textwrap.wrap(scene["text"], width=80)
        for i, line in enumerate(wrapped_text):
            text_surface = self.font_medium.render(line, True, BLACK)
            self.screen.blit(text_surface, (50, story_y + i * 30))
        
        # Choices
        choices_y = story_y + len(wrapped_text) * 30 + 50
        choice_text = self.font_medium.render("Choose your action:", True, BLUE)
        self.screen.blit(choice_text, (50, choices_y))
        
        for i, (choice_text, _) in enumerate(scene["choices"]):
            y_pos = choices_y + 40 + i * 40
            
            # Highlight selected choice
            if i == self.selected_choice:
                pygame.draw.rect(self.screen, LIGHT_GRAY, (40, y_pos - 5, SCREEN_WIDTH - 80, 35))
            
            choice_num = f"{i + 1}. {choice_text}"
            choice_surface = self.font_medium.render(choice_num, True, BLACK)
            self.screen.blit(choice_surface, (50, y_pos))
        
        # Instructions
        instruction_text = "Use UP/DOWN arrows to select, ENTER to choose, ESC to quit"
        instruction_surface = self.font_small.render(instruction_text, True, GRAY)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_surface, instruction_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP:
                    scene = self.get_current_scene()
                    self.selected_choice = (self.selected_choice - 1) % len(scene["choices"])
                elif event.key == pygame.K_DOWN:
                    scene = self.get_current_scene()
                    self.selected_choice = (self.selected_choice + 1) % len(scene["choices"])
                elif event.key == pygame.K_RETURN:
                    self.make_choice()
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    # Direct number selection
                    choice_num = event.key - pygame.K_1
                    scene = self.get_current_scene()
                    if choice_num < len(scene["choices"]):
                        self.selected_choice = choice_num
                        self.make_choice()
        return True
    
    def make_choice(self):
        scene = self.get_current_scene()
        if self.selected_choice < len(scene["choices"]):
            _, next_scene = scene["choices"][self.selected_choice]
            
            # Handle special conditions
            if next_scene == "portal_activate" and "Crystal" not in self.inventory:
                # Can't activate portal without crystal
                return
            
            # Update inventory and stats based on choices
            if self.current_scene == "clearing_search":
                self.inventory.extend(["Energy Scanner", "Rations", "Crystal"])
                self.score += 10
            elif self.current_scene == "electric_passage":
                self.score += 20
            elif next_scene == "peaceful_ending":
                self.score += 100
            
            self.current_scene = next_scene
            self.selected_choice = 0
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw_game()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = AIDungeonQuest()
    game.run()
