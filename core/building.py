import logging


class BaseBuilding:
    def __init__(self, tag) -> None:
        self.tag = tag
        self.capacity = 0
        self.miners = []
        # ids of miners

    def __repr__(self) -> str:
        return f"{{{self.__class__.__name__}-{self.tag}-capacity: {self.capacity}-miners: {self.miners}}}"


class Mine(BaseBuilding):
    def add_miner(self, miner):
        logging.warning(f"inside add_miner {miner}, {self.__repr__()}")
        self.miners.append(miner.idx)
        self.capacity += 1
        return self.miners

    def get_miners_id(self):
        id_list = []
        for miner in self.miners:
            self.miners.append(miner.idx)
        return id_list

    def is_full(self):
        if len(self.miners) == 2:
            return True
        return False

    def remove_miner(self, miner_id):
        for miner in self.miners:
            if miner == miner_id:
                self.miners.remove(miner)
                self.capacity -= 1
                return self.miners
