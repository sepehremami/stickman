# from .army import Miner
from .types import Miner


class StateMineMixin:
    @classmethod
    def get_mine(cls):
        for mine in cls.__mines:
            if not mine.is_full():
                return mine

    @classmethod
    def check_mine_capacity(cls):
        capacity = sum(i.capacity for i in cls.__mines)
        if capacity >= 8:
            return False
        return True

    @classmethod
    def allocate_miner(cls, troop_obj):
        if not isinstance(troop_obj, Miner):
            return
        miner = troop_obj
        mine = cls.get_mine()
        mine.add_miner(miner)

    @classmethod
    def remove_from_mine(cls, troop_id):
        for mine in cls.__mines:
            miner = mine.remove_miner(troop_id)
            if isinstance(miner, Miner):
                return miner

    @classmethod
    def check_is_miner(cls, troop):
        if isinstance(troop, Miner):
            return True
