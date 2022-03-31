from functools import partial

from flask import g, Blueprint, request

from flaskr.db import get_db
from flaskr.db_utils.sql_wrapper import create_single_instance, get_single_instance, update_instance, delete_instance
from flaskr.db.fields import Field, PositiveIntegerField
from flaskr.utils import login_required, expose_model_instance
from flaskr.validators import validate_gender, validate_280_string, validate_type, validate_egg_group, validate_level


get_user_id = lambda value: g.user["id"]
get_bool_value = lambda value: 1 if value is not None else 0


profile_model = {
    "user_id": Field(create=True, get=True, db_format=get_user_id),
    "gender": Field(create=True, get=True, required=True, custom_validate=validate_gender),
    "search_male": Field(create=True, get=True, db_format=get_bool_value),
    "search_female": Field(create=True, get=True, db_format=get_bool_value),
    "search_none": Field(create=True, get=True, db_format=get_bool_value),
    "short_bio": Field(create=True, get=True, custom_validate=validate_280_string),
    "public_popularity": Field(get=True),
    "type": Field(create=True, get=True, required=True, custom_validate=validate_type),
    "type_2": Field(create=True, get=True, custom_validate=validate_type),
    "egg_group": Field(create=True, get=True, required=True, custom_validate=validate_egg_group),
    "egg_group_2": Field(create=True, get=True, custom_validate=validate_egg_group),
    "level": PositiveIntegerField(create=True, get=True, required=True, custom_validate=validate_level)
}


create_profile = partial(create_single_instance, profile_model, "profile")
get_profile_by_id = partial(get_single_instance, "profile", "user_id")
update_profile = partial(update_instance, profile_model, "profile")
delete_profile = partial(delete_instance, "profile")
expose_profile = partial(expose_model_instance, profile_model)


bp = Blueprint("profile", __name__, url_prefix="/profile")


# To do: add a get method with a profile id, to get other profiles
@bp.route('/', methods=('GET', 'POST', 'PUT', 'DELETE'))
@login_required
def self_profile():
    if request.method == "POST":
        db = get_db()
        try:
            create_profile(instance=request.form, db=db)
        except db.IntegrityError:
            return f"User {g.user['email']} has already defined a profile.", 409
        except AssertionError as e:
            return str(e), 400
        else:
            return expose_profile(get_profile_by_id(g.user["id"]), 201)

    if request.method == "GET":
        return expose_profile(get_profile_by_id(g.user["id"]))

    elif request.method == "PUT":
        try:
            update_profile(update=request.form, conditions={"user_id": g.user["id"]})
        except AssertionError as e:
            return str(e), 400
        else:
            return expose_profile(get_profile_by_id(g.user["id"]), 201)

    elif request.method == "DELETE":
        delete_profile(conditions={"user_id": g.user["id"]})
        return "Profile successfully deleted", 200


@bp.route('/<user_id>', methods=('GET',))
@login_required
def other_profile(user_id: int):
    return expose_profile(get_profile_by_id(user_id))
