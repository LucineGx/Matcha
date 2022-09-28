from typing import Tuple, Union

from flask import Response, Blueprint, session, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ForeignKeyField, BooleanField, BlobField
from flaskr.utils import login_required

from .user import User, bp


class Picture(BaseModel):
    """
    Each picture must be linked to one user.
    Each user can only save a maximum of five pictures.
    Only one can be the main picture, but there don't have to be one.

    We need to be able to
        - add a picture
        - delete a picture
        - pdate a picture or its 'main' status
        - get all the pictures of a given user.
    """
    name = "picture"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True, unique=True),
        "user_id": ForeignKeyField(to=User),
        "picture": BlobField(required=True), # Defined field for image
        "main": BooleanField(required=True)
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        """
            When a picture is added or changed, if the form indicates that this picture is going
            to be the main one, we'll run a request to make sure all the others pictures of the
            user get their 'main' field set to 0.
        """
        form["user_id"] = session["user_id"]
        if BooleanField().db_format(form['main']):
            cls.safe_update({'main': 0}, on_col='user_id', for_val=session['user_id'])
        return cls._create(form, expose=False)
    
    @classmethod
    def validate_form(cls, form: dict, check_required: bool = True) -> None:
        assert len(cls.get_user_pictures()) < 5, "Maximum of five pictures for one user."
        return super().validate_form(form, check_required)
    
    @classmethod
    def get_user_pictures(cls, user_id: int = None):
        if user_id is None:
            user_id = session['user_id']
        return cls.get(on_col="user_id", for_val=user_id).fetchall()
    
    @classmethod
    def get_user_profile_picture(cls, user_id: int = None):
        if user_id is None:
            user_id = session['user_id']
        result = cls.get(on_col=["user_id", 'main'], for_val=[user_id, 1]).fetchone()
        if result :
            return result['picture']
        else:
            return None


@bp.route('/pictures', methods=('GET',))
@login_required
def get_self_pictures():
    user_pictures = Picture.get_user_pictures() or list()
    return Picture.bulk_expose(user_pictures, 200)


@bp.route('/<user_id>/pictures', methods=('GET',))
@login_required
def get_other_pictures(user_id: int):
    user_pictures = Picture.get_user_pictures(user_id) or list()
    return Picture.bulk_expose(user_pictures, 200)


@bp.route('/picture', methods=('POST',))
@login_required
def add_picture():
    return Picture.create(dict(request.form))


@bp.route('/picture/<picture_id>', methods=('PUT', 'DELETE',))
@login_required
def update_picture(picture_id: int):
    """
        When a picture is added or changed, if the form indicates that this picture is going
        to be the main one, we'll run a request to make sure all the others pictures of the
        user get their 'main' field set to 0.
    """
    if request.method == 'DELETE':
        Picture.delete("id", picture_id)
    elif request.method == 'PUT':
        if BooleanField().db_format(request.form['main']):
            Picture.safe_update({'main': 0}, on_col='user_id', for_val=session['user_id'])
        Picture.safe_update(request.form, "id", picture_id)
    user_pictures = Picture.get_user_pictures() or list()
    return Picture.bulk_expose(user_pictures, 200)

