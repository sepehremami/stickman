import logging
from .state import StateManager
from .army import ArmyUnit, Miner


class CommandManager:
    @staticmethod
    def add(info, timestamp):
        role: str = info.pop()
        price = int(eval((f"{role.capitalize()}.price")))
        if price > StateManager.money_status():
            print("not enough money")
        else:
            troop = eval(f"{role.capitalize()}(timestamp)")
            StateManager.add_troop(troop)
            print(troop.total_work_unit)

    @staticmethod
    def damage(info, timestamp):
        damage = int(info.pop())
        idx = int(info.pop())
        troop = StateManager.damage(idx, damage)
        isinstance(troop, ArmyUnit) and print(troop.hp)
        print("dead")

    @staticmethod
    def money_status(*args):
        return StateManager.money_status()

    @staticmethod
    def run(move, info, timestamp):
        controller = getattr(CommandManager, move)
        result = controller(info, timestamp)
        result is not None and print(result)


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
        logging.info(f"user input : {userin}")
        userin = userin.split()
        timestamp = userin.pop()
        func_name: str = userin.pop(0).replace("-", "_")

        time_seconds = (lambda l: l[0] * 60 + l[1] + l[2] / 1000)(
            list(map(int, timestamp.split(":")))
        )

        return func_name, userin, time_seconds

    def run(self, num, dragon_health):
        logging.info("Inside Game.run")
        for _ in range(num):
            move, info, timestamp = self.handle_input(input())
            StateManager.add_event(move, info, timestamp)
            CommandManager.run(move, info, timestamp)


"""

write the main class as a context manager that has a time attr

"""
