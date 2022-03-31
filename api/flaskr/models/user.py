import secrets
from typing import Tuple, Union

from flask import Blueprint, g, request, session, Response
from werkzeug.security import generate_password_hash

from flaskr.db.fields import CharField, PositiveIntegerField, PositiveTinyIntegerField, DatetimeField
from flaskr.db.base_model import BaseModel
from flaskr.utils import login_required
from flaskr.validators import validate_email, validate_password



create_confirmation_token = lambda value: secrets.token_urlsafe(20)


# To do: email should be exposed for self, but not for other users
class User(BaseModel):
    name = "user"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True),
        "email": CharField(
            unique=True, null=False, required=True, custom_validate=validate_email
        ),
        "first_name": CharField(required=True),
        "last_name": CharField(default=""),
        "password": CharField(
            min_length=8,
            authorized_characters="^[a-zA-Z0-9 _-.#^¨%,;:?!]*$",
            required=True,
            expose=False,
            custom_validate=validate_password,
            db_format=generate_password_hash
        ),
        "created_on": DatetimeField(),
        "confirmed": PositiveTinyIntegerField(max=1, default=0, expose=True),
        "confirmation_token": CharField(unique=True, null=True, expose=False), # To do: call create_confirmation_token in register function
        "password_reinit_token": CharField(unique=True, null=True, expose=False)
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        return cls._create(form, "email")


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=('GET', 'PUT', 'DELETE'))
@login_required
def user():
    if request.method == 'GET':
        return User.expose("id", session['user_id'], 200)

    elif request.method == 'PUT':
        return User.safe_update(request.form, "id", session["user_id"])

    elif request.method == "DELETE":
        User.delete("id", session["user_id"])
        session.clear()
        return "User successfully deleted", 200



