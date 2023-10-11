import os
import logging
from core.state import StateManager
from core.game import Game

file_path = "log/app.log"

try:
    os.remove(file_path)
except OSError as e:
    print(f"Error: {e.filename} - {e.strerror}")


logging.basicConfig(
    filename="log/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


if __name__ == "__main__":
    game = Game()
    command_num, dragon_health = map(int, input().split())
    logging.info("Game started!")
    game.run(command_num, dragon_health)
