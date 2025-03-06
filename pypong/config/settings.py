import os
import yaml
import pygame
from enum import Enum, auto
from typing import Tuple, Optional

class GameState(Enum):
    """Enumeration of possible game states."""
    START_SCREEN = auto()
    PLAYING = auto()
    BETWEEN_POINTS = auto()
    GAME_OVER = auto()

class Settings:
    class ScreenSettings:
        def __init__(self):
            self.SCREEN_DIMENSIONS: Tuple[int, int] = (800, 600)
            self.FPS: int = 60

    class GameSettings:
        def __init__(self):
            self.WINNING_SCORE: int = 11
            self.WIN_BY_TWO: bool = True

    class Colors:
        def __init__(self):
            """Centralised color definitions using RGB tuples."""
            self.BLACK: Tuple[int, int, int] = (0, 0, 0)
            self.WHITE: Tuple[int, int, int] = (255, 255, 255)
            self.GREEN: Tuple[int, int, int] = (0, 255, 0)
            self.RED: Tuple[int, int, int] = (255, 0, 0)
            self.FOREST_GREEN: Tuple[int, int, int] = (34, 139, 34)
            self.CRIMSON: Tuple[int, int, int] = (220, 20, 60)
            self.BURLYWOOD: Tuple[int, int, int] = (222, 184, 135)
            self.LIGHT_BLUE: Tuple[int, int, int] = (135, 206, 235)

    class FontSettings:
        def __init__(self):
            """Font configuration for different text elements."""
            self.DEFAULT_FONT: Optional[str] = None # None uses pygame's default
            self.CONTROLS_FONT: str = 'courier new'
            self.TITLE_SIZE: int = 74
            self.MENU_SIZE: int = 36
            self.CONTROLS_SIZE: int = 16

    class KeyBindings:
        def __init__(self):
            """Initialise default key bindings for controls for both players."""
            self.left_up = pygame.K_w
            self.left_down = pygame.K_s
            self.right_up = pygame.K_UP
            self.right_down = pygame.K_DOWN

        def rebind_key(self, action, new_key):
            """
            Rebind an action (up or down, for either left or right player) to a new key.

            :param action: The action to rebind ('left_up', 'left_down', 'right_up' or 'right_down').
            :param new_key: The new Pygame key constant.
            """
            if action == "left_up":
                self.left_up = new_key
            elif action == "left_down":
                self.left_down = new_key
            elif action == "right_up":
                self.right_up = new_key
            elif action == "right_down":
                self.right_down = new_key
            else:
                raise ValueError("Invalid action - requires one of 'left_up', 'left_down', 'right_up' or 'right_down'.")

    class BallSettings:
        """Ball configuration parameters."""
        COLOR = None

    class PaddleSettings:
        """Paddle configuration parameters"""
        COLOR = None

    def __init__(self):
        # Initialise nested settings classes
        self.colors = self.Colors()
        self.fonts = self.FontSettings()
        self.ball = self.BallSettings()
        self.paddle = self.PaddleSettings()
        self.screen = self.ScreenSettings()
        self.game = self.GameSettings()
        self.key_bindings = self.KeyBindings()

        # Load user settings if available
        self._load_user_config()

    def update_settings(self, category, setting_name, value):
        if hasattr(self, category) and hasattr(getattr(self, category), setting_name):
            setattr(getattr(self, category), setting_name, value)
            return True
        return False

    def _load_user_config(self):
        """Load user settings from config.yaml if available and override default settings."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)

                # Update settings with user values
                if user_config:
                    print(f"User config file found at {config_path}")
                    if 'screen' in user_config:
                        screen_config = user_config['screen']
                        if 'screen_width' and 'screen_height' in screen_config:
                            self.screen.SCREEN_DIMENSIONS = (screen_config['screen_width'], screen_config['screen_height'])
                        if 'fps' in screen_config:
                            self.screen.FPS = screen_config['fps']

                    if 'gameplay' in user_config:
                        gameplay_config = user_config['gameplay']
                        if 'winning_score' in gameplay_config:
                            self.game.WINNING_SCORE = gameplay_config['winning_score']
                        if 'win_by_two' in gameplay_config:
                            self.game.WIN_BY_TWO = gameplay_config['win_by_two']


# Create singleton instance
settings = Settings()

