from typing import Tuple, Union

from flask import Blueprint, Response, session

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ForeignKeyField
from flaskr.models import User, Tag


class UserTag(BaseModel):
    name = "user_tag"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True, unique=True),
        "user_id": ForeignKeyField(to=User),
        "tag_id": ForeignKeyField(to=Tag, required=True),
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        form["user_id"] = session["user_id"]
        return cls._create(form, expose=False)

