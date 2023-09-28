import os
import sys
import unittest
import logging
from unittest.mock import patch
from io import StringIO


# Add the parent directory of mypackage to the Python path
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
    def test_game_run(self, mock_input, mock_stdout):
        # Mock user input
        l = [
            # "12 132",
            "money-status 00:19:999",
            "money-status 00:20:001",
            "add miner 00:20:002",
            "money-status 00:20:003",
            "add miner 00:20:004",
            "money-status 00:20:005",
            "add miner 00:20:006",
            "money-status 00:20:007",
            "money-status 00:20:009",
            "money-status 2:00:00",
            "add miner 2:20:008",
            "add miner 2:29:010",
            "add miner 2:30:011",
            "add giant 4:0:0",
            "add giant 4:20:0",
            "add giant 4:40:2",
            "add giant 5:20:2",
            "add giant 5:40:2",
            "add giant 6:0:3",
            "add giant 7:0:4",
            "add giant 8:0:5",
            "army-status 8:19:0",
            "add giant 8:20:5",
            "army-status 8:21:0",
            "add giant 8:40:5",
            "army-status 9:1:0",
        ]
        mock_input.side_effect = l

        self.game.run(26, 123)

        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
        logging.info(mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
