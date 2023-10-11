from functools import update_wrapper
import logging


def check_dragon_dead(func, *args, **kwargs):
    logging.warning(f"inside deco{func}\nargs{args}\nkwargs{kwargs}")

    def wrapper(cls, *args, **kwds):
        # return func(*args, **kwds)
        logging.warning(
            f"inside deco{func}\nargs{args}\nkwargs{kwargs}\n0: {args[0]}\n1: {args[1]}\n2: {args[2]}"
        )
        if cls.DRAGON == 0:
            cls.game_over = True
        else:
            result = func(cls, args[0], args[1], args[2])
            return result

    return update_wrapper(wrapper, func)
