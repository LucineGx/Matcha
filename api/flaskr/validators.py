from typing import Any, List
from functools import partial
import re

from email_validator import validate_email as _validate_email
from email_validator import EmailNotValidError


def validate_email(_: str, email: Any) -> None:
    try:
        _validate_email(email)
    except EmailNotValidError as e:
        raise AssertionError(e)


def validate_password(_: str, password: Any) -> None:
    patterns = [r"\d", r"[A-Z]", r"[a-z]", r"[_\-.#^¨%,;:?!@]"]
    for pattern in patterns:
        if re.search(pattern, password) is None:
            raise AssertionError(f"Pattern {pattern} missing in password.")

