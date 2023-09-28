from typing import Any, Callable
import logging


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
        logging.info(f"inside callback {self.func}")
        logging.info(
            f"\n\t{self.timestamp}\n\t{self.cooldown}\n\t{self.last_command_timestamp}"
        )
        return self.func(*args, **kwds)

    def __repr__(self) -> str:
        return f"{self.func.__name__.capitalize()} at {self.timestamp}"
