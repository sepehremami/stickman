import logging
from .state import StateManager
from .army import *


class CommandManager:
    @staticmethod
    def add(info, timestamp):
        role: str = info.pop()
        troop_obj = eval((f"{role.capitalize()}"))

        if troop_obj.price > StateManager.get_money_status():
            return "not enough money"
        elif StateManager.check_army_capacity(troop_obj):
            return "too many army"
        elif role == "miner":
            miner = eval(f"{role.capitalize()}(timestamp)")
            StateManager.add_miner(miner)
            return miner.idx
        else:
            troop = eval(f"{role.capitalize()}(timestamp)")
            StateManager.add_troop(troop)
            return troop.idx

    @staticmethod
    def damage(info, timestamp):
        damage = int(info.pop())
        idx = int(info.pop())
        result = StateManager.damage(idx, damage, timestamp)
        return result

    @staticmethod
    def money_status(*args):
        return StateManager.get_money_status()

    @staticmethod
    def enemy_status(*args):
        return StateManager.get_enemy_status()

    @staticmethod
    def army_status(*args):
        army = StateManager.get_troops()
        stats = []
        troops = ["Miner", "Swordwrath", "Archidon", "Spearton", "Magikill", "Giant"]
        for i in troops:
            stats.append(
                len(list(troop for _, troop in army.items() if type(troop) is eval(i)))
            )
        return stats

    @staticmethod
    def mine(*args):
        mines = [mine.capacity for mine in StateManager.mines]
        return mines

    @staticmethod
    def run(move, info, timestamp):
        controller = getattr(CommandManager, move)
        result = controller(info, timestamp)
        if result:
            return result


class Game:
    def __init__(self) -> None:
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
        StateManager.set_state(num, dragon_health)

        for _ in range(num):
            move, info, timestamp = self.handle_input(input())
            end = StateManager.add_event(move, info, timestamp)
            if StateManager.game_over:
                print("game over")

            res = CommandManager.run(move, info, timestamp)
            print(*res) if isinstance(res, list) else print(res)


"""

write the main class as a context manager that has a time attr

"""
