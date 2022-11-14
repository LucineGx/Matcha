from dataclasses import dataclass
from typing import Callable, Any, Optional
from math import inf
import re


def do_nothing(value: Any) -> Any:
    return value


@dataclass
class Field:
    # Fields used at table creation
    primary_key: bool = False
    auto_increment: bool = False

    unique: bool = False
    null: bool = False
    default: Any = None

    # Fields for API routes
    required: bool = False
    expose: bool = True

    updatable: bool = True

    custom_validate: Callable = lambda n, v: True
    db_format: Callable = do_nothing

    @property
    def type_name(self):
        raise NotImplementedError

    def validate(self, name: str, value: Any):
        self._validate(name, value)
        self.custom_validate(name, value)

    def _validate(self, name: str, value: Any) -> None:
        raise NotImplementedError


@dataclass
class BlobField(Field):
    @property
    def type_name(self):
        return "BLOB"

    def _validate(self, name: str, value: Any) -> None:
        pass



@dataclass
class PositiveIntegerField(Field):
    min: int = 0
    max: int = inf
    db_format = int

    @property
    def type_name(self):
        return "INTEGER"

    def _validate(self, name: str, value: Any) -> None:
        if isinstance(value, str):
            assert value.isnumeric(), f"Field {name} should be an int"
            assert self.min <= int(value) <= self.max, f"Field {name} value should be between {self.min} and {self.max}"
        else:
            assert isinstance(value, int), f"Field {name} should be an int"
            assert self.min <= value <= self.max, f"Field {name} value should be between {self.min} and {self.max}"


dataclass
class ForeignField(Field):
    to: object = None
    on: str = "id"

    def _validate(self, name: str, value: Any) -> None:
        super()._validate(name, value)
        foreign_rows = self.to._list()
        foreign_values = [row[self.on] for row in foreign_rows]
        assert value in foreign_values, f"{name} not in {self.to.name} table."


@dataclass
class ForeignKeyField(ForeignField, PositiveIntegerField):
    to: object = None
    on: str = "id"

    def _validate(self, name: str, value: Any) -> None:
        super()._validate(name, int(value))


@dataclass
class PositiveTinyIntegerField(PositiveIntegerField):
    @property
    def type_name(self):
        return "TINYINT"

@dataclass
class BooleanField(PositiveTinyIntegerField):
    max: int = 1
    default: int = 0
    db_format: lambda value: 1 if (value is not None and int(value) != 0) else 0


@dataclass
class CharField(Field):
    min_length: int = 0
    max_length: int = 32
    authorized_characters: str = "^[a-zA-Z0-9 _\-.]*$"

    @property
    def type_name(self):
        return f"varchar({self.max_length})"

    def _validate(self, name: str, value: Any) -> None:
        assert isinstance(value, str), f"Field {name} should be a string"
        assert self.min_length <= len(value) <= self.max_length, f"Field {name} should be {self.max_length} characters max"
        assert re.match(self.authorized_characters, value), f"Authorized characters for {name}: {self.authorized_characters}"


@dataclass
class ForeignCharField(ForeignField, CharField):
    to: object = None
    on: str = "id"


@dataclass
class ChoiceField(CharField):
    choice: Optional[list] = None
    
    def _validate(self, name: str, value: Any) -> None:
        assert isinstance(value, str), f"Field {name} should be a string"
        assert isinstance(self.choice, list), f"{name} choice should be a list of string"
        for elem in self.choice:
            assert isinstance(elem, str), f"{name} choice should be a list of string"
        assert value in self.choice, f"{name} should be in {self.choice}"


@dataclass
class DatetimeField(Field):
    default: Any = "CURRENT_TIMESTAMP"

    @property
    def type_name(self):
        return "TIMESTAMP"

    # To do: if required, find a way to validate timestamp.
    def _validate(self, name: str, value: Any) -> None:
        pass



@dataclass
class FloatField(Field):
    min: int = -inf
    max: int = inf
    db_format = float

    @property
    def type_name(self):
        return "FLOAT"

    def _validate(self, name: str, value: Any) -> None:
        if isinstance(value, str):
            try :
                assert self.min <= float(value) <= self.max, f"Field {name} value should be between {self.min} and {self.max}"
            except ValueError:
                raise AssertionError(f"Field {name} should be an int")
        else:
            assert isinstance(value, float), f"Field {name} should be an int"
            assert self.min <= value <= self.max, f"Field {name} value should be between {self.min} and {self.max}"

