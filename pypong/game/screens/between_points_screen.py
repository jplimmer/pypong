import pygame
from ...config import settings

class BetweenPointsScreen:
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


    def render(self, screen, scores):
        """
        Render the between points screen.

        Args:
             screen (pygame.Surface): Pygame screen surface
             scores (tuple): Final scores for both players (score_p1, score_p2)
        """
        # Clear screen
        screen.fill(settings.colors.BLACK)

        # Current score
        p1_text = self.title_font.render(f"Player 1: ", True, settings.colors.WHITE)
        p2_text = self.title_font.render(f"Player 2: ", True, settings.colors.WHITE)

        # Colour-coding for scores
        if scores[0] > scores[1]:
            p1_score_text = self.title_font.render(f"{scores[0]}", True, settings.colors.FOREST_GREEN)
            p2_score_text = self.title_font.render(f"{scores[1]}", True, settings.colors.CRIMSON)
        elif scores[0] < scores[1]:
            p1_score_text = self.title_font.render(f"{scores[0]}", True, settings.colors.CRIMSON)
            p2_score_text = self.title_font.render(f"{scores[1]}", True, settings.colors.FOREST_GREEN)
        else:
            p1_score_text = self.title_font.render(f"{scores[0]}", True, settings.colors.BURLYWOOD)
            p2_score_text = self.title_font.render(f"{scores[1]}", True, settings.colors.BURLYWOOD)

        p1_comb_width = p1_text.get_width() + p1_score_text.get_width()
        p2_comb_width = p2_text.get_width() + p2_score_text.get_width()

        score_rect = pygame.Rect(self.screen_dims[0] // 2 - p1_text.get_width(),
                                 self.screen_dims[1] // 2 - p1_text.get_height() * 1.1 - 100,
                                 max(p1_comb_width, p2_comb_width),
                                 p1_text.get_height() * 2.1)

        screen.blit(p1_text, (score_rect.x, score_rect.y))
        screen.blit(p1_score_text, (score_rect.x + p1_text.get_width(), score_rect.y))
        screen.blit(p2_text, (score_rect.x, score_rect.y + p1_text.get_height() * 1.1))
        screen.blit(p2_score_text, (score_rect.x + p2_text.get_width(), score_rect.y + p1_text.get_height() * 1.1))

        # 'Continue' instructions
        win_by_two_text = "(win by 2 points)" if settings.game.WIN_BY_TWO else ""
        continue_text_1 = self.menu_font.render(f"First to {settings.game.WINNING_SCORE} {win_by_two_text}", True, "grey")
        continue_text_2 = self.menu_font.render(f"Press SPACE to continue", True, settings.colors.WHITE)
        continue_rect_1 = continue_text_1.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50))
        continue_rect_2 = continue_text_2.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50 +
                                                           continue_rect_1.height * 2))
        screen.blit(continue_text_1, continue_rect_1)
        screen.blit(continue_text_2, continue_rect_2)

