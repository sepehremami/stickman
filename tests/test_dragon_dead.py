import os
import sys
import unittest
import logging
from unittest.mock import patch
from io import StringIO

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from core.game import Game


file_path = "log/test.log"

try:
    os.remove(file_path)
except OSError as e:
    print(f"Error: {e.filename} - {e.strerror}")


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    filename="log/test.log",
)


class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        pass

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_game_run2(self, mock_input, mock_stdout):
        # Mock user input

        l = [
            "money-status 00:00:01",
            "add miner 00:00:02",  # 1
            "add miner 00:00:03",  # 2
            "add miner 1:00:03",  # 3
            "add swordwrath 1:00:04",  # 3
            "add miner 1:004:06",  # 3
            "add miner 1:005:07",  # 3
            "add miner 1:006:08",  # 3
            "army-status 1:00:09",
            "add miner 3:00:03",  # 5
            "add miner 3:00:04",  # 6
            "add miner 3:00:05",
            "money-status 13:0:5",
            "add giant 14:00:05",  # 7  # 4
            "add giant 14:01:05",  # 4
            "add giant 14:02:05",  # 4
            "add giant 14:03:05",  # 4
            "money-status 14:00:01",
            "mine 17:2:0",
            "damage 1 150 7:5:11",
            "damage 2 150 7:6:21",
            "mine 7:7:1",
        ]
        mock_input.side_effect = l
        # Run the game
        self.game.run(len(l), 40)

        # Assert the expected output
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
        logging.info(mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
