import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypong.game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()