from dataclasses import dataclass
from typing import Callable, Any


def do_nothing(value: Any) -> Any:
    return value


@dataclass
class Field:
    create: bool = False
    get: bool = False
    required: bool = False
    validate: bool = False
    db_format: Callable = do_nothing
