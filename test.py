import io
import unittest
from unittest.mock import patch
from io import StringIO
from core.game import Game

import logging

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

        # Assert the expected output

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


if __name__ == "__main__":
    unittest.main()
