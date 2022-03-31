import secrets
from functools import partial

from flask import Blueprint, g, request, session
from werkzeug.security import generate_password_hash

from flaskr.db.fields import Field
from flaskr.utils import login_required, expose_model_instance
from flaskr.validators import validate_email, validate_32_string, validate_password
from flaskr.db_utils.sql_wrapper import get_single_instance, update_instance, delete_instance, create_single_instance


create_confirmation_token = lambda value: secrets.token_urlsafe(20)


user_model = {
    "id": Field(get=True),
    "email": Field(create=True, get=True, required=True, custom_validate=validate_email),
    "firstname": Field(create=True, get=True, required=True, custom_validate=validate_32_string),
    "lastname": Field(create=True, get=True, required=True, custom_validate=validate_32_string),
    "password": Field(create=True, get=True, required=True, custom_validate=validate_password, db_format=generate_password_hash),
    "confirmed": Field(get=True, db_format=int),
    "confirmation_token": Field(create=True, db_format=create_confirmation_token),
    "password_reinit_token": Field(),
    "created_on": Field(get=True)
}


create_user = partial(create_single_instance, user_model, "user")
get_user = partial(get_single_instance, "user")
update_user = partial(update_instance, user_model, "user")
delete_user = partial(delete_instance, "user")
expose_user = partial(expose_model_instance, user_model)


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=('GET', 'PUT', 'DELETE'))
@login_required
def user():
    if request.method == 'GET':
        return expose_user(g.user)

    elif request.method == 'PUT':
        try:
            update_user(update=request.form, conditions={"id": g.user["id"]})
        except AssertionError as e:
            return str(e), 400
        else:
            return expose_user(get_user("id", g.user["id"]), 201)

    elif request.method == "DELETE":
        delete_user(conditions={"id": g.user["id"]})
        session.clear()
        return "User successfully deleted", 200



