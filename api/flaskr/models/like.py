from typing import Tuple, Union

from flask import Response, session, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, DatetimeField
from flaskr.utils import login_required

from .profile import bp
from .user import User


class Like(BaseModel):
    """
    Users must be able to consult who liked their profile.
    When a user unlike an other, the like is simply removed from the table.
    """
    name = "like"

    fields = {
        "host_user_id": ForeignKeyField(to=User, expose=False),
        "guest_user_id": ForeignKeyField(to=User),
        "liked_on": DatetimeField()
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        if not cls.is_profile_liked(form['host_user_id']):
            form['guest_user_id'] = session['user_id']
            return cls._create(form, expose=False)
        else:
            return "Profile liked already", 409
    
    @classmethod
    def is_profile_liked(cls, user_id: int) -> bool:
        return cls.get(
            on_col=['host_user_id', 'guest_user_id'], for_val=[user_id, session['user_id']]
        ).fetchone() is not None


@bp.route('/likes', methods=('GET',))
@login_required
def list_likes():
    likes = Like.get('host_user_id', session['user_id']).fetchall()
    return Like.bulk_expose(likes, 200)


@bp.route('/<user_id>/like', methods=('POST', 'DELETE'))
@login_required
def like_profile(user_id: int):
    
    if request.method == 'POST':
        return Like.create({"host_user_id": user_id})

    elif request.method == 'DELETE':
        Like.delete(on_col=["host_user_id", "guest_user_id"], for_val=[user_id, session['user_id']])
        return "Profile unliked", 200

    
