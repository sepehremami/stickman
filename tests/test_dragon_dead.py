import os
import sys
import unittest
import logging
from unittest.mock import patch
from io import StringIO

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
from new_2 import Game


file_path = "log/test.log"


logger = logging.getLogger("my_logger")
logger.setLevel(logging.NOTSET)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
            "add miner 01:00:03",  # 3
            "add swordwrath 01:00:04",  # 3
            "add miner 01:04:06",  # 3
            "add miner 01:05:07",  # 3
            "add miner 01:06:08",  # 3
            "army-status 01:07:09",
            "add miner 03:00:03",  # 5
            "add miner 03:00:04",  # 6
            "add miner 03:00:05",
            "money-status 13:00:5",
            "add giant 14:00:05",  # 7  # 4
            "add giant 14:01:05",  # 4
            "add giant 14:02:05",  # 4
            "add giant 14:03:05",  # 4
            "money-status 14:00:01",
            "damage 1 150 17:5:11",
            "damage 2 150 17:6:21",
        ]
        mock_input.side_effect = l
        print(len(l))
        self.game.run(len(l), 40)

        logging.info(mock_stdout.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")


if __name__ == "__main__":
    unittest.main()
