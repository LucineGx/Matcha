from functools import partial
from typing import Any

from flask import Blueprint, g, jsonify, request, session
from werkzeug.security import generate_password_hash

from flaskr.utils import login_required
from flaskr.db_utils.sql_wrapper import get_single_instance, update_instance, delete_instance


def do_nothing(value: Any) -> Any:
    return value


user_model = {
    "fields": {
        "id": {"required": False, "db_format": do_nothing},
        "email": {"required": True, "db_format": do_nothing},
        "firstname": {"required": True, "db_format": do_nothing},
        "lastname": {"required": True, "db_format": do_nothing},
        "password": {"required": True, "db_format": generate_password_hash},
        "confirmed": {"required": False, "db_format": int},
        "created_on": {"required": False, "db_format": do_nothing},
        "confirmation_token": {"required": False, "db_format": do_nothing},
        "password_reinit_token": {"required": False, "db_format": do_nothing}
    },
    "get": {"id", "email", "firstname", "lastname", "confirmed", "created_on"}
}


get_user = partial(get_single_instance, "user")
update_user = partial(update_instance, user_model["fields"], "user")
delete_user = partial(delete_instance, "user")


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=('GET', 'PUT', 'DELETE'))
@login_required
def user():
    if request.method == 'GET':
        return jsonify({key: g.user[key] for key in user_model["get"]}), 200

    elif request.method == 'PUT':
        update_user(update=request.form, conditions={"id": g.user["id"]})
        updated_user = get_user("id", g.user["id"])
        return jsonify({key: updated_user[key] for key in user_model["get"]}), 200

    elif request.method == "DELETE":
        delete_user(conditions={"id": g.user["id"]})
        session.clear()
        return "User successfully deleted", 200



