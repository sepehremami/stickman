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


from functools import wraps


def check_dragon_dead(func, dragon=None):
    @wraps(func)
    def wrapper(dragon, *args, **kwargs):
        if dragon == 0:
            print("Can't perform action while dragon is alive!")
            return
        return func(*args, **kwargs)

    return wrapper


from typing import Any, Callable

# import logging


class Callback:
    def __init__(
        self, func: Callable, troop_id, cooldown, timestamp, last_command_timestamp
    ) -> None:
        self.func = func
        self.troop_id = troop_id
        self.cooldown = cooldown
        self.timestamp = timestamp
        self.last_command_timestamp = last_command_timestamp

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        # logging.info(f"inside callback {self.func}")
        # logging.info(
        #     f"\n\t{self.timestamp}\n\t{self.cooldown}\n\t{self.last_command_timestamp}"
        # )
        return self.func(*args, **kwds)

    def __repr__(self) -> str:
        return f"{self.func.__name__.capitalize()} at {self.timestamp}"


def goverment_help():
    StateManager.collect_money(StateManager.GOV_HELP)
    # logging.debug(
    #     f"inside goverment_help at timestamp: {StateManager.last_command_timestamp}"
    # )


class StateMine:
    @classmethod
    def handle_mine(cls):
        mines = cls.__mines
        for mine in mines:
            if mine.capacity == 0:
                return mine


class StateManager(StateMine):
    __money = 500
    __callbacks = [
        Callback(goverment_help, 0, cooldown=20, timestamp=0, last_command_timestamp=0)
    ]
    __troops = {}
    __events = []
    __mines = []
    GOV_HELP = 180
    DRAGON = 0
    number_of_turns = 0
    game_over = False
    last_command_timestamp = 0

    @classmethod
    def get_troops(cls):
        # logging.info(f"all troops: {cls.__troops}")
        return cls.__troops

    @classmethod
    def set_state(cls, turn, dragon_health):
        # set Dragon health
        cls.DRAGON = dragon_health

        # Generate 4 mines
        for tag in range(4):
            cls.__mines.append(Mine(tag))

        # set turns (just in case)
        cls.number_of_turns = turn

        # logging.info(
        #     f"\n\t\tdragon health: {cls.DRAGON}\n\t\t dragon input: {dragon_health}\n\t\t"
        # )

    # @check_dragon_dead
    @classmethod
    def add_event(cls, move, info, timestamp):
        if cls._check_dragon_dead():
            return "dead"
        # logging.debug(f"cls.last_command_timestamp: {cls.last_command_timestamp}")
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
        # logging.debug(f"there are a total of {units} units")
        return units

    @classmethod
    def check_army_capacity(cls, troop_obj):
        units = cls.get_army_status()
        if units + troop_obj.work_unit >= 50:
            return True

    @classmethod
    def collect_money(cls, money):
        cls.__money += money

    @classmethod
    def add_troop(cls, troop_obj):
        if cls.__money - troop_obj.price < 0:
            print("not enough money")
            return

        if cls.check_army_capacity(troop_obj):
            # print("too many army")
            return

        cls.__money -= troop_obj.price

        callback = troop_obj._callback

        cls.__callbacks.append(
            Callback(
                callback,
                troop_obj.idx,
                troop_obj.cooldown,
                troop_obj.created,
                cls.last_command_timestamp,
            )
        )

        cls.__troops[troop_obj.idx] = troop_obj

        # logging.info(troop_obj)
        # logging.info(f"callbacks are here: {cls.__callbacks}")

    @classmethod
    def damage(cls, troop_id, damage: int, timestamp):
        troop = cls._get_troop_by_id(troop_id=troop_id)
        if troop and type(troop) is not str:
            if damage >= troop.hp:
                cls.remove_troop_callbacks(cls.__troops.pop(troop_id))
                # logging.info(f"{troop} is dead at {timestamp}")
                return "dead"
            else:
                troop.hp -= damage
                return troop.hp
        return troop

    @classmethod
    def _get_troop_by_id(cls, troop_id):
        try:
            # logging.debug(
            #     f"this is the troop you are looking for (possibly) {cls.__troops[troop_id]}"
            # )
            return cls.__troops[troop_id]
        except KeyError:
            # logging.debug(f"troop with {troop_id} id does not exist")
            return "no matter"

    @classmethod
    def remove_troop_callbacks(cls, troop):
        for callback in cls.__callbacks:
            if callback.troop_id == troop.idx:
                cls.__callbacks.remove(callback)
                # logging.warning(
                # f"{callback.func.__name__} removed from callback list for troop with id:{troop.idx}"
                # )

    @classmethod
    def _check_dragon_dead(cls):
        if cls.DRAGON == 0:
            return "dead"
        return False

    @classmethod
    def attack_dragon(cls, damage):
        if check := cls._check_dragon_dead() and damage >= cls.DRAGON:
            cls.DRAGON = 0
            game_over = True
            return check

        else:
            cls.DRAGON -= damage
            # logging.warning(
            #     f"dragon is taking {damage} damage; its health is: {cls.DRAGON} at timestamp {cls.last_command_timestamp}"
            # )

    @classmethod
    def call_callbacks(cls, timestamp):
        repeat = timestamp - cls.last_command_timestamp
        for callback in cls.__callbacks:
            if callback.timestamp + callback.cooldown <= timestamp:
                """checking if the callback should be called"""
                loop = int(repeat / callback.cooldown)
                if callback.func.__name__ == "goverment_help":
                    callback()
                for _ in range(loop):
                    callback()
                callback.timestamp += callback.cooldown

        # logging.info(f"callbacks inside add event{cls.__callbacks}")
        # logging.info(f"state manager add events: {cls.__events}")


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
        # logging.info(
        #     f"\n\t{self.__class__.__name__} class is being created.\n\t\
        #         {work_unit} comming in are available"
        # )
        self.__class__.total_work_unit += work_unit
        # logging.info(f"{self.__class__.total_work_unit} work units are ava")

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
        # logging.info(
        #     f"inside __init__ of {self.__class__.__name__} class \
        #     at {timestamp}, {self.__class__.idx} is the id and {super().allocate_id()} is the allocated_id"
        # )
        self.__class__.created = timestamp
        self.__class__.idx = Counter.allocate_id()
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
    cooldown = 10  #
    work_unit = 2

    def callback_yield_coin(self):
        StateManager.collect_money(self.__class__.collected_money)
        # logging.info(
        #     f"{self.__class__.__name__} number {self.__class__.idx} yielding coin"
        # )

    # yield_coin = sign_function(yield_coin)
    _callback = callback_yield_coin


class Swordwrath(ArmyUnit):
    hp = 100
    price = 125
    cooldown = 1
    power = 20

    def callback_attack_dragon(self):
        StateManager.attack_dragon(self.power)
        # logging.info(
        #     f"{self.__class__.__name__} number {self.idx} is attacking the dragon"
        # )
        # # logging.info(
        #     f"dragon health is {StateManager.get_enemy_status()} at timestamp "
        # )

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
    def miner_allocation(self, troop_obj):
        if not isinstance(troop_obj, Miner):
            return True

    @staticmethod
    def add(info, timestamp):
        role: str = info.pop()
        troop_obj = eval((f"{role.capitalize()}"))

        if troop_obj.price > StateManager.get_money_status():
            return "not enough money"
        elif StateManager.check_army_capacity(troop_obj):
            return "too many army"
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
        stats = [
            len(list(troop for _, troop in army.items() if type(troop) is Miner)),
            len(list(troop for _, troop in army.items() if type(troop) is Swordwrath)),
            len(list(troop for _, troop in army.items() if type(troop) is Archidon)),
            len(list(troop for _, troop in army.items() if type(troop) is Spearton)),
            len(list(troop for _, troop in army.items() if type(troop) is Magikill)),
            len(list(troop for _, troop in army.items() if type(troop) is Giant)),
        ]  # TODO check if we can handle this with a named tupple

        # stats_dict = {}
        # for idx, troop in army.items():
        #     key = troop.__class__.__name__.lower
        #     if stats_dict.get(key):
        #         stats_dict[key] += 1
        #     else:
        #         stats_dict[key] = 1
        # # wont work if troops are removes
        return stats

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
        # logging.info(f"user input : {userin}")
        userin = userin.split()
        timestamp = userin.pop()
        func_name: str = userin.pop(0).replace("-", "_")

        time_seconds = (lambda l: l[0] * 60 + l[1] + l[2] / 1000)(
            list(map(int, timestamp.split(":")))
        )

        return func_name, userin, time_seconds

    def run(self, num, dragon_health):
        # logging.info("Inside Game.run")
        StateManager.set_state(num, dragon_health)

        for _ in range(num):
            move, info, timestamp = self.handle_input(input())
            StateManager.add_event(move=move, info=info, timestamp=timestamp)
            res = CommandManager.run(move, info, timestamp)
            print(*res) if isinstance(res, list) else print(res)


import os

# import logging


# file_path = "log/app.log"

# try:
#     os.remove(file_path)
# except OSError as e:
#     print(f"Error: {e.filename} - {e.strerror}")


if __name__ == "__main__":
    game = Game()
    command_num, dragon_health = map(int, input().split())
    # logging.info("Game started!")
    game.run(command_num, dragon_health)
