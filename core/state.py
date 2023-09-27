import logging
from .callback import Callback


def goverment_help():
    StateManager.collect_money(StateManager.GOV_HELP)


class StateManager:
    last_command_timestamp = 0
    __money = 500
    __callbacks = [
        Callback(goverment_help, cooldown=20, timestamp=0, last_command_timestamp=0)
    ]
    __troops = []
    __events = []
    GOV_HELP = 180

    @classmethod
    def call_callbacks(cls):
        for callback in cls.__callbacks:
            callback()

    @classmethod
    def add_event(cls, move, info, timestamp):
        cls.update_time(timestamp)
        cls.__events.append((move, timestamp))

        for callback in cls.__callbacks:
            if callback.timestamp + callback.cooldown < timestamp:
                callback()
                callback.timestamp += callback.cooldown

        logging.info(f"callbacks inside add event{cls.__callbacks}")
        logging.info(f"state manager add events: {cls.__events}")

    @classmethod
    def update_time(cls, timestamp):
        cls.last_command_timestamp = timestamp

    @classmethod
    def money_status(cls):
        return cls.__money

    @classmethod
    def collect_money(cls, money):
        cls.__money += money

    @classmethod
    def add_troop(cls, troop_obj):
        if cls.__money - troop_obj.price < 0:
            print("Not enough money")
            return
        cls.__money -= troop_obj.price
        callback = troop_obj._callback

        cls.__callbacks.append(
            Callback(
                callback,
                troop_obj.cooldown,
                troop_obj.created,
                cls.last_command_timestamp,
            )
        )
        # TODO: check if len troops is out of range
        cls.__troops.append(troop_obj)
        logging.info(troop_obj)
        logging.info(callback.__name__)
        logging.info(f"callbacks are here: {cls.__callbacks}")

    @classmethod
    def run(cls, move, info, timestamp):
        ...

    # for callback in cls.__callbackes:
    #     callback(move, info, timestamp)

    @classmethod
    def damage(cls, troop_id, damage: int):
        troop = cls._get_troop_by_id(troop_id=troop_id)
        troop.hp -= damage
        if cls._check_troop_perished:
            return "dead"
        return troop

    @classmethod
    def _get_troop_by_id(cls, troop_id):
        for troop in cls.__troops:
            if troop.idx == troop_id:
                return troop

    @classmethod
    def _check_troop_perished(cls, troop):
        if troop.hp == 0:
            return True
        return False
