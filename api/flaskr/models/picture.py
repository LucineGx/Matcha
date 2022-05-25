from typing import Tuple, Union

from flask import Response, Blueprint, session, request
from api.flaskr.models.user import user
from api.flaskr.utils import login_required

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ForeignKeyField, BooleanField, do_nothing, BlobField
from flaskr.models import User


class Picture(BaseModel):
    name = "picture"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True, unique=True),
        "user_id": ForeignKeyField(to=User),
        "picture": BlobField(required=True), # Defined field for image
        "main": BooleanField(required=True)
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        form["user_id"] = session["user_id"]
        if BooleanField().db_format(form['main']):
            cls.safe_update({'main': 0}, on_col='user_id', for_val=session['user_id'])
        return cls._create(form, expose=False)
    
    @classmethod
    def validate_form(cls, form: dict, check_required: bool = True) -> None:
        assert len(cls.get_user_pictures()) < 5, "Maximum of five pictures for one user."
        return super().validate_form(form, check_required)
    
    @classmethod
    def get_user_pictures(cls, user_id: int = session['user_id']):
        return cls.get(on_col="user_id", for_val=user_id).fetchall()



bp = Blueprint("picture", __name__, url_prefix="/profile")


@bp.route('/pictures', mehods=('GET',))
def get_self_pictures():
    user_pictures = Picture.get_user_pictures() | list()
    return Picture.bulk_expose(user_pictures, 200)


@bp.route('/picture', methods=('POST',))
@login_required
def add_picture():
    return Picture.create(dict(request.form))
