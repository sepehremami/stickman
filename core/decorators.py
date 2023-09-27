def check_dragon_dead(cls):
    original_methods = {}

    for name, method in cls.__dict__.items():
        if callable(method):
            original_methods[name] = method

    def check_dragon_wrapper(self, *args, **kwargs):
        if self.DRAGON == 0:
            self.game_over = True
            return "dead"
        else:
            return original_methods[self.__class__.__name__](self, *args, **kwargs)

    # Replace the original methods with the wrapper
    for name, method in original_methods.items():
        setattr(cls, name, check_dragon_wrapper)

    return cls
