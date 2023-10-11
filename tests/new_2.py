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


from typing import Any, Callable


class Callback:
    def __init__(
        self,
        name,
        func: Callable,
        troop_id,
        cooldown,
        timestamp,
        last_command_timestamp,
    ) -> None:
        self.name = name
        self.func = func
        self.troop_id = troop_id
        self.cooldown = cooldown
        self.timestamp = timestamp
        self.last_command_timestamp = last_command_timestamp

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        logging.info(f"inside callback {self.name}")
        logging.info(
            f"\n\tself.timestamp: {self.timestamp}\n\t\tself.cooldown: {self.cooldown}\n\t\tself.last_command_timestamp: {self.last_command_timestamp}"
        )
        return self.func(*args, **kwds)

    def __repr__(self) -> str:
        return f"{self.func.__name__.capitalize()} at {self.timestamp}"


from functools import update_wrapper


def check_dragon_dead(func, *args, **kwargs):
    def wrapper(cls, *args, **kwds):
        if cls.DRAGON == 0:
            cls.game_over = True

        result = func(cls, args[0], args[1], args[2])
        return result

    return update_wrapper(wrapper, func)


class StateMineMixin:
    @classmethod
    def check_mine_capacity(cls):
        # cap = sum(mine.capacity for mine in cls.mines)
        cap = 0
        for mine in cls.mines:
            cap += mine.capacity

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
            logging.warning(f"inside allocate_miner: {mine}")
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
            logging.warning(f"inside dead_miner: {cls.waiting}")
            cls.allocate_miner(cls.waiting.pop())


def goverment_help():
    StateManager.collect_money(StateManager.GOV_HELP)
    logging.debug(
        f"inside goverment_help at timestamp: {StateManager.last_command_timestamp}"
    )


class StateManager(StateMineMixin):
    __money = 500
    __callbacks = [
        Callback(
            "goverment_help",
            goverment_help,
            0,
            cooldown=20,
            timestamp=0,
            last_command_timestamp=0,
        )
    ]

    waiting = []
    troops = {}
    __events = []
    mines = []
    GOV_HELP = 180
    DRAGON = 0
    number_of_turns = 0
    game_over = False
    last_command_timestamp = 0

    @classmethod
    def get_troops(cls):
        logging.info(f"all troops: {cls.troops}")
        return cls.troops

    @classmethod
    def set_state(cls, turn, dragon_health):
        # set Dragon health
        cls.DRAGON = dragon_health

        # Generate 4 mines
        for tag in range(4):
            cls.mines.append(Mine(tag))

        # set turns (just in case)
        cls.number_of_turns = turn

        logging.info(
            f"\n\t\tdragon health: {cls.DRAGON}\n\t\t dragon input: {dragon_health}\n\t\t"
        )

    @classmethod
    @check_dragon_dead
    def add_event(cls, move, info, timestamp):
        cls.__events.append((move, timestamp))
        cls.call_callbacks(timestamp=timestamp)
        cls.update_time(timestamp)

    @classmethod
    def update_time(cls, timestamp):
        cls.last_command_timestamp = timestamp

    @classmethod
    def get_money_status(cls):
        return cls.__money

    @classmethod
    def get_enemy_status(cls):
        return cls.DRAGON

    @classmethod
    def get_army_status(cls):
        units = 0
        army = StateManager.get_troops()
        for _, troop in army.items():
            units += troop.work_unit
        logging.debug(f"there are a total of {units} units")
        return units

    @classmethod
    def check_army_capacity(cls, troop_obj):
        units = cls.get_army_status()
        if units + troop_obj.work_unit >= 50:
            return True

    @classmethod
    def collect_money(cls, money):
        logging.warning(
            f"inside collect_money: {money} now we've got {cls.__money}, sum: {cls.__money + money}\nthis is timestamp: {StateManager.last_command_timestamp}"
        )
        cls.__money += money

    @classmethod
    def add_troop(cls, troop_obj):
        cls.__money -= troop_obj.price

        cls.add_callbacks(troop_obj)

        cls.troops[troop_obj.idx] = troop_obj

        logging.info(troop_obj)
        logging.info(f"callbacks are here: {cls.__callbacks}")

    @classmethod
    def add_miner(cls, miner):
        cls.__money -= miner.price
        waiting = cls.allocate_miner(miner)
        # cls.waiting.append(miner)
        cls.troops[miner.idx] = miner

    @classmethod
    def add_callbacks(cls, troop_obj):
        callback = troop_obj._callback

        cls.__callbacks.append(
            Callback(
                troop_obj.__repr__(),
                callback,
                troop_obj.idx,
                troop_obj.cooldown,
                troop_obj.created,
                cls.last_command_timestamp,
            )
        )

    @classmethod
    def damage(cls, troop_id, damage: int, timestamp):
        troop = cls._get_troop_by_id(troop_id=troop_id)
        if troop and type(troop) is not str:
            if damage >= troop.hp:
                dead_troop = cls.troops.pop(troop_id)
                cls.remove_troop_callbacks(dead_troop)
                if dead_troop.__class__.__name__ == "Miner":
                    cls.dead_miner(dead_troop)
                    logging.warning(f"inside damage: {dead_troop}")

                logging.info(f"{troop} is dead at {timestamp}")
                return "dead"
            else:
                troop.hp -= damage
                return troop.hp
        return troop

    @classmethod
    def _get_troop_by_id(cls, troop_id):
        try:
            logging.debug(
                f"this is the troop you are looking for (possibly) {cls.troops[troop_id]}"
            )
            return cls.troops[troop_id]
        except KeyError:
            logging.debug(f"troop with {troop_id} id does not exist")
            return "no matter"

    @classmethod
    def remove_troop_callbacks(cls, troop):
        for callback in cls.__callbacks:
            if callback.troop_id == troop.idx:
                cls.__callbacks.remove(callback)
                logging.warning(
                    f"{callback.func.__name__} removed from callback list for troop with id:{troop.idx}"
                )

    @classmethod
    def _check_dragon_dead(cls):
        if cls.DRAGON == 0:
            return "dead"
        return False

    @classmethod
    def attack_dragon(cls, damage):
        if check := cls._check_dragon_dead() and damage >= cls.DRAGON:
            cls.DRAGON = 0
            return check

        else:
            cls.DRAGON -= damage
            logging.warning(
                f"dragon is taking {damage} damage; its health is: {cls.DRAGON} at timestamp {cls.last_command_timestamp}"
            )

    @classmethod
    def call_callbacks(cls, timestamp):
        for callback in cls.__callbacks:
            logging.info(f"inside call_callbacks, callback: {callback}")

            while True:
                created = callback.timestamp
                s = round(created + callback.cooldown, 4)
                logging.info(f"created: {created}, s: {s}")
                if timestamp >= s:
                    callback()
                    callback.timestamp = s
                else:
                    break

        #     if should_repeat >= timestamp:
        #         ...
        #     logging.info(f"inside call_callbacks, all callbacks: {cls.__callbacks}")
        #     logging.info(f"timestamp: {timestamp}")
        #     logging.info(f"repeat (timestamp - last_command_timestamp): {repeat}")
        #     logging.info(f"last command timestamp: {cls.last_command_timestamp}")

        #     logging.warning(f"this is the callback we are trying to call: {callback}")
        #     logging.warning(f"this is the cooldown: {callback.cooldown}")
        #     logging.warning(f"this is the callback timestamp: {callback.timestamp}")
        #     logging.warning(f"the relation {callback.timestamp} <= {timestamp}")
        #     debug_var = repeat / callback.cooldown

        #     logging.warning({f"this is the debug var (repeat / cooldown): {debug_var}"})
        #     if callback.timestamp + callback.cooldown <= timestamp:
        #         """checking if the callback should be called"""
        #         loop = int(repeat / callback.cooldown)
        #         logging.warning(f"we are inside if statement, loop: {loop}")
        #         # if callback.func.__name__ == "goverment_help":
        #         #     callback()
        #         for _ in range(loop):
        #             logging.warning(f"now we shall call {callback} {loop} times")
        #             callback()
        #         callback.timestamp += callback.cooldown

        # logging.info(f"callbacks inside add event{cls.__callbacks}")
        # logging.info(f"state manager add events: {cls.__events}")


from typing import Callable


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
        logging.info(
            f"\n\t{self.__class__.__name__} class is being created.\n\t\
                {work_unit} comming in are available"
        )
        self.__class__.total_work_unit += work_unit
        logging.info(f"{self.__class__.total_work_unit} work units are available")

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
        self.__class__.created = timestamp
        self.__class__.idx = Counter.allocate_id()
        super().__init__(self.__class__.work_unit)
        logging.info(
            f"inside __init__ of {self.__class__.__name__} class at {timestamp}, {self.__class__.idx} is the id"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}-{self.__class__.idx} Troop object ({self.hp}) at your service"


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
        logging.info(
            f"dragon health is {StateManager.get_enemy_status()} at timestamp "
        )

    _callback = callback_attack_dragon

    # TODO: take the callback funtion by the callback_ in the function name


class Archidon(Swordwrath):
    hp = 80
    price = 300
    power = 10


class Spearton(Swordwrath):
    hp = 250
    price = 500
    work_unit = 2
    cooldown = 3
    power = 35


class Magikill(Swordwrath):
    hp = 80
    price = 1200
    work_unit = 4
    cooldown = 5
    power = 200


class Giant(Swordwrath):
    hp = 1000
    price = 1500
    work_unit = 4
    cooldown = 4
    power = 150


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
            StateManager.add_event(move, info, timestamp)
            if StateManager.game_over:
                print("game over")

            res = CommandManager.run(move, info, timestamp)
            print(*res) if isinstance(res, list) else print(res)


"""

write the main class as a context manager that has a time attr

"""


import os

file_path = "app.log"

try:
    os.remove(file_path)
except OSError as e:
    print(f"Error: {e.filename} - {e.strerror}")


# logging.basicConfig(
#     level=logging.NOTSET,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

if __name__ == "__main__":
    game = Game()
    command_num, dragon_health = map(int, input().split())
    logger.info("Game started!")
    game.run(command_num, dragon_health)
