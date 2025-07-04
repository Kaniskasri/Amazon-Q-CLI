# ThinkVerse Game Launcher

A Python-based game launcher featuring 8 unique pygame-powered mini-games.

## Requirements

- Python 3.6+
- pygame library

## Installation

1. Install pygame:
```bash
pip install pygame
```

2. Run the launcher:
```bash
python thinkverse_launcher.py
```

## Games Included

### 1. Code Breaker
A logic puzzle game where you guess a secret 4-digit code using color-coded hints.
- **Controls**: Number keys (1-6), ENTER to submit, BACKSPACE to edit
- **Objective**: Decode the secret sequence in 10 attempts or less

### 2. AI Dungeon Quest
A text-based adventure game with branching story choices.
- **Controls**: Arrow keys to navigate, ENTER to select, number keys for direct choice
- **Features**: Multiple story paths, inventory system, score tracking

### 3. Memory Matrix
Test your memory by recalling number patterns shown briefly on a grid.
- **Controls**: Arrow keys to navigate, ENTER to select positions, SPACE to continue
- **Challenge**: Patterns get more complex as you progress through levels

### 4. Mystery Sound
Identify objects based on visual sound representations and text clues.
- **Controls**: Type your guess, SPACE for next clue, G to make guess
- **Features**: Animated visual sound effects, progressive hint system

### 5. Escape 404
A digital escape room with three challenging puzzle rooms.
- **Room 1**: Binary code decoding
- **Room 2**: Network routing puzzle (click to create paths)
- **Room 3**: Password cracking using clues
- **Controls**: Keyboard input, mouse clicking for grid puzzles

### 6. Quantum Dice
Strategic dice game with probability-manipulation abilities.
- **Controls**: Arrow keys to select strategy, ENTER to confirm, SPACE to continue
- **Features**: Quantum energy system, special scoring bonuses, AI opponent

### 7. Quiz Master
Test your knowledge with trivia questions across multiple categories.
- **Controls**: Arrow keys to navigate, ENTER to select, A/B/C/D for direct answers
- **Features**: Multiple categories, timed questions, lifelines (50/50, Skip), scoring system

### 8. Snake Classic
Classic snake game with modern power-ups and multiple difficulty levels.
- **Controls**: Arrow keys to move, SPACE to pause
- **Features**: Power-ups (invincibility, slow-motion, double points), multiple difficulties, lives system

## Launcher Controls

- **Arrow Keys**: Navigate game menu
- **ENTER**: Launch selected game
- **Number Keys (1-8)**: Direct game selection
- **ESC**: Quit launcher

## Game Features

- Each game runs as an independent pygame application
- Visual and audio feedback (where applicable)
- Score tracking and progression systems
- Restart functionality in all games
- Consistent control schemes across games

## Troubleshooting

If you encounter issues:
1. Ensure pygame is properly installed: `pip install --upgrade pygame`
2. Check that all game files are in the same directory as the launcher
3. Verify Python version compatibility (3.6+)

## File Structure

```
thinkverse_launcher.py    # Main launcher
code_breaker.py          # Logic puzzle game
ai_dungeon_quest.py      # Text adventure game
memory_matrix.py         # Memory challenge game
mystery_sound.py         # Sound identification game
escape_404.py           # Digital escape room
quantum_dice.py         # Strategic dice game
quiz_master.py          # Trivia quiz game
snake_classic.py        # Classic snake game
README.md               # This file
```

Enjoy exploring the ThinkVerse!
#