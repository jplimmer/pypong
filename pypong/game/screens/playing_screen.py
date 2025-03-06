import pygame
from ...config import settings

class PlayingScreen:
    def __init__(self, screen_dims):
        """
        Initialise the playing screen.

        Args:
             screen_dims (tuple): Screen dimensions
        """
        self.screen_dims = screen_dims

    def render(self, screen, ball, l_paddle, r_paddle):
        """
        Render the playing screen.

        Args:
             screen (pygame.Surface): Pygame screen surface
             ball (Ball): Ball object
             l_paddle (Paddle): Paddle object
             r_paddle (Paddle): Paddle object
        """
        # Clear screen
        screen.fill(settings.colors.BLACK)

        # Draw objects
        self.draw_net(screen)
        l_paddle.draw(screen)
        r_paddle.draw(screen)
        ball.draw(screen)

    def draw_net(self, screen):
        """Draw a dashed net in the middle of the screen."""
        net_x = self.screen_dims[0] // 2
        num_segments = 20
        segment_height = self.screen_dims[1] // (num_segments * 2)
        net_width = 1

        for i in range(num_segments):
            # Calculate y-coordinate for each segment
            segment_y = i * (segment_height * 2)
            # Draw segment
            pygame.draw.rect(
                screen,
                settings.colors.WHITE,
                (net_x - net_width // 2, segment_y, net_width, segment_height)
            )

