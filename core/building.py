class BaseBuilding:
    def __init__(self, tag) -> None:
        self.tag = tag
        self.capacity = 0
        self.miners = []


class Mine(BaseBuilding):
    def add_miner(self, miner):
        self.miners.appned(miner)
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
