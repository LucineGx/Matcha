from typing import Union

from flask import Response, g

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, DatetimeField, BooleanField, CharField

from .user import User


class Message(BaseModel):
    """
    Store messages between two users.
    We will need to know if the destination user already has read a message or not.
    """
    name = "message"

    fields = {
        "author_user_id": ForeignKeyField(to=User),
        "destination_user_id": ForeignKeyField(to=User, required=True),
        "datetime": DatetimeField(),
        "read": BooleanField(required=True),
        "content": CharField(required=True, max_length=1580)
    }

    @classmethod
    def create(cls, form: dict) -> tuple[Union[str, Response], int]:
        form["author_user_id"] = g.user["id"]
