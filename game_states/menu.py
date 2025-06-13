# Import required modules
import pygame
import math
from utils.constants import *
from game_states.base_state import BaseState

class Menu(BaseState):
    """
    Menu state class that handles the main menu screen.
    Displays title, buttons, and animated background.
    """
    
    def __init__(self, game):
        """
        Initialize the menu state
        
        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        self.buttons = {}
        self.time = 0  # For animations
        self.setup_buttons()
        self.bg_offset = 0  # For background animation
        
    def setup_buttons(self):
        """Create and position all menu buttons"""
        center_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        
        # Create buttons with vertical spacing
        button_texts = ["Start", "Instructions", "Quit"]
        for i, text in enumerate(button_texts):
            y_pos = start_y + (BUTTON_HEIGHT + BUTTON_PADDING) * i
            text_surf, button_rect = self.create_button(text, (center_x, y_pos))
            self.buttons[text] = {
                'text': text_surf,
                'rect': button_rect,
                'hover': False,
                'base_y': y_pos  # Store original y position for animation
            }
    
    def handle_event(self, event):
        """
        Handle menu input events
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for text, button in self.buttons.items():
                if button['rect'].collidepoint(event.pos):
                    if text == "Start":
                        self.game.states['game'].reset_game()
                        self.game.change_state('game')
                    elif text == "Instructions":
                        self.game.change_state('instructions')
                    elif text == "Quit":
                        self.game.running = False
                        
    def update(self):
        """Update menu animations and button states"""
        self.time += 1/60  # Update animation timer
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button['hover'] = button['rect'].collidepoint(mouse_pos)
            
    def render(self, screen):
        """
        Render the menu screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Draw animated background circles
        for x in range(-1, 2):
            for y in range(-1, 2):
                offset_x = (x * WINDOW_WIDTH + self.bg_offset) % WINDOW_WIDTH
                offset_y = (y * WINDOW_HEIGHT + self.bg_offset) % WINDOW_HEIGHT
                color = (
                    int(128 + 127 * math.sin(self.time + offset_x / 100)),
                    int(128 + 127 * math.sin(self.time + offset_y / 100)),
                    int(128 + 127 * math.sin(self.time * 0.5))
                )
                pygame.draw.circle(screen, color, 
                                 (offset_x, offset_y), 
                                 100 + 20 * math.sin(self.time * 2))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title = self.title_font.render("Jelly Ninja", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        screen.blit(title, title_rect)
        
        # Draw high score
        high_score_text = self.font.render(
            f"High Score: {self.game.high_score.get_high_score()}", 
            True, WHITE
        )
        high_score_rect = high_score_text.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4 + 80)
        )
        screen.blit(high_score_text, high_score_rect)
        
        # Draw buttons with hover effects and floating animation
        for button in self.buttons.values():
            # Calculate floating offset for smooth button animation
            float_offset = math.sin(self.time * 4) * 5
            
            # Temporarily move the button for rendering
            button['rect'].centery = button['base_y'] + float_offset
            
            # Draw the button with hover effect
            self.draw_button(
                screen,
                button['text'],
                button['rect'],
                button['hover']
            )
            
            # Reset the button position
            button['rect'].centery = button['base_y'] 