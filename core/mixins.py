# from .army import Miner
# from .types import Miner


class StateMineMixin:
    waiting = []

    @classmethod
    def check_mine_capacity(cls):
        cap = sum(mine.capacity for mine in cls.mines)
        if cap < 8:
            return True
        return False

    @classmethod
    def get_mine(cls):
        for mine in cls.mines:
            if not mine.is_full():
                return mine

    @classmethod
    def allocate_miner(cls, miner):
        if cls.check_mine_capacity():
            mine = cls.get_mine()
            mine.add_miner(miner)
            cls.add_callbacks(miner)
        else:
            cls.waiting.append(miner)
            return True

    @classmethod
    def dead_miner(cls, miner):
        for mine in cls.mines:
            mine.remove_miner(miner.idx)

        if cls.waiting:
            for miner in cls.waiting:
                cls.allocate_miner(miner)
