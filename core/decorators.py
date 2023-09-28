from functools import wraps


def check_dragon_dead(func, dragon=None):
    @wraps(func)
    def wrapper(dragon, *args, **kwargs):
        if dragon == 0:
            print("Can't perform action while dragon is alive!")
            return
        return func(*args, **kwargs)

    return wrapper
