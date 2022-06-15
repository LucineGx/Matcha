from typing import Tuple, Union

from flask import Response, session, request


from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField
from flaskr.utils import login_required

from .user import User, bp


class BlockedUser(BaseModel):
    """
    Users must be able to block each-others.
    A blocked user shouldn't appear in search results, and shouldnt trigger notifications.

    We need to be able to
        - block a user
        - list all blocked users
        - unblock a user
    """
    name = "blocked_user"

    fields = {
        "user_id": ForeignKeyField(to=User, expose=False),
        "blocked_user_id": ForeignKeyField(to=User)
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        if not cls.is_user_blocked(form['blocked_user_id']):
            form['user_id'] = session['user_id']
            return cls._create(form, expose=False)
        else:
            return "User blocked already", 409
    
    @classmethod
    def is_user_blocked(cls, user_id: int) -> bool:
        return cls.get(
            on_col=['blocked_user_id', 'user_id'], for_val=[user_id, session['user_id']]
        ).fetchone() is not None


@bp.route('/blocked_users', methods=('GET',))
@login_required
def list_blocked_users():
    blocked_users = BlockedUser.get('user_id', session['user_id']).fetchall()
    return BlockedUser.bulk_expose(blocked_users, 200)


@bp.route('/<user_id>/block', methods=('POST', 'DELETE'))
@login_required
def block_user(user_id: int):

    if request.method == 'POST':
        return BlockedUser.create({"blocked_user_id": user_id})
    
    elif request.method == 'DELETE':
        BlockedUser.delete(on_col=["blocked_user_id", "user_id"], for_val=[user_id, session['user_id']])
        return "User unblocked", 200
