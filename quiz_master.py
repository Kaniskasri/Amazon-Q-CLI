#!/usr/bin/env python3
"""
Quiz Master - Test your knowledge with trivia questions
"""

import pygame
import random
import sys
import textwrap

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
ORANGE = (255, 165, 0)

class QuizMaster:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quiz Master")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.game_state = "menu"  # menu, playing, result, game_over
        self.current_question = 0
        self.selected_answer = 0
        self.score = 0
        self.total_questions = 10
        self.time_limit = 30  # seconds per question
        self.time_remaining = self.time_limit
        self.question_start_time = 0
        
        # Question categories
        self.categories = ["General", "Science", "History", "Geography", "Technology", "Sports", "Arts"]
        self.current_category = "Mixed"
        
        # Quiz questions database
        self.questions = [
            # General Knowledge
            {
                "category": "General",
                "question": "What is the largest planet in our solar system?",
                "answers": ["Earth", "Jupiter", "Saturn", "Neptune"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "General",
                "question": "Which element has the chemical symbol 'O'?",
                "answers": ["Gold", "Silver", "Oxygen", "Iron"],
                "correct": 2,
                "difficulty": "Easy"
            },
            {
                "category": "General",
                "question": "What is the capital of Australia?",
                "answers": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "correct": 2,
                "difficulty": "Medium"
            },
            
            # Science
            {
                "category": "Science",
                "question": "What is the speed of light in vacuum?",
                "answers": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "200,000 km/s"],
                "correct": 0,
                "difficulty": "Medium"
            },
            {
                "category": "Science",
                "question": "Which scientist developed the theory of relativity?",
                "answers": ["Newton", "Einstein", "Galileo", "Darwin"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "Science",
                "question": "What is the hardest natural substance on Earth?",
                "answers": ["Gold", "Iron", "Diamond", "Platinum"],
                "correct": 2,
                "difficulty": "Easy"
            },
            
            # History
            {
                "category": "History",
                "question": "In which year did World War II end?",
                "answers": ["1944", "1945", "1946", "1947"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "History",
                "question": "Who was the first person to walk on the moon?",
                "answers": ["Buzz Aldrin", "Neil Armstrong", "John Glenn", "Alan Shepard"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "History",
                "question": "Which ancient wonder of the world was located in Alexandria?",
                "answers": ["Hanging Gardens", "Colossus of Rhodes", "Lighthouse", "Statue of Zeus"],
                "correct": 2,
                "difficulty": "Hard"
            },
            
            # Geography
            {
                "category": "Geography",
                "question": "Which is the longest river in the world?",
                "answers": ["Amazon", "Nile", "Mississippi", "Yangtze"],
                "correct": 1,
                "difficulty": "Medium"
            },
            {
                "category": "Geography",
                "question": "What is the smallest country in the world?",
                "answers": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
                "correct": 1,
                "difficulty": "Medium"
            },
            {
                "category": "Geography",
                "question": "Which mountain range contains Mount Everest?",
                "answers": ["Andes", "Rocky Mountains", "Alps", "Himalayas"],
                "correct": 3,
                "difficulty": "Easy"
            },
            
            # Technology
            {
                "category": "Technology",
                "question": "What does 'HTTP' stand for?",
                "answers": ["HyperText Transfer Protocol", "High Tech Transfer Process", "Home Tool Transfer Protocol", "HyperText Technical Process"],
                "correct": 0,
                "difficulty": "Medium"
            },
            {
                "category": "Technology",
                "question": "Who founded Microsoft?",
                "answers": ["Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Larry Page"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "Technology",
                "question": "What does 'AI' stand for in computing?",
                "answers": ["Advanced Intelligence", "Artificial Intelligence", "Automated Intelligence", "Applied Intelligence"],
                "correct": 1,
                "difficulty": "Easy"
            },
            
            # Sports
            {
                "category": "Sports",
                "question": "How many players are on a basketball team on the court at one time?",
                "answers": ["4", "5", "6", "7"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "Sports",
                "question": "In which sport would you perform a slam dunk?",
                "answers": ["Tennis", "Basketball", "Volleyball", "Baseball"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "Sports",
                "question": "How often are the Summer Olympic Games held?",
                "answers": ["Every 2 years", "Every 3 years", "Every 4 years", "Every 5 years"],
                "correct": 2,
                "difficulty": "Easy"
            },
            
            # Arts
            {
                "category": "Arts",
                "question": "Who painted the Mona Lisa?",
                "answers": ["Picasso", "Van Gogh", "Leonardo da Vinci", "Michelangelo"],
                "correct": 2,
                "difficulty": "Easy"
            },
            {
                "category": "Arts",
                "question": "Which instrument has 88 keys?",
                "answers": ["Organ", "Piano", "Harpsichord", "Accordion"],
                "correct": 1,
                "difficulty": "Easy"
            },
            {
                "category": "Arts",
                "question": "Who wrote the play 'Romeo and Juliet'?",
                "answers": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Oscar Wilde"],
                "correct": 1,
                "difficulty": "Easy"
            }
        ]
        
        self.current_quiz = []
        self.answered_questions = []
        self.lifelines = {"50_50": True, "skip": True}  # Available lifelines
        
    def generate_quiz(self, category="Mixed"):
        """Generate a quiz with questions from specified category"""
        if category == "Mixed":
            available_questions = self.questions.copy()
        else:
            available_questions = [q for q in self.questions if q["category"] == category]
        
        # Ensure we have enough questions
        if len(available_questions) < self.total_questions:
            available_questions = self.questions.copy()
        
        # Randomly select questions
        self.current_quiz = random.sample(available_questions, min(self.total_questions, len(available_questions)))
        self.current_question = 0
        self.score = 0
        self.answered_questions = []
        self.question_start_time = pygame.time.get_ticks()
        self.time_remaining = self.time_limit
    
    def get_current_question(self):
        """Get the current question data"""
        if self.current_question < len(self.current_quiz):
            return self.current_quiz[self.current_question]
        return None
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = "Quiz Master"
        title_surface = self.font_large.render(title_text, True, PURPLE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Test Your Knowledge!"
        subtitle_surface = self.font_medium.render(subtitle_text, True, BLUE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game info
        info_lines = [
            f"• {self.total_questions} questions per quiz",
            f"• {self.time_limit} seconds per question",
            "• Multiple choice answers",
            "• Lifelines available: 50/50 and Skip",
            "• Points based on difficulty and speed"
        ]
        
        for i, line in enumerate(info_lines):
            text_surface = self.font_small.render(line, True, BLACK)
            self.screen.blit(text_surface, (200, 200 + i * 30))
        
        # Category selection
        category_title = "Select Category:"
        category_title_surface = self.font_medium.render(category_title, True, BLUE)
        self.screen.blit(category_title_surface, (200, 350))
        
        categories = ["Mixed"] + self.categories
        for i, category in enumerate(categories):
            y_pos = 390 + (i % 4) * 40
            x_pos = 200 + (i // 4) * 200
            
            color = GREEN if category == self.current_category else BLACK
            category_surface = self.font_small.render(f"{i+1}. {category}", True, color)
            self.screen.blit(category_surface, (x_pos, y_pos))
        
        # Instructions
        instruction_lines = [
            "Press 1-8 to select category",
            "Press SPACE to start quiz",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instruction_lines):
            text_surface = self.font_small.render(instruction, True, GRAY)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, 550 + i * 25))
            self.screen.blit(text_surface, text_rect)
    
    def draw_playing(self):
        self.screen.fill(WHITE)
        
        question_data = self.get_current_question()
        if not question_data:
            return
        
        # Update timer
        elapsed = (pygame.time.get_ticks() - self.question_start_time) / 1000
        self.time_remaining = max(0, self.time_limit - elapsed)
        
        # Header
        header_y = 30
        question_num_text = f"Question {self.current_question + 1}/{len(self.current_quiz)}"
        score_text = f"Score: {self.score}"
        category_text = f"Category: {question_data['category']}"
        difficulty_text = f"Difficulty: {question_data['difficulty']}"
        
        question_num_surface = self.font_medium.render(question_num_text, True, BLUE)
        score_surface = self.font_medium.render(score_text, True, GREEN)
        category_surface = self.font_small.render(category_text, True, PURPLE)
        difficulty_surface = self.font_small.render(difficulty_text, True, ORANGE)
        
        self.screen.blit(question_num_surface, (50, header_y))
        self.screen.blit(score_surface, (SCREEN_WIDTH - 150, header_y))
        self.screen.blit(category_surface, (50, header_y + 30))
        self.screen.blit(difficulty_surface, (SCREEN_WIDTH - 200, header_y + 30))
        
        # Timer
        timer_y = 80
        timer_text = f"Time: {int(self.time_remaining)}s"
        timer_color = RED if self.time_remaining < 10 else BLACK
        timer_surface = self.font_medium.render(timer_text, True, timer_color)
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH//2, timer_y))
        self.screen.blit(timer_surface, timer_rect)
        
        # Timer bar
        bar_width = 400
        bar_height = 10
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = timer_y + 25
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        time_ratio = self.time_remaining / self.time_limit
        fill_width = int(bar_width * time_ratio)
        bar_color = GREEN if time_ratio > 0.5 else YELLOW if time_ratio > 0.25 else RED
        pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Question
        question_y = 150
        wrapped_question = textwrap.wrap(question_data["question"], width=70)
        
        for i, line in enumerate(wrapped_question):
            question_surface = self.font_medium.render(line, True, BLACK)
            question_rect = question_surface.get_rect(center=(SCREEN_WIDTH//2, question_y + i * 35))
            self.screen.blit(question_surface, question_rect)
        
        # Answers
        answers_y = question_y + len(wrapped_question) * 35 + 50
        
        for i, answer in enumerate(question_data["answers"]):
            y_pos = answers_y + i * 60
            
            # Highlight selected answer
            if i == self.selected_answer:
                pygame.draw.rect(self.screen, LIGHT_GRAY, (100, y_pos - 5, SCREEN_WIDTH - 200, 50))
            
            # Answer letter and text
            letter = chr(ord('A') + i)
            answer_text = f"{letter}. {answer}"
            answer_surface = self.font_medium.render(answer_text, True, BLACK)
            self.screen.blit(answer_surface, (120, y_pos))
        
        # Lifelines
        lifeline_y = answers_y + 4 * 60 + 30
        lifeline_title = "Lifelines:"
        lifeline_title_surface = self.font_small.render(lifeline_title, True, BLUE)
        self.screen.blit(lifeline_title_surface, (50, lifeline_y))
        
        lifeline_x = 150
        if self.lifelines["50_50"]:
            fifty_text = "Press F for 50/50"
            fifty_surface = self.font_small.render(fifty_text, True, GREEN)
            self.screen.blit(fifty_surface, (lifeline_x, lifeline_y))
            lifeline_x += 150
        
        if self.lifelines["skip"]:
            skip_text = "Press S to Skip"
            skip_surface = self.font_small.render(skip_text, True, GREEN)
            self.screen.blit(skip_surface, (lifeline_x, lifeline_y))
        
        # Instructions
        instruction_text = "Use UP/DOWN arrows to select, ENTER to answer, or A/B/C/D keys"
        instruction_surface = self.font_small.render(instruction_text, True, GRAY)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Check if time is up
        if self.time_remaining <= 0:
            self.answer_question(-1)  # Time up, wrong answer
    
    def draw_result(self):
        self.screen.fill(WHITE)
        
        question_data = self.get_current_question()
        if not question_data:
            return
        
        # Determine if answer was correct
        last_answer = self.answered_questions[-1] if self.answered_questions else None
        if last_answer:
            correct = last_answer["user_answer"] == last_answer["correct_answer"]
            
            # Result message
            if correct:
                result_text = "Correct!"
                result_color = GREEN
                points_earned = self.calculate_points(question_data, last_answer["time_taken"])
                points_text = f"+{points_earned} points!"
            else:
                result_text = "Incorrect!"
                result_color = RED
                points_text = "No points"
            
            result_surface = self.font_large.render(result_text, True, result_color)
            result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(result_surface, result_rect)
            
            points_surface = self.font_medium.render(points_text, True, BLUE)
            points_rect = points_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(points_surface, points_rect)
            
            # Show correct answer
            correct_answer_text = f"Correct answer: {chr(ord('A') + question_data['correct'])}. {question_data['answers'][question_data['correct']]}"
            correct_surface = self.font_medium.render(correct_answer_text, True, BLACK)
            correct_rect = correct_surface.get_rect(center=(SCREEN_WIDTH//2, 280))
            self.screen.blit(correct_surface, correct_rect)
            
            # Show explanation or fun fact (if available)
            if "explanation" in question_data:
                explanation_lines = textwrap.wrap(question_data["explanation"], width=60)
                for i, line in enumerate(explanation_lines):
                    exp_surface = self.font_small.render(line, True, GRAY)
                    exp_rect = exp_surface.get_rect(center=(SCREEN_WIDTH//2, 320 + i * 25))
                    self.screen.blit(exp_surface, exp_rect)
        
        # Current score
        score_text = f"Current Score: {self.score}"
        score_surface = self.font_medium.render(score_text, True, PURPLE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(score_surface, score_rect)
        
        # Continue or finish
        if self.current_question < len(self.current_quiz) - 1:
            continue_text = "Press SPACE for next question"
        else:
            continue_text = "Press SPACE to see final results"
        
        continue_surface = self.font_small.render(continue_text, True, GRAY)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH//2, 550))
        self.screen.blit(continue_surface, continue_rect)
    
    def draw_game_over(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = "Quiz Complete!"
        title_surface = self.font_large.render(title_text, True, PURPLE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Final score
        final_score_text = f"Final Score: {self.score}"
        final_score_surface = self.font_large.render(final_score_text, True, GREEN)
        final_score_rect = final_score_surface.get_rect(center=(SCREEN_WIDTH//2, 180))
        self.screen.blit(final_score_surface, final_score_rect)
        
        # Statistics
        correct_answers = sum(1 for ans in self.answered_questions if ans["user_answer"] == ans["correct_answer"])
        accuracy = (correct_answers / len(self.answered_questions)) * 100 if self.answered_questions else 0
        
        stats_lines = [
            f"Questions Answered: {len(self.answered_questions)}/{len(self.current_quiz)}",
            f"Correct Answers: {correct_answers}",
            f"Accuracy: {accuracy:.1f}%",
            f"Category: {self.current_category}"
        ]
        
        for i, line in enumerate(stats_lines):
            stats_surface = self.font_medium.render(line, True, BLACK)
            stats_rect = stats_surface.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 35))
            self.screen.blit(stats_surface, stats_rect)
        
        # Performance rating
        if accuracy >= 90:
            rating = "Outstanding! You're a quiz master!"
        elif accuracy >= 75:
            rating = "Excellent! Great knowledge!"
        elif accuracy >= 60:
            rating = "Good job! Keep learning!"
        elif accuracy >= 40:
            rating = "Not bad! Room for improvement."
        else:
            rating = "Keep studying and try again!"
        
        rating_surface = self.font_medium.render(rating, True, BLUE)
        rating_rect = rating_surface.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(rating_surface, rating_rect)
        
        # Options
        options_text = "Press R to play again or ESC to quit"
        options_surface = self.font_small.render(options_text, True, GRAY)
        options_rect = options_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(options_surface, options_rect)
    
    def calculate_points(self, question_data, time_taken):
        """Calculate points based on difficulty and time"""
        base_points = {"Easy": 10, "Medium": 20, "Hard": 30}
        points = base_points.get(question_data["difficulty"], 10)
        
        # Time bonus (faster answers get more points)
        time_bonus = max(0, int((self.time_limit - time_taken) / 2))
        
        return points + time_bonus
    
    def answer_question(self, answer_index):
        """Process the answer to current question"""
        question_data = self.get_current_question()
        if not question_data:
            return
        
        time_taken = self.time_limit - self.time_remaining
        
        # Record the answer
        answer_record = {
            "question": question_data["question"],
            "user_answer": answer_index,
            "correct_answer": question_data["correct"],
            "time_taken": time_taken
        }
        self.answered_questions.append(answer_record)
        
        # Calculate score
        if answer_index == question_data["correct"]:
            points = self.calculate_points(question_data, time_taken)
            self.score += points
        
        self.game_state = "result"
    
    def use_fifty_fifty(self):
        """Use 50/50 lifeline"""
        if not self.lifelines["50_50"]:
            return
        
        question_data = self.get_current_question()
        if not question_data:
            return
        
        correct_answer = question_data["correct"]
        wrong_answers = [i for i in range(len(question_data["answers"])) if i != correct_answer]
        
        # Remove 2 wrong answers randomly
        to_remove = random.sample(wrong_answers, min(2, len(wrong_answers)))
        
        # Create new answer list with removed answers marked
        new_answers = []
        for i, answer in enumerate(question_data["answers"]):
            if i in to_remove:
                new_answers.append("[REMOVED]")
            else:
                new_answers.append(answer)
        
        question_data["answers"] = new_answers
        self.lifelines["50_50"] = False
    
    def skip_question(self):
        """Skip current question"""
        if not self.lifelines["skip"]:
            return
        
        # Mark as skipped (wrong answer with no time penalty)
        self.answer_question(-2)  # Special code for skipped
        self.lifelines["skip"] = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.generate_quiz(self.current_category)
                        self.game_state = "playing"
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_8:
                        category_index = event.key - pygame.K_1
                        categories = ["Mixed"] + self.categories
                        if category_index < len(categories):
                            self.current_category = categories[category_index]
                elif self.game_state == "playing":
                    if event.key == pygame.K_UP:
                        self.selected_answer = (self.selected_answer - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        self.selected_answer = (self.selected_answer + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        self.answer_question(self.selected_answer)
                    elif event.key >= pygame.K_a and event.key <= pygame.K_d:
                        answer_index = event.key - pygame.K_a
                        self.selected_answer = answer_index
                        self.answer_question(answer_index)
                    elif event.key == pygame.K_f:
                        self.use_fifty_fifty()
                    elif event.key == pygame.K_s:
                        self.skip_question()
                elif self.game_state == "result":
                    if event.key == pygame.K_SPACE:
                        self.current_question += 1
                        if self.current_question >= len(self.current_quiz):
                            self.game_state = "game_over"
                        else:
                            self.selected_answer = 0
                            self.question_start_time = pygame.time.get_ticks()
                            self.time_remaining = self.time_limit
                            self.game_state = "playing"
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart_game()
        return True
    
    def restart_game(self):
        """Restart the game"""
        self.game_state = "menu"
        self.current_question = 0
        self.selected_answer = 0
        self.score = 0
        self.answered_questions = []
        self.lifelines = {"50_50": True, "skip": True}
        self.current_category = "Mixed"
    
    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playing()
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
    game = QuizMaster()
    game.run()
