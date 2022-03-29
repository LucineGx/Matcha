import random
from functools import partial

from flask import Blueprint

from flaskr.fields import Field
from flaskr.utils import login_required, expose_model_instance
from flaskr.db_utils.sql_wrapper import get_single_instance, create_single_instance, get_db


get_color = lambda value: str(hex(random.randint(0, 0xffffff)))


tag_model = {
    "id": Field(get=True),
    "name": Field(create=True, get=True, required=True, validate=True),
    "color": Field(create=True, get=True, required=True, db_format=get_color)
}


create_tag = partial(create_single_instance, tag_model, "tag")
get_tag_by_name = partial(get_single_instance, "tag", "name")
expose_tag = partial(expose_model_instance, tag_model)


bp = Blueprint("tag", __name__, url_prefix="/tag")


@bp.route('/<tag_name>', methods=("GET",))
@login_required
def get_tag(tag_name: str):
    tag = get_tag_by_name(tag_name)
    if tag is None:
        db = get_db()
        create_tag({"name": tag_name}, db)
        tag = get_tag_by_name(tag_name)

    return expose_tag(tag)

