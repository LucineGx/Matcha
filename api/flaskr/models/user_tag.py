from typing import Tuple, Union

from flask import Response, session, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, ForeignCharField, BooleanField
from flaskr.models import User, Tag
from flaskr.models.user import bp
from flaskr.models.tag import get_or_create_tag
from flaskr.utils import login_required


class UserTag(BaseModel):
    name = "user_tag"

    fields = {
        "user_id": ForeignKeyField(to=User),
        "tag_name": ForeignCharField(to=Tag, on='name', required=True),
        "hidden": BooleanField()
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        form["user_id"] = session["user_id"]
        return cls._create(form, expose=False)


@bp.route('/tag/<tag_name>', methods=('PUT', 'DELETE'))
@login_required
def update_user_tags(tag_name: str):
    if request.method == 'PUT':
        user_tag = UserTag.get(on_col=['user_id', 'tag_name'], for_val=[session['user_id'], tag_name]).fetchone()
        if user_tag is None:
            get_or_create_tag(tag_name)
            UserTag.create({'tag_name': tag_name})
    elif request.method == 'DELETE':
        UserTag.delete(on_col=['user_id', 'tag_name'], for_val=[session['user_id'], tag_name])

    return list_tags(session["user_id"])


@bp.route('/tags', methods=('GET',))
@login_required
def list_user_tags():
    return list_tags(session["user_id"])


@bp.route('/<user_id>/tags', methods=('GET',))
@login_required
def list_other_user_tags(user_id: int):
    return list_tags(user_id)


def list_tags(user_id):
    user_tags = UserTag.get(on_col="user_id", for_val=user_id).fetchall()
    tag_names = [tag["tag_name"] for tag in user_tags]
    if tag_names:
        tags = Tag.get(on_col="name", for_val=tag_names).fetchall()
    else:
        tags = list()
    return Tag.bulk_expose(tags, 200)
