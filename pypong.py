import pygame
import random


# Game states
START_SCREEN = 0
PLAYING = 1
BETWEEN_POINTS = 2
GAME_OVER = 3


class Game:
    def __init__(self):
        """
        Initialise the PyPong game with game setup, configuration, and initial game state.

        Sets up pygame, screen dimensions, game fonts, initial scoring, game objects,
        and prepares the game for starting. Configures:
        - Screen display and frame rate
        - Custom fonts for menus and titles
        - Initial game state (start screen)
        - Scoring parameters
        - Game objects (ball and paddles)
        - Key bindings for player controls

        Attributes:
            screen_dims (tuple): Screen width and height in pixels
            current_state (int): Current game state (START_SCREEN, PLAYING, etc.)
            score_p1 (int): Score for Player 1 (left paddle)
            score_p2 (int): Score for Player 2 (right paddle)
            winning_score (int): Points needed to win the game
            ball (Ball): Game ball object
            l_paddle (Paddle): Left player's paddle
            r_paddle (Paddle): Right player's paddle
        """
        # pygame setup
        pygame.init()
        pygame.display.set_caption("PyPong")
        self.screen_dims = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_dims)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Fonts
        self.title_font = pygame.font.Font(None, 74)
        self.menu_font = pygame.font.Font(None, 36)

        # Game state tracking
        self.current_state = START_SCREEN
        self.score_p1 = 0 #p1 is left paddle
        self.score_p2 = 0
        self.winning_score = 11
        self.winner = ""

        # User config
        self.key_bindings = KeyBindings()

        # Create ball & paddle instances
        self.ball = Ball(screen_size=self.screen_dims)
        self.l_paddle = Paddle(left=True, screen_size=self.screen_dims) #p1
        self.r_paddle = Paddle(left=False, screen_size=self.screen_dims)


    def draw_start_screen(self):
        """Render the START_SCREEN."""
        self.screen.fill("black")

        # Title
        title_text = self.title_font.render("Welcome to PyPong!", True, "white")
        title_rect = title_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # 'Start' instructions
        start_text = self.menu_font.render("Press SPACE to start", True, "white")
        start_rect = start_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50))
        self.screen.blit(start_text, start_rect)


    def draw_between_points_screen(self):
        """Render the BETWEEN_POINTS screen."""
        self.screen.fill("black")

        # Current score
        p1_text = self.title_font.render(f"Player 1: ", True, "white")
        p2_text = self.title_font.render(f"Player 2: ", True, "white")

        # Colour-coding for scores
        if self.score_p1 > self.score_p2:
            p1_score_text = self.title_font.render(f"{self.score_p1}", True, "forestgreen")
            p2_score_text = self.title_font.render(f"{self.score_p2}", True, "crimson")
        elif self.score_p1 < self.score_p2:
            p1_score_text = self.title_font.render(f"{self.score_p1}", True, "crimson")
            p2_score_text = self.title_font.render(f"{self.score_p2}", True, "forestgreen")
        else:
            p1_score_text = self.title_font.render(f"{self.score_p1}", True, "burlywood")
            p2_score_text = self.title_font.render(f"{self.score_p2}", True, "burlywood")

        p1_comb_width = p1_text.get_width() + p1_score_text.get_width()
        p2_comb_width = p2_text.get_width() + p2_score_text.get_width()

        score_rect = pygame.Rect(self.screen_dims[0] // 2 - p1_text.get_width(),
                                 self.screen_dims[1] // 2 - p1_text.get_height() * 1.1 - 100,
                                 max(p1_comb_width, p2_comb_width),
                                 p1_text.get_height() * 2.1)

        self.screen.blit(p1_text, (score_rect.x, score_rect.y))
        self.screen.blit(p1_score_text, (score_rect.x + p1_text.get_width(), score_rect.y))
        self.screen.blit(p2_text, (score_rect.x, score_rect.y + p1_text.get_height() * 1.1))
        self.screen.blit(p2_score_text, (score_rect.x + p2_text.get_width(), score_rect.y + p1_text.get_height() * 1.1))

        # 'Continue' instructions
        continue_text_1 = self.menu_font.render(f"First to {self.winning_score} (win by 2 points)", True, "grey")
        continue_text_2 = self.menu_font.render(f"Press SPACE to continue", True, "white")
        continue_rect_1 = continue_text_1.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50))
        continue_rect_2 = continue_text_2.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 50 +
                                                           continue_rect_1.height * 2))
        self.screen.blit(continue_text_1, continue_rect_1)
        self.screen.blit(continue_text_2, continue_rect_2)


    def draw_game_over_screen(self):
        """Render the GAME_OVER screen."""
        self.screen.fill("black")

        # Game over text
        game_over_text = self.title_font.render(f"GAME OVER - {self.winner} wins!", True, "green")
        game_over_rect = game_over_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)

        # # Final score
        # start_text = self.menu_font.render(f"Player 1: {self.score_p1}\tPlayer 2: {self.score_p2}",
        #                                     True, "white")
        # start_rect = start_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2))
        # self.screen.blit(start_text, start_rect)

        # Restart instructions
        restart_text = self.menu_font.render("Press SPACE to restart", True, "white")
        restart_rect = restart_text.get_rect(center=(self.screen_dims[0] // 2, self.screen_dims[1] // 2 + 100))
        self.screen.blit(restart_text, restart_rect)


    def draw_playing_screen(self):
        """Render the PLAYING screen."""
        self.screen.fill("black")

        self.draw_net()
        self.l_paddle.draw(self.screen)
        self.r_paddle.draw(self.screen)
        self.ball.draw(self.screen)


    def draw_net(self):
        """Draw a dashed net in the middle of the screen."""
        net_x = self.screen_dims[0] // 2
        num_segments = 20
        segment_height = self.screen_dims[1] // (num_segments * 2)
        net_width = 1

        for i in range(num_segments):
            # Calculate y-coordinate for each segment
            segment_y = i * (segment_height * 2)
            # Draw segment
            pygame.draw.rect(self.screen, "white", (net_x - net_width // 2, segment_y, net_width, segment_height))


    def update_game_objects(self):
        """
        Update ball position and check if edges or paddles have been hit.
        Update paddle positions.
        """
        # Update ball and paddle positions
        self.ball.move()

        # Change direction if ball hits either side (top/bottom)
        self.ball.check_sides_hit()

        # Change direction and speed if ball hits either paddle
        if self.ball.h_speed < 0:
            self.ball.check_paddle_hit(self.l_paddle)
        else:
            self.ball.check_paddle_hit(self.r_paddle)

        # End point if ball hits either end
        if self.ball.check_ends_hit() == "left":
            self.end_point("left")
        if self.ball.check_ends_hit() == "right":
            self.end_point("right")

        self.l_paddle.move()
        self.r_paddle.move()


    def end_point(self, side: str = None):
        """
        Update score and transition to GAME_OVER screen if game has been won.
        Reset ball and paddle positions.
        """
        # Update scores and check if game won
        if side == "left":
            self.score_p2 += 1
            if self.game_over_condition():
                self.winner = "Player 2"
                self.current_state = GAME_OVER
            else:
                self.current_state = BETWEEN_POINTS
        elif side == "right":
            self.score_p1 += 1
            if self.game_over_condition():
                self.winner = "Player 1"
                self.current_state = GAME_OVER
            else:
                self.current_state = BETWEEN_POINTS
        else:
            raise ValueError(f"`end_point()` expected a string of either 'left' or 'right'")

        # Paddle speeds reset to 0
        self.l_paddle.v_speed = self.r_paddle.v_speed = 0

        # Paddles moved back to centre
        self.l_paddle.rect.top = self.r_paddle.rect.top = (self.screen_dims[1] // 2 - self.r_paddle.rect.height // 2)

        # Random starting position and direction for ball
        self.ball.rect.left = self.ball.screen_width // 2 - self.ball.side_length // 2
        self.ball.rect.top = random.randint(0, self.ball.screen_height)
        self.ball.h_speed = random.choice([-1, 1]) * 3
        self.ball.v_speed = random.choice([-1, 1]) * 5


    def game_over_condition(self):
        """Check if winning conditions have been fulfilled - return a boolean."""
        if self.score_p1 >= self.winning_score or self.score_p2 >= self.winning_score:
            if abs(self.score_p1 - self.score_p2) >= 2:
                return True

    def handle_events(self):
        """Handle transitions between game states and game control logic."""
        for event in pygame.event.get():
            # Closing the game
            if event.type == pygame.QUIT:
                return False

            # Start screen
            if self.current_state == START_SCREEN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.current_state = PLAYING

            # Playing screen
            if self.current_state == PLAYING:
                # Logic for key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == self.key_bindings.left_up:
                        if self.l_paddle.v_speed >= 0:
                            self.l_paddle.v_speed += 2
                        else:
                            self.l_paddle.v_speed = 0
                    elif event.key == self.key_bindings.left_down:
                        if self.l_paddle.v_speed <= 0:
                            self.l_paddle.v_speed -= 2
                        else:
                            self.l_paddle.v_speed = 0
                    elif event.key == self.key_bindings.right_up:
                        if self.r_paddle.v_speed >= 0:
                            self.r_paddle.v_speed += 2
                        else:
                            self.r_paddle.v_speed = 0
                    elif event.key == self.key_bindings.right_down:
                        if self.r_paddle.v_speed <= 0:
                            self.r_paddle.v_speed -= 2
                        else:
                            self.r_paddle.v_speed = 0

                # Move ball and paddles
                self.update_game_objects()

            # Between Points screen
            if self.current_state == BETWEEN_POINTS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.current_state = PLAYING

            # Game Over screen
            if self.current_state == GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Reset scores
                    self.score_p1, self.score_p2 = 0, 0
                    self.current_state = START_SCREEN

        return True


    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Handle events
            running = self.handle_events()

            # Draw screen based on current state
            if self.current_state == START_SCREEN:
                self.draw_start_screen()
            elif self.current_state == PLAYING:
                self.update_game_objects()
                self.draw_playing_screen()
            elif self.current_state == BETWEEN_POINTS:
                self.draw_between_points_screen()
            elif self.current_state == GAME_OVER:
                self.draw_game_over_screen()

            # Update display
            pygame.display.flip()

            # Clear event queue?

            # Control frame rate
            self.clock.tick(self.fps)

        # Quit the game
        pygame.quit()



class KeyBindings:
    def __init__(self):
        """
        Initialise default key bindings for the Pong game.

        Sets up default control keys for both players:
        - Left player: W (up), S (down)
        - Right player: Up arrow (up), Down arrow (down)

        Attributes:
            left_up (int): Pygame key constant for left player's up movement
            left_down (int): Pygame key constant for left player's down movement
            right_up (int): Pygame key constant for right player's up movement
            right_down (int): Pygame key constant for right player's down movement
        """
        # Default key bindings
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

        Attributes:
            screen_width (int): Screen width
            screen_height (int): Screen height
            rect (pygame.Rect): Ball's rectangular representation
            h_speed (int): Horizontal speed
            v_speed (int): Vertical speed
            color (str): Ball color
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

        Attributes:
            screen_width (int): Screen width
            screen_height (int): Screen height
            left (bool): Paddle side (left or right)
            width (int): Paddle width
            rect (pygame.Rect): Paddle's rectangular representation
            color (str): Paddle color
            _v_speed (int): Vertical speed (with setter for range validation)
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


if __name__ == "__main__":
    game = Game()
    game.run()

