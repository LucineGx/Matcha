from typing import Any, List
from functools import partial
import re

from email_validator import validate_email as _validate_email
from email_validator import EmailNotValidError


def validate_email(field_name: str, email: Any) -> None:
    try:
        _validate_email(email)
    except EmailNotValidError as e:
        raise AssertionError(e)


def validate_password(field_name: str, password: Any) -> None:
    patterns = [r"\d", r"[A-Z]", r"[a-z]", r"[_-.#^¨%,;:?!]"]
    for pattern in patterns:
        if re.search(pattern, password) is None:
            raise AssertionError(f"Pattern {pattern} missing in password.")


def validate_choice(valid_choices: List[str], field_name: str, value: Any) -> None:
    error_msg = f"Unauthorized value for {field_name}"
    assert isinstance(value, str), error_msg
    assert value in valid_choices


gender_choice = {"female", "male", "none"}
validate_gender = partial(validate_choice, gender_choice)
type_choice = {
    "Bug",
    "Dark",
    "Dragon",
    "Electric",
    "Fairy",
    "Fighting",
    "Fire",
    "Flying",
    "Ghost",
    "Grass",
    "Ground",
    "Ice",
    "Normal",
    "Poison",
    "Psychic",
    "Rock",
    "Steel",
    "Water",
}
validate_type = partial(validate_choice, type_choice)
egg_group_choice = {
    "Amorphous",
    "Bug",
    "Ditto",
    "Dragon",
    "Fairy",
    "Field",
    "Flying",
    "Grass",
    "Human-like",
    "Mineral",
    "Monster",
    "Undiscovered",
    "Water 1",
    "Water 2",
    "Water 3",
}
validate_egg_group = partial(validate_choice, egg_group_choice)
