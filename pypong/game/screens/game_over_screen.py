import pygame
from ...config import settings

class GameOverScreen:
    def __init__(self, screen_dims):
        """
        Initialise the game over screen.

        Args:
             screen_dims (tuple): Screen dimensions
        """
        self.screen_dims = screen_dims

        # Initialise fonts
        self.title_font = pygame.font.Font(settings.fonts.DEFAULT_FONT, settings.fonts.TITLE_SIZE)
        self.menu_font = pygame.font.Font(settings.fonts.DEFAULT_FONT, settings.fonts.MENU_SIZE)

    def render(self, screen, winner, scores):
        """
        Render the game over screen.

        Args:
             screen (pygame.Surface): Pygame screen surface
             winner (str): Name of the winning player
             scores (tuple): Final scores for both players (score_p1, score_p2)
        """
        # Clear screen
        screen.fill(settings.colors.BLACK)

        # Game over text
        game_over_text = self.title_font.render(f"GAME OVER - {winner} wins!", True, settings.colors.GREEN)
        game_over_rect = game_over_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        # Final score
        score_text = self.menu_font.render(
            f"Final Score: Player 1 {scores[0]} - {scores[1]} Player 2",
            True,
            settings.colors.WHITE
        )
        start_rect = score_text.get_rect(
            center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2))
        screen.blit(score_text, start_rect)

        # Restart instructions
        restart_text = self.menu_font.render("Press SPACE to restart", True, settings.colors.WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 100))
        screen.blit(restart_text, restart_rect)


