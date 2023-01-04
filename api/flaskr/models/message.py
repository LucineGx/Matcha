from typing import Union

from flask import Response, session, Blueprint, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, DatetimeField, BooleanField, CharField, PositiveIntegerField
from flaskr.utils import login_required
from flaskr.db.utils import get_db

from .user import User


class Message(BaseModel):
    """
    Store messages between two users.
    We will need to know if the destination user already has read a message or not.
    """
    name = "message"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True, unique=True),
        "author_user_id": ForeignKeyField(to=User),
        "destination_user_id": ForeignKeyField(to=User, required=True),
        "datetime": DatetimeField(),
        "read": BooleanField(required=True),
        "last": BooleanField(),
        "content": CharField(required=True, max_length=1580, authorized_characters="^[a-zA-Zéèêàùûô0-9_\-.#^'¨%,;:?!@ \x0d\x0a]*$")
    }

    @classmethod
    def create(cls, form: dict) -> tuple[Union[str, Response], int]:
        form["author_user_id"] = session["user_id"]
        form["read"] = 0
        form["last"] = 1
        return cls._create(form, expose=False)


bp = Blueprint("messages", __name__, url_prefix="")


# TODO: add last_messages route to return the last message only for all the discussions
@bp.route("messages/<user_id>", methods=("GET", "POST"))
@login_required
def get_or_create_message(user_id: int):
    """
    Mark as read all the messages return by GET where the current user is the destination user.
    """
    user_id = int(user_id)
    users = [user_id, session["user_id"]]
    if request.method == "GET":
        messages = Message.get(
            on_col=["author_user_id", "destination_user_id"],
            for_val=[users, users],
        ).fetchall()
        Message.update({"read": 1}, {"author_user_id": user_id, "destination_user_id": session["user_id"]})
        return Message.bulk_expose(messages, 200)
    if request.method == "POST":
        Message.update({"last": 0}, {"author_user_id": users, "destination_user_id": users})
        return Message.create(dict(request.form))


@bp.route("last_messages", methods=("GET",))
@login_required
def get_all_last_messages():
    """
    Return the last message of each conversation with other users
    """
    db = get_db()
    user_id = session["user_id"]
    messages = db.execute(f"SELECT * FROM {Message.name} WHERE last = 1 and (author_user_id = {user_id} or destination_user_id = {user_id})").fetchall()
    return Message.bulk_expose(messages, 200)



