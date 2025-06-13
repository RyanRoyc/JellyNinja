# Import required modules
import pygame
import math
from utils.constants import *
from game_states.base_state import BaseState

class Instructions(BaseState):
    """
    Instructions state class that displays how to play the game.
    Shows game rules and controls with animated text effects.
    """
    
    def __init__(self, game):
        """
        Initialize the instructions state
        
        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        self.time = 0  # For animations
        self.setup_instructions()
        # Create back button at bottom of screen
        self.back_text, self.back_button = self.create_button(
            "Back", 
            (WINDOW_WIDTH//2, WINDOW_HEIGHT - 60)
        )
        
    def setup_instructions(self):
        """Define the instruction text to display"""
        self.instructions = [
            "HOW TO PLAY",
            "",
            "• Slice jellies with your mouse",
            "• Get points for each jelly sliced",
            "• Slice multiple jellies in one swipe for combo bonus!",
            "• Watch out for bombs - they end your game!",
            "",
            "The game gets harder over time:",
            "- Jellies move faster",
            "- More bombs appear",
            "- More jellies spawn at once",
            "",
            "Try to beat your high score!"
        ]
        
    def handle_event(self, event):
        """
        Handle instruction screen input events
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.game.change_state('menu')
                
    def update(self):
        """Update instruction screen animations"""
        self.time += 1/60  # Update animation timer
        
    def render(self, screen):
        """
        Render the instructions screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Draw animated background pattern
        for x in range(0, WINDOW_WIDTH, 100):
            for y in range(0, WINDOW_HEIGHT, 100):
                color = (
                    int(128 + 127 * math.sin(self.time + x / 200)),
                    int(128 + 127 * math.sin(self.time + y / 150)),
                    int(128 + 127 * math.cos(self.time * 0.7))
                )
                pygame.draw.circle(screen, color, (x, y), 
                                 50 + 10 * math.sin(self.time * 1.5 + x / 100))
        
        # Draw semi-transparent overlay for better text readability
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))
        
        # Draw instructions with animated effects
        for i, line in enumerate(self.instructions):
            if i == 0:  # Title
                text = self.title_font.render(line, True, WHITE)
            else:
                # Add wave effect to regular instructions
                color = (
                    255,
                    255,
                    int(200 + 55 * math.sin(self.time * 2 + i / 2))
                )
                text = self.font.render(line, True, color)
            
            # Calculate position with wave effect
            x = WINDOW_WIDTH//2
            base_y = 80 + i * 40  # Spacing between lines
            if i > 0:  # Don't apply wave to title
                x += math.sin(self.time * 2 + i / 2) * 10
            
            # Draw the text
            rect = text.get_rect(center=(x, base_y))
            screen.blit(text, rect)
        
        # Draw back button with hover effect
        hover = self.is_button_hovered(self.back_button)
        self.draw_button(screen, self.back_text, self.back_button, hover) 