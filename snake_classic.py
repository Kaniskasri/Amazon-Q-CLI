#!/usr/bin/env python3
"""
Snake Classic - Classic snake game with modern twists
"""

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Game settings
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 100) // GRID_SIZE  # Leave space for UI

class SnakeClassic:
    def __init__(self):
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Snake Classic")
            self.clock = pygame.time.Clock()
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            
            self.game_state = "menu"  # menu, playing, paused, game_over
            self.difficulty = "Normal"  # Easy, Normal, Hard, Extreme
            self.game_mode = "Classic"  # Classic, Arcade, Survival
            
            # Snake properties
            self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            self.direction = (1, 0)  # Moving right initially
            self.next_direction = (1, 0)
            
            # Food and power-ups
            self.food = self.generate_food()
            self.special_food = None
            self.special_food_timer = 0
            
            # Game stats
            self.score = 0
            self.high_score = 0
            self.level = 1
            self.speed = 8  # FPS for snake movement
            self.lives = 3
            
            # Special effects
            self.invincible = False
            self.invincible_timer = 0
            self.slow_motion = False
            self.slow_motion_timer = 0
            self.double_points = False
            self.double_points_timer = 0
            
            # Obstacles (for advanced modes)
            self.obstacles = []
            
            # Animation and timing
            self.animation_time = 0
            self.last_move_time = 0
            self.move_delay = 1000 // self.speed  # milliseconds between moves
            
            self.setup_difficulty()
            
        except Exception as e:
            print(f"Error initializing Snake game: {e}")
            sys.exit(1)
    
    def setup_difficulty(self):
        """Set up game parameters based on difficulty"""
        try:
            difficulty_settings = {
                "Easy": {"speed": 6, "obstacles": False, "power_ups": True},
                "Normal": {"speed": 8, "obstacles": False, "power_ups": True},
                "Hard": {"speed": 12, "obstacles": True, "power_ups": True},
                "Extreme": {"speed": 16, "obstacles": True, "power_ups": False}
            }
            
            settings = difficulty_settings.get(self.difficulty, difficulty_settings["Normal"])
            self.speed = settings["speed"]
            self.move_delay = 1000 // self.speed
            
            if settings["obstacles"] and self.game_mode != "Classic":
                self.generate_obstacles()
            else:
                self.obstacles = []
        except Exception as e:
            print(f"Error setting up difficulty: {e}")
            # Use default settings
            self.speed = 8
            self.move_delay = 125
            self.obstacles = []
    
    def generate_food(self):
        """Generate food at random position"""
        try:
            max_attempts = 100  # Prevent infinite loop
            attempts = 0
            
            while attempts < max_attempts:
                food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if (food_pos not in self.snake and 
                    food_pos not in self.obstacles and
                    (not self.special_food or food_pos != self.special_food)):
                    return food_pos
                attempts += 1
            
            # Fallback: return a position that's not in the snake
            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    pos = (x, y)
                    if pos not in self.snake:
                        return pos
            
            # Ultimate fallback
            return (0, 0)
            
        except Exception as e:
            print(f"Error generating food: {e}")
            return (5, 5)  # Safe fallback position
    
    def generate_special_food(self):
        """Generate special food with power-up effects"""
        try:
            if random.random() < 0.3:  # 30% chance
                max_attempts = 50
                attempts = 0
                
                while attempts < max_attempts:
                    special_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                    if (special_pos not in self.snake and 
                        special_pos not in self.obstacles and
                        special_pos != self.food):
                        return special_pos
                    attempts += 1
            return None
        except Exception as e:
            print(f"Error generating special food: {e}")
            return None
    
    def generate_obstacles(self):
        """Generate obstacles for harder difficulties"""
        try:
            self.obstacles = []
            num_obstacles = min(5, max(1, self.level))
            
            for _ in range(num_obstacles):
                max_attempts = 50
                attempts = 0
                
                while attempts < max_attempts:
                    obstacle_pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
                    if (obstacle_pos not in self.snake and 
                        obstacle_pos != self.food and
                        obstacle_pos not in self.obstacles):
                        self.obstacles.append(obstacle_pos)
                        break
                    attempts += 1
        except Exception as e:
            print(f"Error generating obstacles: {e}")
            self.obstacles = []
    
    def move_snake(self):
        """Move the snake and handle collisions"""
        try:
            # Update direction
            self.direction = self.next_direction
            
            # Calculate new head position
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            # Check wall collisions
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                if not self.invincible:
                    self.game_over()
                    return
                else:
                    # Wrap around when invincible
                    new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
            
            # Check self collision
            if new_head in self.snake and not self.invincible:
                self.game_over()
                return
            
            # Check obstacle collision
            if new_head in self.obstacles and not self.invincible:
                self.game_over()
                return
            
            # Add new head
            self.snake.insert(0, new_head)
            
            # Check food collision
            food_eaten = False
            if new_head == self.food:
                food_eaten = True
                points = 10
                if self.double_points:
                    points *= 2
                self.score += points
                self.food = self.generate_food()
                
                # Level up every 100 points
                new_level = (self.score // 100) + 1
                if new_level > self.level:
                    self.level = new_level
                    self.speed = min(20, self.speed + 1)  # Increase speed
                    self.move_delay = 1000 // self.speed
                    if self.difficulty in ["Hard", "Extreme"]:
                        self.generate_obstacles()
            
            # Check special food collision
            if self.special_food and new_head == self.special_food:
                food_eaten = True
                self.activate_power_up()
                self.special_food = None
                self.special_food_timer = 0
            
            # Remove tail if no food eaten
            if not food_eaten:
                self.snake.pop()
                
        except Exception as e:
            print(f"Error moving snake: {e}")
            self.game_over()
    
    def activate_power_up(self):
        """Activate a random power-up effect"""
        try:
            power_ups = ["invincible", "slow_motion", "double_points", "extra_life"]
            power_up = random.choice(power_ups)
            
            if power_up == "invincible":
                self.invincible = True
                self.invincible_timer = 300  # 5 seconds at 60 FPS
            elif power_up == "slow_motion":
                self.slow_motion = True
                self.slow_motion_timer = 300
            elif power_up == "double_points":
                self.double_points = True
                self.double_points_timer = 600  # 10 seconds
            elif power_up == "extra_life":
                self.lives += 1
            
            # Add score bonus
            bonus = 50
            if self.double_points:
                bonus *= 2
            self.score += bonus
            
        except Exception as e:
            print(f"Error activating power-up: {e}")
    
    def update_power_ups(self):
        """Update power-up timers"""
        try:
            if self.invincible_timer > 0:
                self.invincible_timer -= 1
                if self.invincible_timer <= 0:
                    self.invincible = False
            
            if self.slow_motion_timer > 0:
                self.slow_motion_timer -= 1
                if self.slow_motion_timer <= 0:
                    self.slow_motion = False
            
            if self.double_points_timer > 0:
                self.double_points_timer -= 1
                if self.double_points_timer <= 0:
                    self.double_points = False
            
            # Special food timer
            if not self.special_food:
                self.special_food_timer += 1
                if self.special_food_timer > 600:  # 10 seconds
                    self.special_food = self.generate_special_food()
                    self.special_food_timer = 0
                    
        except Exception as e:
            print(f"Error updating power-ups: {e}")
    
    def game_over(self):
        """Handle game over"""
        try:
            self.lives -= 1
            if self.lives <= 0:
                if self.score > self.high_score:
                    self.high_score = self.score
                self.game_state = "game_over"
            else:
                # Reset snake position but keep score
                self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                self.direction = (1, 0)
                self.next_direction = (1, 0)
                self.invincible = True
                self.invincible_timer = 180  # 3 seconds of invincibility
        except Exception as e:
            print(f"Error in game over: {e}")
            self.game_state = "game_over"
    
    def draw_grid_object(self, pos, color, special_effect=None):
        """Draw an object on the grid"""
        try:
            x, y = pos
            # Ensure coordinates are within bounds
            if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                return
                
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE - 1, GRID_SIZE - 1)
            
            if special_effect == "pulse":
                # Pulsing effect
                pulse = abs(math.sin(self.animation_time * 0.1)) * 0.3 + 0.7
                adjusted_color = tuple(int(min(255, max(0, c * pulse))) for c in color)
                pygame.draw.rect(self.screen, adjusted_color, rect)
            elif special_effect == "glow":
                # Glowing effect
                for i in range(3):
                    if rect.width > i * 2 and rect.height > i * 2:
                        glow_rect = rect.inflate(i * 2, i * 2)
                        glow_color = tuple(max(0, min(255, c - i * 50)) for c in color)
                        pygame.draw.rect(self.screen, glow_color, glow_rect)
            else:
                pygame.draw.rect(self.screen, color, rect)
            
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            
        except Exception as e:
            print(f"Error drawing grid object: {e}")
    
    def draw_menu(self):
        """Draw the main menu"""
        try:
            self.screen.fill(BLACK)
            
            # Title with snake-like animation
            title_text = "SNAKE CLASSIC"
            title_surface = self.font_large.render(title_text, True, GREEN)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title_surface, title_rect)
            
            # Animated snake
            snake_y = 150
            for i in range(8):
                try:
                    x = 200 + i * 25 + int(math.sin(self.animation_time * 0.1 + i * 0.5) * 10)
                    color = GREEN if i == 0 else DARK_GREEN
                    pygame.draw.rect(self.screen, color, (x, snake_y, 20, 20))
                    pygame.draw.rect(self.screen, BLACK, (x, snake_y, 20, 20), 1)
                except:
                    pass  # Skip if drawing fails
            
            # Menu options
            menu_y = 250
            options = [
                f"Difficulty: {self.difficulty}",
                f"Mode: {self.game_mode}",
                f"High Score: {self.high_score}",
                "",
                "Controls:",
                "Arrow Keys - Move",
                "SPACE - Pause",
                "ESC - Quit"
            ]
            
            for i, option in enumerate(options):
                try:
                    color = WHITE
                    if option.startswith("Difficulty:") or option.startswith("Mode:"):
                        color = YELLOW
                    elif option.startswith("High Score:"):
                        color = GREEN
                    elif option.startswith("Controls:"):
                        color = BLUE
                    
                    text_surface = self.font_small.render(option, True, color)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, menu_y + i * 30))
                    self.screen.blit(text_surface, text_rect)
                except:
                    pass  # Skip if rendering fails
            
            # Instructions
            instruction_lines = [
                "Press D to change difficulty",
                "Press M to change mode", 
                "Press ENTER to start game"
            ]
            
            for i, instruction in enumerate(instruction_lines):
                try:
                    text_surface = self.font_small.render(instruction, True, GRAY)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, 500 + i * 25))
                    self.screen.blit(text_surface, text_rect)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error drawing menu: {e}")
    
    def draw_playing(self):
        """Draw the game during play"""
        try:
            self.screen.fill(BLACK)
            
            # Draw UI background
            pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 100))
            
            # Score and stats
            score_text = f"Score: {self.score}"
            level_text = f"Level: {self.level}"
            lives_text = f"Lives: {self.lives}"
            
            score_surface = self.font_medium.render(score_text, True, WHITE)
            level_surface = self.font_medium.render(level_text, True, WHITE)
            lives_surface = self.font_medium.render(lives_text, True, WHITE)
            
            self.screen.blit(score_surface, (20, 20))
            self.screen.blit(level_surface, (20, 50))
            self.screen.blit(lives_surface, (200, 20))
            
            # Power-up indicators
            power_up_x = 400
            if self.invincible:
                invincible_text = f"INVINCIBLE: {max(0, self.invincible_timer // 60)}s"
                invincible_surface = self.font_small.render(invincible_text, True, YELLOW)
                self.screen.blit(invincible_surface, (power_up_x, 20))
            
            if self.slow_motion:
                slow_text = f"SLOW-MO: {max(0, self.slow_motion_timer // 60)}s"
                slow_surface = self.font_small.render(slow_text, True, BLUE)
                self.screen.blit(slow_surface, (power_up_x, 40))
            
            if self.double_points:
                double_text = f"2X POINTS: {max(0, self.double_points_timer // 60)}s"
                double_surface = self.font_small.render(double_text, True, GREEN)
                self.screen.blit(double_surface, (power_up_x, 60))
            
            # Draw game area border
            game_area = pygame.Rect(0, 100, SCREEN_WIDTH, SCREEN_HEIGHT - 100)
            pygame.draw.rect(self.screen, WHITE, game_area, 2)
            
            # Draw obstacles
            for obstacle in self.obstacles:
                self.draw_grid_object(obstacle, GRAY)
            
            # Draw food
            if self.food:
                self.draw_grid_object(self.food, RED, "pulse")
            
            # Draw special food
            if self.special_food:
                self.draw_grid_object(self.special_food, PURPLE, "glow")
            
            # Draw snake
            for i, segment in enumerate(self.snake):
                if i == 0:  # Head
                    color = YELLOW if self.invincible else GREEN
                    self.draw_grid_object(segment, color)
                    # Draw eyes
                    try:
                        x, y = segment
                        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                            eye_size = 2
                            eye1_pos = (x * GRID_SIZE + 5, y * GRID_SIZE + 105)
                            eye2_pos = (x * GRID_SIZE + 15, y * GRID_SIZE + 105)
                            pygame.draw.circle(self.screen, BLACK, eye1_pos, eye_size)
                            pygame.draw.circle(self.screen, BLACK, eye2_pos, eye_size)
                    except:
                        pass
                else:  # Body
                    color = ORANGE if self.invincible else DARK_GREEN
                    self.draw_grid_object(segment, color)
                    
        except Exception as e:
            print(f"Error drawing game: {e}")
    
    def draw_paused(self):
        """Draw pause screen"""
        try:
            # Draw the game state first
            self.draw_playing()
            
            # Draw pause overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Pause text
            pause_text = "PAUSED"
            pause_surface = self.font_large.render(pause_text, True, WHITE)
            pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_surface, pause_rect)
            
            instruction_text = "Press SPACE to resume"
            instruction_surface = self.font_medium.render(instruction_text, True, GRAY)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(instruction_surface, instruction_rect)
            
        except Exception as e:
            print(f"Error drawing pause screen: {e}")
    
    def draw_game_over(self):
        """Draw game over screen"""
        try:
            self.screen.fill(BLACK)
            
            # Game Over text
            game_over_text = "GAME OVER"
            game_over_surface = self.font_large.render(game_over_text, True, RED)
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(game_over_surface, game_over_rect)
            
            # Final stats
            stats = [
                f"Final Score: {self.score}",
                f"High Score: {self.high_score}",
                f"Level Reached: {self.level}",
                f"Snake Length: {len(self.snake)}"
            ]
            
            for i, stat in enumerate(stats):
                color = GREEN if "High Score" in stat else WHITE
                stat_surface = self.font_medium.render(stat, True, color)
                stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH//2, 280 + i * 40))
                self.screen.blit(stat_surface, stat_rect)
            
            # Performance rating
            if self.score >= 500:
                rating = "Snake Master!"
            elif self.score >= 300:
                rating = "Excellent!"
            elif self.score >= 150:
                rating = "Good Job!"
            elif self.score >= 50:
                rating = "Not Bad!"
            else:
                rating = "Keep Trying!"
            
            rating_surface = self.font_medium.render(rating, True, YELLOW)
            rating_rect = rating_surface.get_rect(center=(SCREEN_WIDTH//2, 450))
            self.screen.blit(rating_surface, rating_rect)
            
            # Restart options
            restart_text = "Press R to restart or ESC to quit"
            restart_surface = self.font_small.render(restart_text, True, GRAY)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, 520))
            self.screen.blit(restart_surface, restart_rect)
            
        except Exception as e:
            print(f"Error drawing game over screen: {e}")
    
    def handle_events(self):
        """Handle pygame events"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif self.game_state == "menu":
                        if event.key == pygame.K_RETURN:
                            self.start_game()
                        elif event.key == pygame.K_d:
                            self.cycle_difficulty()
                        elif event.key == pygame.K_m:
                            self.cycle_mode()
                    elif self.game_state == "playing":
                        if event.key == pygame.K_SPACE:
                            self.game_state = "paused"
                        elif event.key == pygame.K_UP and self.direction != (0, 1):
                            self.next_direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.next_direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.next_direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.next_direction = (1, 0)
                    elif self.game_state == "paused":
                        if event.key == pygame.K_SPACE:
                            self.game_state = "playing"
                    elif self.game_state == "game_over":
                        if event.key == pygame.K_r:
                            self.restart_game()
            return True
        except Exception as e:
            print(f"Error handling events: {e}")
            return True
    
    def cycle_difficulty(self):
        """Cycle through difficulty levels"""
        try:
            difficulties = ["Easy", "Normal", "Hard", "Extreme"]
            current_index = difficulties.index(self.difficulty)
            self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
            self.setup_difficulty()
        except Exception as e:
            print(f"Error cycling difficulty: {e}")
    
    def cycle_mode(self):
        """Cycle through game modes"""
        try:
            modes = ["Classic", "Arcade", "Survival"]
            current_index = modes.index(self.game_mode)
            self.game_mode = modes[(current_index + 1) % len(modes)]
            
            # Adjust lives based on mode
            if self.game_mode == "Classic":
                self.lives = 3
            elif self.game_mode == "Arcade":
                self.lives = 5
            elif self.game_mode == "Survival":
                self.lives = 1
        except Exception as e:
            print(f"Error cycling mode: {e}")
    
    def start_game(self):
        """Start a new game"""
        try:
            self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            self.direction = (1, 0)
            self.next_direction = (1, 0)
            self.food = self.generate_food()
            self.special_food = None
            self.special_food_timer = 0
            self.score = 0
            self.level = 1
            self.last_move_time = pygame.time.get_ticks()
            
            # Set lives based on mode
            if self.game_mode == "Classic":
                self.lives = 3
            elif self.game_mode == "Arcade":
                self.lives = 5
            elif self.game_mode == "Survival":
                self.lives = 1
            
            # Reset power-ups
            self.invincible = False
            self.invincible_timer = 0
            self.slow_motion = False
            self.slow_motion_timer = 0
            self.double_points = False
            self.double_points_timer = 0
            
            self.setup_difficulty()
            self.game_state = "playing"
            
        except Exception as e:
            print(f"Error starting game: {e}")
    
    def restart_game(self):
        """Restart game from menu"""
        self.game_state = "menu"
    
    def update(self):
        """Update game state"""
        try:
            self.animation_time += 1
            
            if self.game_state == "playing":
                self.update_power_ups()
                
                # Move snake based on timing
                current_time = pygame.time.get_ticks()
                move_delay = self.move_delay
                
                if self.slow_motion:
                    move_delay *= 2  # Double the delay for slow motion
                
                if current_time - self.last_move_time >= move_delay:
                    self.move_snake()
                    self.last_move_time = current_time
                    
        except Exception as e:
            print(f"Error updating game: {e}")
    
    def draw(self):
        """Draw the current game state"""
        try:
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "playing":
                self.draw_playing()
            elif self.game_state == "paused":
                self.draw_paused()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error drawing: {e}")
    
    def run(self):
        """Main game loop"""
        try:
            running = True
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
            
            pygame.quit()
            
        except Exception as e:
            print(f"Error in main game loop: {e}")
            pygame.quit()

if __name__ == "__main__":
    try:
        game = SnakeClassic()
        game.run()
    except Exception as e:
        print(f"Failed to start Snake Classic: {e}")
        sys.exit(1)
