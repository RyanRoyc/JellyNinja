# main.py
#
# TEJ3M
#
# June 11, 2025
#
# Ryan Roychowdhury
#
# This project was developed utilizing the claude-3.5-sonnet AI model in the Cursor IDE


# Import necessary modules
import pygame  # Main game library for graphics and input
import sys    # For system-level operations like exiting the game
from game_states.menu import Menu                 # Menu screen state
from game_states.game import Game                 # Main gameplay state
from game_states.instructions import Instructions # Instructions screen state
from game_states.game_over import GameOver       # Game over screen state
from utils.constants import *                     # Game constants and settings
from utils.high_score import HighScore           # High score management

class JellyNinja:
    """
    Main game class that manages the game states and main loop.
    Handles initialization, state switching, and game execution.
    """
    def __init__(self):
        """Initialize the game, create window, and set up game states"""
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Jelly Ninja")
        
        # Create the game window and clock
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = None
        self.high_score = HighScore()
        
        # Initialize all game states
        self.states = {
            'menu': Menu(self),
            'game': Game(self),
            'instructions': Instructions(self),
            'game_over': GameOver(self)
        }
        # Start with the menu state
        self.change_state('menu')

    def change_state(self, new_state):
        """
        Switch to a different game state
        Args:
            new_state (str): Name of the state to switch to
        """
        self.current_state = self.states[new_state]
        self.current_state.enter()

    def run(self):
        """Main game loop that handles events, updates, and rendering"""
        while self.running:
            # Maintain consistent frame rate
            self.clock.tick(FPS)
            
            # Process all events
            for event in pygame.event.get():
                # Check for game exit
                if event.type == pygame.QUIT:
                    self.running = False
                # Pass events to current state
                self.current_state.handle_event(event)
            
            # Update and render current state
            self.current_state.update()
            self.current_state.render(self.screen)
            
            # Update display
            pygame.display.flip()

        # Clean up and exit
        pygame.quit()
        sys.exit()

# Only run the game if this file is run directly
if __name__ == "__main__":
    game = JellyNinja()
    game.run() 