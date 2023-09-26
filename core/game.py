from datetime import datetime
import logging
from .state import StateManager
from .army import Miner


class CommandManager:
    @staticmethod
    def add(info, timestamp):
        role: str = info.pop()
        troop = eval(f"{role.capitalize()}(timestamp)")
        StateManager.add_troop(troop)

    @staticmethod
    def money_status(*args):
        return StateManager.money_status()

    @staticmethod
    def run(move, info, timestamp):
        controller = getattr(CommandManager, move)
        result = controller(info, timestamp)
        print(result)


class Game:
    def __init__(self) -> None:
        pass

    def next_turn(self, turn):
        pass

    def combat(self):
        pass

    def end_game(self):
        pass

    @staticmethod
    def handle_input(userin):
        userin = userin.split()
        timestamp = userin.pop()
        func_name: str = userin.pop(0).replace("-", "_")

        time_obj = datetime.strptime(timestamp, "%M:%S:%f")

        return func_name, userin, time_obj

    def run(self):
        logging.info("Inside Game.run")
        while True:
            move, info, timestamp = self.handle_input(input())
            StateManager.add_event(move, info, timestamp)
            CommandManager.run(move, info, timestamp)


"""

write the main class as a context manager that has a time attr

"""
