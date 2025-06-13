# Import required modules
import pygame
import math
from utils.constants import *
from game_states.base_state import BaseState

class GameOver(BaseState):
    """
    Game Over state class that shows the final score and options to continue.
    Displays score, high score, and buttons with animated effects.
    """
    
    def __init__(self, game):
        """
        Initialize the game over state
        
        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        self.time = 0  # For animations
        self.setup_buttons()
        
    def setup_buttons(self):
        """Create and position the game over screen buttons"""
        center_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT * 3 // 4  # Position buttons in lower third
        
        # Create buttons with vertical spacing
        self.buttons = {}
        button_texts = ["Play Again", "Main Menu"]
        for i, text in enumerate(button_texts):
            y_pos = start_y + (BUTTON_HEIGHT + BUTTON_PADDING) * i
            text_surf, button_rect = self.create_button(text, (center_x, y_pos))
            self.buttons[text] = {
                'text': text_surf,
                'rect': button_rect,
                'hover': False
            }
            
    def handle_event(self, event):
        """
        Handle game over screen input events
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for text, button in self.buttons.items():
                if button['rect'].collidepoint(event.pos):
                    if text == "Play Again":
                        self.game.states['game'].reset_game()
                        self.game.change_state('game')
                    elif text == "Main Menu":
                        self.game.change_state('menu')
                        
    def update(self):
        """Update game over screen animations and button states"""
        self.time += 1/60  # Update animation timer
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button['hover'] = button['rect'].collidepoint(mouse_pos)
            
    def render(self, screen):
        """
        Render the game over screen
        
        Args:
            screen: Pygame surface to render to
        """
        # Draw background with pulsing red overlay
        screen.fill((40, 0, 0))
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((255, 0, 0))
        alpha = int(64 + 32 * math.sin(self.time * 2))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        
        # Draw "Game Over" text with shadow effect
        game_over_text = self.title_font.render("Game Over", True, WHITE)
        text_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
        )
        
        # Draw shadow
        shadow_surf = self.title_font.render("Game Over", True, (128, 0, 0))
        shadow_rect = shadow_surf.get_rect(
            center=(WINDOW_WIDTH//2 + 4, WINDOW_HEIGHT//3 + 4)
        )
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(game_over_text, text_rect)
        
        # Get scores
        score = self.game.states['game'].score
        high_score = self.game.high_score.get_high_score()
        
        # Draw current score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30)
        )
        screen.blit(score_text, score_rect)
        
        # Draw high score
        high_score_text = self.font.render(
            f"High Score: {high_score}", True, WHITE
        )
        high_score_rect = high_score_text.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30)
        )
        screen.blit(high_score_text, high_score_rect)
        
        # Draw new high score message with pulsing animation if applicable
        if score == high_score and score > 0:
            new_record_text = self.font.render(
                "New High Score!", True, (255, 255, 0)
            )
            new_record_rect = new_record_text.get_rect(
                center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 90)
            )
            # Make it pulse
            scale = 1 + 0.1 * math.sin(self.time * 4)
            scaled_text = pygame.transform.scale(
                new_record_text,
                (int(new_record_rect.width * scale),
                 int(new_record_rect.height * scale))
            )
            scaled_rect = scaled_text.get_rect(
                center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 90)
            )
            screen.blit(scaled_text, scaled_rect)
        
        # Draw buttons with hover effects
        for button in self.buttons.values():
            self.draw_button(
                screen,
                button['text'],
                button['rect'],
                button['hover']
            ) 