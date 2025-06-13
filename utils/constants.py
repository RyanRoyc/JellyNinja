# Import Pygame for color definitions and other constants
import pygame

# Window settings
WINDOW_WIDTH = 1280   # Width of game window in pixels
WINDOW_HEIGHT = 720   # Height of game window in pixels
FPS = 60             # Target frames per second for smooth gameplay

# Basic color definitions (RGB format)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Game settings
# List of colors for jellies (RGB format)
JELLY_COLORS = [
    (255, 100, 100),  # Red jelly
    (100, 255, 100),  # Green jelly
    (100, 100, 255),  # Blue jelly
    (255, 255, 100),  # Yellow jelly
    (255, 100, 255),  # Pink jelly
]

# Physics settings
GRAVITY = 0.35           # Gravity strength for falling objects
INITIAL_VELOCITY = -18   # Starting upward velocity for objects
SPAWN_INTERVAL = 1.2     # Time between object spawns in seconds
COMBO_TIME = 0.4         # Time window for combo chains in seconds

# Difficulty progression settings
DIFFICULTY_INCREASE_INTERVAL = 20  # Time between difficulty increases in seconds
SPEED_INCREASE = 1.15            # Multiplier for speed increases
SPAWN_RATE_INCREASE = 0.85       # Multiplier for spawn rate increases
BOMB_CHANCE_INCREASE = 1.3       # Multiplier for bomb frequency increases

# UI settings
BUTTON_WIDTH = 200    # Width of UI buttons in pixels
BUTTON_HEIGHT = 60    # Height of UI buttons in pixels
BUTTON_PADDING = 20   # Space between buttons in pixels
FONT_SIZE = 36        # Regular text size
TITLE_FONT_SIZE = 72  # Title text size

# Animation settings
SLICE_TRAIL_LENGTH = 10    # Number of points to track for slice trail
PARTICLE_COUNT = 20        # Number of particles per effect
SHAKE_INTENSITY = 10       # Screen shake amount in pixels
SHAKE_DURATION = 0.3       # Screen shake duration in seconds 