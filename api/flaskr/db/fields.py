from dataclasses import dataclass
from typing import Callable, Any
from math import inf
import re


def do_nothing(value: Any) -> Any:
    return value


@dataclass
class Field:
    # Fields used at table creation
    type_name: str = None
    primary_key: bool = False
    auto_increment: bool = False
    unique: bool = False
    null: bool = False
    default: Any = None

    required: bool = False
    expose: bool = False
    custom_validate: Callable = lambda n, v: True
    db_format: Callable = do_nothing


    @classmethod
    def validate(cls, name: str, value: Any):
        cls._validate(value, name)
        cls.custom_validate(value, name)

    @classmethod
    def _validate(cls, name: str, value: Any):
        raise NotImplementedError


@dataclass
class PositiveIntegerField(Field):
    type_name: str = "INTEGER"
    min: int = 0
    max: int = inf

    @classmethod
    def _validate(cls, name: str, value: Any):
        assert isinstance(value, int), f"Field {name} should be an int"
        assert (
            cls.min <= value <= cls.max,
            f"Field {name} value should be between {cls.min} and {cls.max}"
        )


@dataclass
class PositiveTinyIntegerField(PositiveIntegerField):
    type_name: str = "TINYINT"


@dataclass
class CharField(Field):
    min_length: int = 0
    max_length: int = 32
    authorized_characters: str = "^[a-zA-Z0-9 _-.]*$"

    @property
    def type_name(self):
        return f"varchar({self.max_length})"

    @classmethod
    def _validate(cls, name: str, value: Any):
        assert isinstance(value, str), f"Field {name} should be a string"
        assert (
            cls.min_length <= len(value) <= cls.max_length,
            f"Field {name} should be {cls.max_length} characters max"
        )
        assert (
            re.match(cls.authorized_characters, value),
            f"Authorized characters for {name}: alpha-numerical or one of .-_"
        )


@dataclass
class FixedCharField(Field):
    length: int = 0
    authorized_characters: str = "^[a-zA-Z0-9 _-.]*$"

    @property
    def type_name(self):
        return f"char({self.length})"

    @classmethod
    def _validate(cls, name: str, value: Any):
        assert isinstance(value, str), f"Field {name} should be a string"
        assert (len(value) == cls.length, f"Field {name} should be {cls.length} characters long")
        assert (
            re.match(cls.authorized_characters, value),
            f"Authorized characters for {name}: alpha-numerical or one of .-_"
        )


@dataclass
class DatetimeField(Field):
    type_name: str = "TIMESTAMP"
    default: Any = "CURRENT_TIMESTAMP"

    # To do: if required, find a way to validate timestamp.
    @classmethod
    def _validate(cls, name: str, value: Any):
        pass
