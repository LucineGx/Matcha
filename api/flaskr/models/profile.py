from typing import Tuple, Union

from flask import Blueprint, request, Response, session

from flaskr.db.utils import get_db
from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, CharField, PositiveTinyIntegerField, ForeignKeyField, BooleanField
from flaskr.utils import login_required
from flaskr.validators import validate_gender

from .egg_group import EggGroup
from .type import Type
from .user import User


get_bool_value = lambda value: 1 if (value is not None and int(value) != 0) else 0


class Profile(BaseModel):
    name = "profile"

    fields = {
        "user_id": ForeignKeyField(to=User, primary_key=True),
        "level": PositiveIntegerField(min=1, max=100, required=True),
        "gender": CharField(max_length=6, default="'none'", required=True, custom_validate=validate_gender),
        "search_male": BooleanField(),
        "search_female": BooleanField(),
        "search_none": BooleanField(),
        "short_bio": CharField(max_length=280, null=True),
        "public_popularity": PositiveTinyIntegerField(max=100, null=True),
        "type": ForeignKeyField(to=Type, required=True),
        "type_2": ForeignKeyField(to=Type, null=True),
        "egg_group": ForeignKeyField(to=EggGroup, required=True),
        "egg_group_2": ForeignKeyField(to=EggGroup, null=True)
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        db = get_db()
        form["user_id"] = session["user_id"]
        try:
            return cls._create(form, "user_id")
        except db.IntegrityError:
            return f"User {session['user_id']} has already defined a profile", 409


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route('/', methods=('GET', 'POST', 'PUT', 'DELETE'))
@login_required
def self_profile():
    if request.method == "POST":
        return Profile.create(dict(request.form))

    if request.method == "GET":
        return Profile.expose("user_id", session["user_id"], 200)

    elif request.method == "PUT":
        return Profile.safe_update(request.form, "user_id", session["user_id"])

    elif request.method == "DELETE":
        Profile.delete("user_id", session["user_id"])
        return "Profile successfully deleted", 200


@bp.route('/<user_id>', methods=('GET',))
@login_required
def other_profile(user_id: int):
    return Profile.expose("user_id", user_id, 200)
