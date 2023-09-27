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
    DRAGON = 0
    number_of_turns = 0
    game_over = False

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
        cls.update_time(timestamp)
        cls.__events.append((move, timestamp))
        cls.call_callbacks(timestamp=timestamp)

    @classmethod
    def update_time(cls, timestamp):
        cls.last_command_timestamp = timestamp

    @classmethod
    def money_status(cls):
        if check := cls._check_dragon_dead():
            return check
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
            logging.info(
                f"dragon is taking {damage} damage; its health is: {cls.DRAGON}"
            )

    @classmethod
    def call_callbacks(cls, timestamp):
        diff = timestamp - cls.last_command_timestamp
        for callback in cls.__callbacks:
            if callback.timestamp + callback.cooldown < timestamp:
                if callback.func.__name__ != "goverment_help":
                    n = diff / callback.cooldown
                    logging.info(
                        f"\n\tdiff:{diff}\n\tn:{n}\n\tcooldown:{callback.cooldown} \
                        \n\ttimestamp:{timestamp}\n\tlast_time:{cls.last_command_timestamp} \
                        \n\tcallback timestamp:{callback.timestamp}"
                    )
                    if n > 1:
                        for _ in range(int(n)):
                            callback()
                            if check := cls._check_dragon_dead():
                                return check
                    else:
                        callback()
                else:
                    callback()
                callback.timestamp += callback.cooldown

        logging.info(f"callbacks inside add event{cls.__callbacks}")
        logging.info(f"state manager add events: {cls.__events}")
