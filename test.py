import os
import unittest
import logging
from unittest.mock import patch
from io import StringIO
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
        mock_input.side_effect = [
            # "12 132",
            "money-status 00:19:999",
            "money-status 00:20:001",
            "add miner 00:20:002",
            "money-status 00:20:003",
            "add miner 00:20:004",
            "money-status 00:20:005",
            "add miner 00:20:006",
            "money-status 00:20:007",
            "add miner 00:20:008",
            "money-status 00:20:009",
            "add miner 00:29:010",
            "add miner 00:30:011",
        ]

        # Run the game
        self.game.run(12, 123)

        # Assert the expected output
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
        logging.info(mock_stdout.getvalue())


    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_game_run2(self, mock_input, mock_stdout):
        # Mock user input
        mock_input.side_effect = [
            "money-status 00:00:01",
            "add swordwrath 00:01:002",
            "money-status 00:2:03",
            "add miner 00:2:04",
            "money-status 0:12:05",
        ]

        # Run the game
        self.game.run(5, 100)

        # Assert the expected output
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
        logging.info(mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
