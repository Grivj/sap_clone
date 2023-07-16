import logging

from game import Game

logging.basicConfig(
    level=logging.DEBUG, format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    game = Game()
    game.run()
