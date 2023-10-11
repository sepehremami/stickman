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
            "add miner 00:00:02",  # 350
            "add miner 00:00:03",  # 350
            "add miner 00:00:04",  # 350
            "money-status 00:00:10",  # 50
            "money-status 00:10:03",  # 250
            "money-status 00:20:02",  # 450
            "money-status 00:30:06",  # 950
            "money-status 00:40:07",  # 3
            "money-status 00:50:08",  # 3
            "money-status 01:00:09",
            # "money-status 03:00:03",  # 5
            # "money-status 03:00:04",  # 6
        ]
        mock_input.side_effect = l
        print(len(l))
        self.game.run(len(l), 40)

        logging.info(mock_stdout.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "expected output here\n")


if __name__ == "__main__":
    unittest.main()
