import logging
from typing import Callable
from .state import StateManager


class BaseArmy:
    """
    tracking army units is handled in this class
    """

    total_work_unit = 0

    def __init__(self, work_unit) -> None:
        logging.info(f"{work_unit} comming in are ava")
        self.__class__.total_work_unit += work_unit
        logging.info(f"{self.__class__.total_work_unit} work units are ava")


class ArmyUnit(BaseArmy):
    hp: int = None
    price: int = None
    cooldown: int = None
    created = None
    _callback: Callable = None
    idx = 0

    def __init__(self, timestamp) -> None:
        self.__class__.created = timestamp
        self.idx = self.__class__.idx + 1
        super().__init__(self.__class__.work_unit)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} Troop object ({self.hp}) at your service"


class Miner(ArmyUnit):
    """
    every 10 seconds after initialization \
          call the callback function 
    """

    hp = 100
    price = 150  # coins
    collected_money = 100  # coins
    cooldown = 10  # seconds\
    work_unit = 1

    def yield_coin(self):
        StateManager.collect_money(self.__class__.collected_money)
        logging.info(f"{self.__class__.__name__} yielding coin")
        pass

    # yield_coin = sign_function(yield_coin)
    _callback = yield_coin


class Swordwrath(BaseArmy):
    pass


class Archidon(BaseArmy):
    pass


class Spearton(BaseArmy):
    pass


class Magikill(BaseArmy):
    pass


class Giant(BaseArmy):
    pass
