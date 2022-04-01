from typing import Tuple, Union

from flask import g, Blueprint, request, Response, session

from flaskr.db.utils import get_db
from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, CharField, PositiveTinyIntegerField
from flaskr.utils import login_required
from flaskr.validators import validate_gender, validate_type, validate_egg_group


get_bool_value = lambda value: 1 if value is not None else 0


# To do: handle the unique property with some robustness
class Profile(BaseModel):
    name = "profile"

    fields = {
        "user_id": PositiveIntegerField(primary_key=True),
        "level": PositiveIntegerField(min=1, max=100, required=True),
        "gender": CharField(max_length=6, default="'none'", required=True, custom_validate=validate_gender),
        "search_male": PositiveTinyIntegerField(max=1, default=0, db_format=get_bool_value),
        "search_female": PositiveTinyIntegerField(max=1, default=0, db_format=get_bool_value),
        "search_none": PositiveTinyIntegerField(max=1, default=0, db_format=get_bool_value),
        "short_bio": CharField(max_length=280, null=True),
        "public_popularity": PositiveTinyIntegerField(max=100, null=True),
        "type": CharField(max_length=8, required=True, custom_validate=validate_type),
        "type_2": CharField(max_length=8, null=True, custom_validate=validate_type),
        "egg_group": CharField(max_length=8, required=True, custom_validate=validate_egg_group),
        "egg_group_2": CharField(max_length=8, null=True, custom_validate=validate_egg_group)
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
        return Profile.create(request.form)

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
