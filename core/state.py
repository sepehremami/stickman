import logging
from .callback import Callback
from .decorators import check_dragon_dead
from .building import Mine
from .mixins import StateMineMixin


def goverment_help():
    StateManager.collect_money(StateManager.GOV_HELP)
    logging.debug(
        f"inside goverment_help at timestamp: {StateManager.last_command_timestamp}"
    )


class StateManager(StateMineMixin):
    __money = 500
    __callbacks = [
        Callback(goverment_help, 0, cooldown=20, timestamp=0, last_command_timestamp=0)
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
        # if cls._check_dragon_dead():
        #     return "dead"
        logging.debug(f"cls.last_command_timestamp: {cls.last_command_timestamp}")
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
        # callback = getattr(troop_obj, startswith("callback_))

        cls.__callbacks.append(
            Callback(
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

        logging.info(f"callbacks inside add event{cls.__callbacks}")
        logging.info(f"state manager add events: {cls.__events}")
