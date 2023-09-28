import logging
from typing import Callable
from .state import StateManager


class Counter:
    idx = 0

    @classmethod
    def allocate_id(cls) -> "int":
        cls.idx += 1
        return cls.idx


class BaseArmy:
    """
    tracking army units is handled in this class
    """

    idx = 0

    total_work_unit = 0

    def __init__(self, work_unit) -> None:
        logging.info(f"{work_unit} comming in are ava")
        self.__class__.total_work_unit += work_unit
        logging.info(f"{self.__class__.total_work_unit} work units are ava")

    @classmethod
    def allocate_id(cls):
        cls.idx += 1
        return cls.idx


class ArmyUnit(BaseArmy):
    hp: int = None
    price: int = None
    cooldown: int = None
    created = None
    _callback: Callable = None
    work_unit = 1

    def __init__(self, timestamp) -> None:
        logging.info(
            f"inside __init__ of {self.__class__.__name__} class \
            at {timestamp}, {self.__class__.idx} is the id and {super().allocate_id()} is the allocated_id"
        )
        self.__class__.created = timestamp
        self.__class__.idx = Counter.allocate_id()
        super().__init__(self.__class__.work_unit)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} Troop object ({self.hp}) at your service"

    def __len__(self):
        return self.__class__.work_unit


class Miner(ArmyUnit):
    """
    every 10 seconds after initialization \
          call the callback function 
    """

    hp = 100
    price = 150  # coins
    collected_money = 100  # coins
    cooldown = 10  #
    work_unit = 2

    def callback_yield_coin(self):
        StateManager.collect_money(self.__class__.collected_money)
        logging.info(f"{self.__class__.__name__} number {self.idx} yielding coin")

    # yield_coin = sign_function(yield_coin)
    _callback = callback_yield_coin


class Swordwrath(ArmyUnit):
    hp = 100
    price = 125
    cooldown = 1
    power = 20

    def callback_attack_dragon(self):
        StateManager.attack_dragon(self.power)
        logging.info(
            f"{self.__class__.__name__} number {self.idx} is attacking the dragon"
        )

    _callback = callback_attack_dragon

    # TODO: take the callback funtion by the callback_ in the function name instead of doing this


class Archidon(Swordwrath):
    hp = 80
    price = 300
    power = 10


class Spearton(Swordwrath):
    hp = 250
    price = 500
    work_unit = 2
    power = 35


class Magikill(Swordwrath):
    hp = 80
    price = 1200
    work_unit = 4
    power = 200


class Giant(Swordwrath):
    hp = 1000
    price = 1500
    work_unit = 4
    power = 150
