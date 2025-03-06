import pygame

class Paddle:
    def __init__(self, left: bool=True, width: int=5, length: int=60, y_pos=None, v_speed: int=0, color: str="white",
                 screen_size: tuple=(800, 600)):
        """
        Initialise a Paddle object for the Pong game.

        Creates a paddle with specified or default properties, including position,
        size, movement speed, and colour.

        Args:
            left (bool, optional): Paddle position (True for left, False for right). Defaults to True.
            width (int, optional): Paddle width. Defaults to 5.
            length (int, optional): Paddle height/length. Defaults to 60.
            y_pos (int, optional): Initial y-coordinate. Defaults to screen center.
            v_speed (int, optional): Vertical movement speed. Defaults to 0.
            color (str, optional): Paddle color. Defaults to "white".
            screen_size (tuple, optional): Screen dimensions (width, height). Defaults to (800, 600).

        Raises:
            ValueError: If width or length is invalid, or starting position is outside screen boundaries.
        """
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.left = left

        # Validate width and length
        for param in [width, length]:
            if param <= 0 and not isinstance(param, int):
                raise ValueError(f"{str(param).title()} must be a positive integer.")

        self.width = width

        # Validate starting position
        if y_pos is None:
            # Default `y_pos` if none specified
            odd = 1
            if self.screen_height // 2 == 0:
                odd = 0
            y_pos = self.screen_height // 2 - length // 2 + odd

        if (self.x_pos < 0 or y_pos < 0 or (self.x_pos + width) > self.screen_width
                or (y_pos + length) > self.screen_height):
            raise ValueError(f"Starting position is outside screen boundaries.")


        # Use validated dimensions to create pygame.Rect()
        self.rect = pygame.Rect(self.x_pos, y_pos, width, length)

        self._v_speed = v_speed
        self.color = color


    @property
    def x_pos(self):
        """
        Get x-coordinate of paddle based on left and width params.

        Returns:
            int: x-coordinate of paddle
        """
        if self.left:
            return 2
        else:
            return self.screen_width - (self.width + 2)


    @property
    def v_speed(self):
        """
        Get paddle's vertical speed.

        Returns:
            int: vertical speed
        """
        return self._v_speed


    @v_speed.setter
    def v_speed(self, value):
        """
        Set paddle's vertical speed (with validation).

        :param value (int): New speed value.
        :raises: ValueError: If new speed value outside range -10 to 10.
        """
        if -10 <= value <= 10:
            self._v_speed = value
        else:
            raise ValueError(f"New v_speed value must be an int within -10 to 10.")


    def check_edges_hit(self):
        """
        Check if paddle has reached top or bottom of screen.
        If true, stop paddle at top/bottom of screen and reset paddle speed to 0.
        """
        if self.rect.top <= 0:
            self._v_speed = 0
            self.rect.top = 0
        elif self.rect.bottom >= self.screen_height:
            self._v_speed = 0
            self.rect.bottom = self.screen_height


    def move(self):
        """
        Move paddle according to current vertical speed.
        Call check_edges_hit() to prevent paddle moving off-screen.
        """
        # Subtracts speed value to account for pygame coordinates increasing from top to bottom
        self.rect.top -=self._v_speed

        self.check_edges_hit()

        return

    def draw(self, screen):
        """Draw paddle on screen."""
        pygame.draw.rect(screen, self.color, self.rect)