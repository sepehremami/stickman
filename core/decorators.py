def check_dragon_dead(cls):
    original_methods = {}

    for name, method in cls.__dict__.items():
        if callable(method):
            original_methods[name] = method

    def check_dragon_wrapper(cls, *args, **kwargs):
        if cls.DRAGON == 0:
            cls.game_over = True
            return "dead"
        else:
            return original_methods[cls.__class__.__name__](cls, *args, **kwargs)

    # Replace the original methods with the wrapper
    for name, method in original_methods.items():
        setattr(cls, name, check_dragon_wrapper)

    return cls
