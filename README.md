# Jelly Ninja

A fun and addictive Fruit Ninja-style game built with Pygame, featuring bouncy jellies, combos, and explosions!

## Features

- Slice colorful, bouncy jellies with your mouse
- Chain combos for bonus points
- Avoid bombs or it's game over!
- Progressive difficulty
- High score system
- Smooth animations and particle effects
- No external assets - everything generated in code!

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python main.py
```

### Controls
- Use your mouse to slice jellies
- Slice multiple jellies in one swipe for combo bonuses
- Avoid the black bombs!

### Scoring
- 1 point per jelly sliced
- Bonus points for combos (3+ jellies in one slice)
- Game ends if you hit a bomb

## Development

The game is built with a state-based architecture:
- `main.py` - Game initialization and main loop
- `game_states/` - Different game states (menu, game, etc.)
- `utils/` - Utility functions and constants

All graphics are generated programmatically - no external assets needed! 