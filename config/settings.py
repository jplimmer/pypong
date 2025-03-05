from enum import Enum, auto
from typing import Tuple

# Screen configuration
SCREEN_DIMENSIONS: Tuple[int, int] = (800, 600)
FPS: int = 60
WINNING_SCORE: int = 11

class Colors:
    """Centralised color definitions using RGB tuples."""
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    FOREST_GREEN: Tuple[int, int, int] = (34, 139, 34)
    CRIMSON: Tuple[int, int, int] = (220, 20, 60)
    BURLYWOOD: Tuple[int, int, int] = (222, 184, 135)
    LIGHT_BLUE: Tuple[int, int, int] = (135, 206, 235)

class FontSettings:
    """Font configuration for different text elements."""
    TITLE_SIZE: int = 74
    MENU_SIZE: int = 36
    CONTROLS_SIZE: int = 16
    DEFAULT_FONT: str = None  # None uses pygame's default
    CONTROLS_FONT: str = 'courier new'

# Game state management
class GameState(Enum):
    """Enumeration of possible game states."""
    START_SCREEN = auto()
    PLAYING = auto()
    BETWEEN_POINTS = auto()
    GAME_OVER = auto()