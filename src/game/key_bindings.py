import pygame

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

