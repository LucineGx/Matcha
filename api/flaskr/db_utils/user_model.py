from typing import Any

from werkzeug.security import generate_password_hash


def do_nothing(value: Any) -> Any:
    return value


user = {
    "fields": {
        "id": {"required": False, "db_format": do_nothing},
        "email": {"required": True, "db_format": do_nothing},
        "firstname": {"required": True, "db_format": do_nothing},
        "lastname": {"required": True, "db_format": do_nothing},
        "password": {"required": True, "db_format": generate_password_hash},
        "confirmed": {"required": False, "db_format": int},
        "created_on": {"required": False, "db_format": do_nothing},
        "confirmation_token": {"required": False, "db_format": do_nothing},
    },
    "integrity_unique_field": "email"
}
