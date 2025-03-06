import pygame
from ...config import settings

class StartScreen:
    def __init__(self, screen_dims):
        """
        Initialise the start screen.

        Args:
            screen_dims (tuple): Screen dimensions
        """
        self.screen_dims = screen_dims

        # Initialise fonts
        self.title_font = pygame.font.Font(settings.fonts.DEFAULT_FONT, settings.fonts.TITLE_SIZE)
        self.menu_font = pygame.font.Font(settings.fonts.DEFAULT_FONT, settings.fonts.MENU_SIZE)
        self.controls_font = pygame.font.SysFont(settings.fonts.CONTROLS_FONT, settings.fonts.CONTROLS_SIZE, bold=True)


    def render(self, screen, key_bindings):
        """
        Render the start screen.

        Args:
            screen (pygame.Surface): Pygame screen surface
            key_bindings (KeyBindings): Current key bindings for players
        """

        # Clear screen
        screen.fill(settings.colors.BLACK)

        # Title
        title_text = self.title_font.render("Welcome to PyPong!", True, settings.colors.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 - 100))
        screen.blit(title_text, title_rect)

        # 'Start' instructions
        start_text = self.menu_font.render("Press SPACE to start", True, settings.colors.WHITE)
        start_rect = start_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50))
        screen.blit(start_text, start_rect)

        # Player controls
        self._render_player_controls(screen, key_bindings)

    def _render_player_controls(self, screen, key_bindings):
        """
        Render player control instructions.

        Args:
            screen (pygame.Surface): Pygame screen surface
            key_bindings (KeyBindings): Current key bindings for players
        """
        p1_controls_text = [
            self.controls_font.render("Player 1 controls: ", True, settings.colors.WHITE),
            self.controls_font.render(f"{pygame.key.name(key_bindings.left_up).upper()} - Move up",
                                      True,
                                      settings.colors.WHITE),
            self.controls_font.render(f"{pygame.key.name(key_bindings.left_down).upper()} - Move down",
                                      True,
                                      settings.colors.WHITE)
        ]

        p2_controls_text = [
            self.controls_font.render("Player 2 controls: ", True, settings.colors.WHITE),
            self.controls_font.render(f"{pygame.key.name(key_bindings.right_up).upper()} - Move up",
                                      True,
                                      settings.colors.WHITE),
            self.controls_font.render(f"{pygame.key.name(key_bindings.right_down).upper()} - Move down",
                                      True,
                                      settings.colors.WHITE)
        ]

        start_x = self.screen_dims[0] // 6
        start_y = self.screen_dims[1] // 2 + 130
        spacing = 25
        p1_controls_width = p1_controls_text[0].get_width()

        # Render Player 1 controls
        for i, text in enumerate(p1_controls_text):
            text_rect = text.get_rect(
                left=start_x,
                top=start_y + i * spacing
            )
            screen.blit(text, text_rect)

        # Render Player 2 controls
        for i, text in enumerate(p2_controls_text):
            text_rect = text.get_rect(
                left=start_x * 5 - p1_controls_width,
                top=start_y + i * spacing
            )
            screen.blit(text, text_rect)

