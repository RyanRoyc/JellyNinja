# Import required modules
import pygame
from utils.constants import *

class BaseState:
    """
    Base class for all game states (menu, game, instructions, game over).
    Provides common functionality and interface for state management.
    """
    
    def __init__(self, game):
        """
        Initialize the base state
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        # Initialize fonts for text rendering
        self.font = pygame.font.SysFont('arial', FONT_SIZE)
        self.title_font = pygame.font.SysFont('arial', TITLE_FONT_SIZE)
        
    def enter(self):
        """Called when entering the state. Override in child classes if needed."""
        pass
        
    def exit(self):
        """Called when exiting the state. Override in child classes if needed."""
        pass
        
    def handle_event(self, event):
        """
        Process input events
        
        Args:
            event: Pygame event to process
        """
        pass
        
    def update(self):
        """Update game logic. Override in child classes."""
        pass
        
    def render(self, screen):
        """
        Render the state
        
        Args:
            screen: Pygame surface to render to
        """
        pass
        
    def create_button(self, text, center_pos):
        """
        Create a button with text
        
        Args:
            text (str): Text to display on the button
            center_pos (tuple): (x, y) position for button center
            
        Returns:
            tuple: (text_surface, button_rect) for rendering
        """
        text_surface = self.font.render(text, True, WHITE)
        button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rect.center = center_pos
        return text_surface, button_rect
        
    def draw_button(self, screen, text_surface, button_rect, hovered=False):
        """
        Draw a button with hover effect
        
        Args:
            screen: Surface to draw on
            text_surface: Pre-rendered text surface
            button_rect: Rectangle defining button bounds
            hovered (bool): Whether the button is being hovered over
        """
        # Draw button background with hover effect
        color = (100, 100, 100) if hovered else (50, 50, 50)
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, width=2, border_radius=10)
        
        # Center the text on the button
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_button_hovered(self, button_rect):
        """
        Check if a button is being hovered over
        
        Args:
            button_rect: Rectangle defining button bounds
            
        Returns:
            bool: True if mouse is over button, False otherwise
        """
        return button_rect.collidepoint(pygame.mouse.get_pos()) 