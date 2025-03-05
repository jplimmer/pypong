import pygame
import random
from typing import Tuple, Optional
import logging
from config.settings import (
    SCREEN_DIMENSIONS,
    FPS,
    WINNING_SCORE,
    GameState
)
from .key_bindings import KeyBindings
from .screens.start_screen import StartScreen
from .screens.playing_screen import PlayingScreen
from .screens.between_points_screen import BetweenPointsScreen
from .screens.game_over_screen import GameOverScreen
from .objects.ball import Ball
from .objects.paddle import Paddle

class Game:
    def __init__(self, screen_dims: Tuple[int, int] = SCREEN_DIMENSIONS, fps: int = FPS, winning_score: int = WINNING_SCORE):
        """
        Initialise the PyPong game with game setup, configuration, and initial game state.

        Args:
            screen_dims (Tuple[int, int], optional): Screen dimensions. Defaults to SCREEN_DIMENSIONS.
            fps (int, optional): Frames per second. Defaults to FPS.
            winning_score (int, optional): Score required for one player to win the game. Defaults to WINNING_SCORE.
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Pygame initialisation
        pygame.init()
        pygame.display.set_caption("PyPong")

        # Pygame screen setup
        self.screen_dims = screen_dims
        self.screen = pygame.display.set_mode(self.screen_dims)
        self.clock = pygame.time.Clock()
        self.fps = fps

        # Screens
        self.start_screen = StartScreen(screen_dims)
        self.playing_screen = PlayingScreen(screen_dims)
        self.between_points_screen = BetweenPointsScreen(screen_dims)
        self.game_over_screen = GameOverScreen(screen_dims)

        # Game state management
        self.current_state = GameState.START_SCREEN
        self.winning_score = winning_score
        self.winner: Optional[str] = None

        # Scoring
        self.score_p1 = 0  # p1 is left paddle
        self.score_p2 = 0

        # Game objects
        self.key_bindings = KeyBindings()
        self.ball = Ball(screen_size=self.screen_dims)
        self.l_paddle = Paddle(left=True, screen_size=self.screen_dims) #p1
        self.r_paddle = Paddle(left=False, screen_size=self.screen_dims)

    def reset_game(self):
        """Reset the game to its initial state."""
        # Reset scores
        self.score_p1 = 0
        self.score_p2 = 0
        self.winner = None
        self.current_state = GameState.START_SCREEN

        # Reset game objects
        self.reset_objects()

    def reset_objects(self):
        """Reset ball and paddles. Randomised starting direction for Ball."""
        # Paddle speeds reset to 0
        self.l_paddle.v_speed = self.r_paddle.v_speed = 0

        # Paddles moved back to centre
        self.l_paddle.rect.top = self.r_paddle.rect.top = (self.screen_dims[1] // 2 - self.r_paddle.rect.height // 2)

        # Random starting position and direction for ball
        self.ball.rect.left = self.ball.screen_width // 2 - self.ball.side_length // 2
        self.ball.rect.top = random.randint(0, self.ball.screen_height)
        self.ball.h_speed = random.choice([-1, 1]) * 3
        self.ball.v_speed = random.choice([-1, 1]) * 5

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
        Update score and transition to GAME_OVER screen if game has been won. Reset ball and paddle positions.

        Args:
            side (str, optional): Side which lost the point ("left" or "right").
        """
        # Update scores and check if game won
        if side == "left":
            self.score_p2 += 1
            if self.game_over_condition():
                self.winner = "Player 2"
                self.current_state = GameState.GAME_OVER
            else:
                self.current_state = GameState.BETWEEN_POINTS
        elif side == "right":
            self.score_p1 += 1
            if self.game_over_condition():
                self.winner = "Player 1"
                self.current_state = GameState.GAME_OVER
            else:
                self.current_state = GameState.BETWEEN_POINTS
        else:
            raise ValueError(f"`end_point()` expected a string of either 'left' or 'right'")

        self.reset_objects()

    def game_over_condition(self) -> bool:
        """Check if winning conditions have been fulfilled - return a boolean."""
        if self.score_p1 >= self.winning_score or self.score_p2 >= self.winning_score:
            if abs(self.score_p1 - self.score_p2) >= 2:
                return True
        return False

    def _handle_start_screen_events(self, event):
        """
        Handle events specific to the start screen.

        Args:
            event (pygame.event.Event): Pygame event to process
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.current_state = GameState.PLAYING
            self.logger.info("Game started")

    def _handle_playing_screen_events(self, event):
        """
        Handle events specific to the playing screen.

        Args:
            event (pygame.event.Event): Pygame event to process
        """
        if event.type == pygame.KEYDOWN:
            # Left paddle controls
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

            # Right paddle controls
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

    def _handle_between_points_events(self, event):
        """
        Handle events specific to the between points screen.

        Args:
            event (pygame.event.Event): Pygame event to process
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.current_state = GameState.PLAYING
            self.logger.info("Continuing to next point")

    def _handle_game_over_events(self, event):
        """
        Handle events specific to the game over screen.

        Args:
            event (pygame.event.Event): Pygame event to process
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reset_game()
            self.logger.info("Restarting game")

    def handle_events(self) -> bool:
        """
        Handle pygame events and state transitions.

        Returns:
            bool: False if game should quit, True otherwise
        """
        for event in pygame.event.get():
            # Closing the game
            if event.type == pygame.QUIT:
                return False

            # State-specific event handling
            if self.current_state == GameState.START_SCREEN:
                self._handle_start_screen_events(event)
            elif self.current_state == GameState.PLAYING:
                self._handle_playing_screen_events(event)
            elif self.current_state == GameState.BETWEEN_POINTS:
                self._handle_between_points_events(event)
            elif self.current_state == GameState.GAME_OVER:
                self._handle_game_over_events(event)

            # Update game objects if in playing state
            if self.current_state == GameState.PLAYING:
                self.update_game_objects()

        return True

    def draw_start_screen(self):
        """Render start screen."""
        self.start_screen.render(self.screen, self.key_bindings)

    def draw_playing_screen(self):
        """Render playing screen."""
        self.playing_screen.render(self.screen, self.ball, self.l_paddle, self.r_paddle)

    def draw_between_points_screen(self):
        """Render between points screen."""
        self.between_points_screen.render(
            self.screen,
            (self.score_p1, self.score_p2),
            WINNING_SCORE
        )

    def draw_game_over_screen(self):
        """Render game over screen."""
        self.game_over_screen.render(
            self.screen,
            self.winner,
            (self.score_p1, self.score_p2)
        )

    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Handle events
            running = self.handle_events()

            # Draw screen based on current state
            if self.current_state == GameState.START_SCREEN:
                self.draw_start_screen()
            elif self.current_state == GameState.PLAYING:
                self.update_game_objects()
                self.draw_playing_screen()
            elif self.current_state == GameState.BETWEEN_POINTS:
                self.draw_between_points_screen()
            elif self.current_state == GameState.GAME_OVER:
                self.draw_game_over_screen()

            # Update display
            pygame.display.flip()

            # Clear event queue
            pygame.event.clear()

            # Control frame rate
            self.clock.tick(self.fps)

        # Quit the game
        pygame.quit()

