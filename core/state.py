import logging


class StateManager:
    __money = 500
    __callbacks = []
    __troops = []
    __enemies = []
    __events = []

    @classmethod
    def money_status(cls):
        return cls.__money

    @classmethod
    def collect_money(cls, money):
        cls.__money += money

    @classmethod
    def add_troop(cls, troop_obj):
        logging.info(troop_obj)
        callback = troop_obj._callback()
        cls.__callbacks.append(callback)
        # TODO: check if len troops is out of range
        cls.__troops.append(troop_obj)

    @classmethod
    def add_event(cls, move, info, timestamp):
        cls.__events.append((move, timestamp))
        logging.info(cls.__events)

    @classmethod
    def run(cls, move, info, timestamp):
        ...

    # for callback in cls.__callbackes:
    #     callback(move, info, timestamp)
