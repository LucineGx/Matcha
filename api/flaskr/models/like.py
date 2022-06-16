from typing import Tuple, Union

from flask import Response, g, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, DatetimeField
from flaskr.utils import login_required

from .user import User, bp


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
        if not cls.is_user_liked(form['host_user_id']):
            form['guest_user_id'] = g.user['id']
            response = cls._create(form, expose=False)
            User.compute_popularity_score(form['host_user_id'])
            return response
        else:
            return "User liked already", 409
    
    @classmethod
    def is_user_liked(cls, user_id: int) -> bool:
        return cls.get(
            on_col=['host_user_id', 'guest_user_id'], for_val=[user_id, g.user['id']]
        ).fetchone() is not None


@bp.route('/received_likes', methods=('GET',))
@login_required
def received_likes():
    likes = Like.get('host_user_id', g.user['id']).fetchall()
    return Like.bulk_expose(likes, 200)


@bp.route('/given_likes', methods=('GET',))
@login_required
def given_likes():
    likes = Like.get('guest_user_id', g.user['id']).fetchall()
    return Like.bulk_expose(likes, 200)


@bp.route('/<user_id>/like', methods=('POST', 'DELETE'))
@login_required
def like_user(user_id: int):
    
    if request.method == 'POST':
        # To do: provide a user from liking himself
        return Like.create({"host_user_id": user_id})

    elif request.method == 'DELETE':
        Like.delete(on_col=["host_user_id", "guest_user_id"], for_val=[user_id, g.user['id']])
        return "User unliked", 200

    
