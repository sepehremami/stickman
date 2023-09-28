import logging
from .callback import Callback
from .decorators import check_dragon_dead


def goverment_help():
    StateManager.collect_money(StateManager.GOV_HELP)


@check_dragon_dead
class StateManager:
    last_command_timestamp = 0
    __money = 500
    __callbacks = [
        Callback(goverment_help, 0, cooldown=20, timestamp=0, last_command_timestamp=0)
    ]
    __troops = {}
    __events = []
    GOV_HELP = 180
    DRAGON = 0
    number_of_turns = 0
    game_over = False

    @classmethod
    def get_troops(cls):
        logging.info(f"all troops: {cls.__troops}")
        return cls.__troops

    @classmethod
    def set_state(cls, turn, dragon_health):
        cls.DRAGON = dragon_health
        cls.number_of_turns = turn
        logging.info(
            f"\n\t\tdragon health: {cls.DRAGON}\n\t\t dragon input: {dragon_health}\n\t\t"
        )

    @classmethod
    def add_event(cls, move, info, timestamp):
        if cls._check_dragon_dead():
            return "dead"
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
    def _check_army_status(cls):
        units = 0
        for idx, troop in cls.__troops.items():
            units += len(troop)
        return units

    @classmethod
    def collect_money(cls, money):
        cls.__money += money

    @classmethod
    def add_troop(cls, troop_obj):
        if cls.__money - troop_obj.price < 0:
            print("not enough money")
            return

        if cls._check_army_status() + troop_obj.work_unit >= 50:
            print("too many army")
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

        logging.info(troop_obj)
        logging.info(f"callbacks are here: {cls.__callbacks}")

    @classmethod
    def damage(cls, troop_id, damage: int):
        troop = cls._get_troop_by_id(troop_id=troop_id)
        if troop and type(troop) is not str:
            if damage >= troop.hp:
                cls.remove_troop_callbacks(cls.__troops.pop(troop_id))
                logging.info(f"{troop} is dead")
                return "troop is dead"
            else:
                troop.hp -= damage
                return troop.hp
        return troop

    @classmethod
    def _get_troop_by_id(cls, troop_id):
        try:
            logging.debug(
                f"this is the troop you are looking for (possibly) {cls.__troops[troop_id]}"
            )
            return cls.__troops[troop_id]
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
            game_over = True
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
                for _ in range(loop):
                    callback()

        logging.info(f"callbacks inside add event{cls.__callbacks}")
        logging.info(f"state manager add events: {cls.__events}")
