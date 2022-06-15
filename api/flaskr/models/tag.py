import random
from typing import Tuple, Union

from flask import Blueprint, Response

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import CharField
from flaskr.utils import login_required


class Tag(BaseModel):
    name = "tag"

    fields = {
        "name": CharField(primary_key=True, unique=True, required=True),
        "color": CharField(authorized_characters="^[0-9abcdefx]*$", )
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        form["color"] = str(hex(random.randint(0, 0xffffff)))
        return cls._create(form, "name")


bp = Blueprint("tag", __name__, url_prefix="/tag")


@bp.route('/<tag_name>', methods=("GET",))
@login_required
def _get_or_create_tag(tag_name: str):
    return get_or_create_tag(tag_name)

def get_or_create_tag(tag_name: str):
    tag, status_code = Tag.expose("name", tag_name, 200)

    if status_code == 404:
        return Tag.create({"name": tag_name})

    return tag, status_code
