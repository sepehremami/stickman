# from .army import Miner
# from .types import Miner


class StateMineMixin:
    waiting = []

    @classmethod
    def check_mine_capacity(cls):
        capacity = sum(i.capacity for i in cls.mines)
        if capacity >= 8:
            return False
        return True

    @classmethod
    def allocate_miner(cls, troop_obj):
        if troop_obj.__class__.__name__ == "Miner":
            miner = troop_obj
            mine = cls.get_mine()
            if mine is None:
                cls.add_to_waiting(miner)
                return miner
            else:
                mine.add_miner(miner)
                return True

    @classmethod
    def get_mine(cls):
        for mine in cls.mines:
            if not mine.is_full():
                return mine
        return None

    @classmethod
    def remove_from_mine(cls, troop_obj):
        for mine in cls.mines:
            if troop_obj.__class__.__name__ == "Miner":
                miner = mine.remove_miner(troop_obj.idx)
                return miner

    @classmethod
    def check_is_miner(cls, troop_obj):
        if troop_obj.__class__.__name__ == "Miner":
            return True

    @classmethod
    def add_to_waiting(cls, miner):
        cls.waiting.append(miner)
