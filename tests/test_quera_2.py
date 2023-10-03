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

    # @patch("sys.stdout", new_callable=StringIO)
    # @patch("builtins.input")
    # def test_game_run(self, mock_input, mock_stdout):
    #     # Mock user input
    #     mock_input.side_effect = [
    #         # "12 132",
    #         "money-status 00:19:999",
    #         "money-status 00:20:001",
    #         "add miner 00:20:002",
    #         "money-status 00:20:003",
    #         "add miner 00:20:004",
    #         "money-status 00:20:005",
    #         "add miner 00:20:006",
    #         "money-status 00:20:007",
    #         "add miner 00:20:008",
    #         "money-status 00:20:009",
    #         "add miner 00:29:010",
    #         "add miner 00:30:011",
    #     ]

    #     # Run the game
    #     self.game.run(12, 123)

    #     # Assert the expected output
    #     self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
    #     logging.info(mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_game_run2(self, mock_input, mock_stdout):
        # Mock user input

        mock_input.side_effect = [
            "money-status 00:00:01",
            "add miner 00:00:02",
            "add miner 00:00:03",
            "add miner 00:00:04",
            "money-status 00:00:05",
            "add miner 00:10:06",
            "add miner 00:10:07",
            "add swordwrath 02:00:08",
            "add archidon 02:00:09",
            "army-status 02:00:10",
            "add spearton 02:00:11",
            "add magikill 02:00:12",
            "add giant 02:00:13",
            "enemy-status 02:00:14",
            "army-status 02:00:15",
            "damage 1 10 02:01:16",
            "damage 2 10 02:01:17",
            "damage 3 20 02:01:18",
            "damage 4 3 02:01:19",
            "damage 5 15 02:01:20",
            "damage 6 1000 02:01:21",
            "damage 7 60 02:01:22",
            "damage 8 16 02:01:23",
            "damage 16 16 02:01:24",
            "enemy-status 02:01:25",
            "army-status 02:01:26",
            "damage 6 17 02:31:27",
            "enemy-status 02:31:28",
            "damage 7 18 02:31:29",
            "damage 8 19 02:31:30",
            "damage 9 20 02:31:31",
            "enemy-status 02:31:32",
            "army-status 02:31:33",
            # "money-status 2:34:0",
        ]

        # Run the game
        self.game.run(33, 10000)

        # Assert the expected output
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")
        logging.info(mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
