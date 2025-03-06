import pygame

class Ball:
    def __init__(self, side_length: int=10, x_pos=None, y_pos=None, h_speed: int=3, v_speed: int=5,
                 color: str="white", screen_size: tuple=(800, 600)):
        """
        Initialise a Ball object for the Pong game.

        Creates a ball with specified or default properties, including position,
        horizontal and vertical speed, colour, and screen boundaries.

        Args:
            side_length (int, optional): Size of the ball (width and height). Defaults to 10.
            x_pos (int, optional): Initial x-coordinate. Defaults to screen center.
            y_pos (int, optional): Initial y-coordinate. Defaults to screen center.
            h_speed (int, optional): Horizontal movement speed. Defaults to 3.
            v_speed (int, optional): Vertical movement speed. Defaults to 5.
            color (str, optional): Ball color. Defaults to "white".
            screen_size (tuple, optional): Screen dimensions (width, height). Defaults to (800, 600).

        Raises:
            ValueError: If side length is invalid or starting position is outside screen boundaries.
        """

        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.side_length = side_length

        # Validate side_length
        if side_length <= 0 or not isinstance(side_length, int):
            raise ValueError(f"Side length must be a positive integer.")

        # Validate starting position
        if x_pos is None:
            # Default position if none specified
            odd = 1
            if self.screen_width // 2 == 0:
                odd = 0
            x_pos = self.screen_width // 2 - side_length // 2 + odd

        if y_pos is None:
            # Default position if none specified
            odd = 1
            if self.screen_height // 2 == 0:
                odd = 0
            y_pos = self.screen_height // 2 - side_length // 2 + odd

        if (x_pos < 0 or y_pos < 0 or (x_pos + side_length) > self.screen_width
                or (y_pos + side_length) > self.screen_height):
            raise ValueError(f"Starting position is outside screen boundaries.")

        # Use validated dimensions to create pygame.Rect()
        self.rect = pygame.Rect(x_pos, y_pos, side_length, side_length)

        self.h_speed = h_speed
        self.v_speed = v_speed
        self.color = color


    def check_sides_hit(self):
        """Adjust vertical speed if ball hits top/bottom edge of screen."""
        if self.rect.top <= 0:
            self.v_speed = abs(self.v_speed)
            self.rect.top = 0
        elif self.rect.bottom >= self.screen_height:
            self.v_speed = -abs(self.v_speed)
            self.rect.bottom = self.screen_height


    def check_paddle_hit(self, paddle):
        """Reverse horizontal speed and increase the same by 1 if the ball hits either paddle."""
        if self.rect.colliderect(paddle):
            self.h_speed *= -1
            if self.h_speed < 0:
                self.h_speed -= 1
            else:
                self.h_speed += 1

            # Add angle variation - max/reset logic
            #     offset = (self.y - paddle.y) / paddle.height
            #     self.dy = (offset - 0.5) * 2  # Maps to range [-1, 1]


    def check_ends_hit(self):
        """Return end which was hit (if True)."""
        if self.rect.left <= 0:
            return "left"
        elif self.rect.right >= self.screen_width:
            return "right"
        else:
            return False


    def move(self):
        """Update ball position based on current horizontal and vertical speeds."""
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed


    def draw(self, screen):
        """Draw ball on screen."""
        pygame.draw.rect(screen, self.color, self.rect)