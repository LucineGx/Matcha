import secrets
from functools import partial

from flask import Blueprint, g, request, session
from werkzeug.security import generate_password_hash

from flaskr.fields import Field
from flaskr.utils import login_required, expose_model_instance, validate_creation_form
from flaskr.db_utils.sql_wrapper import get_single_instance, update_instance, delete_instance, create_single_instance


create_confirmation_token = lambda value: secrets.token_urlsafe(20)


user_model = {
    "id": Field(get=True),
    "email": Field(create=True, get=True, required=True, validate=True),
    "firstname": Field(create=True, get=True, required=True, validate=True),
    "lastname": Field(create=True, get=True, required=True, validate=True),
    "password": Field(create=True, get=True, required=True, validate=True, db_format=generate_password_hash),
    "confirmed": Field(get=True, db_format=int),
    "confirmation_token": Field(create=True, db_format=create_confirmation_token),
    "password_reinit_token": Field(),
    "created_on": Field(get=True)
}


create_user = partial(create_single_instance, user_model, "user")
get_user = partial(get_single_instance, "user")
update_user = partial(update_instance, user_model, "user")
delete_user = partial(delete_instance, "user")
validate_user = partial(validate_creation_form, user_model)
expose_user = partial(expose_model_instance, user_model)


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=('GET', 'PUT', 'DELETE'))
@login_required
def user():
    if request.method == 'GET':
        return expose_user(g.user)

    elif request.method == 'PUT':
        update_user(update=request.form, conditions={"id": g.user["id"]})
        updated_user = get_user("id", g.user["id"])
        return expose_user(updated_user)

    elif request.method == "DELETE":
        delete_user(conditions={"id": g.user["id"]})
        session.clear()
        return "User successfully deleted", 200



