from typing import Union

from flask import Response, session, Blueprint, request

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import ForeignKeyField, DatetimeField, BooleanField, CharField, PositiveIntegerField
from flaskr.utils import login_required

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
        "content": CharField(required=True, max_length=1580, authorized_characters="^[a-zA-Zéèêàùûô0-9_\-.#^'¨%,;:?!@ \x0d\x0a]*$")
    }

    @classmethod
    def create(cls, form: dict) -> tuple[Union[str, Response], int]:
        form["author_user_id"] = session["user_id"]
        form["read"] = 0
        return cls._create(form, expose=False)


bp = Blueprint("messages", __name__, url_prefix="/messages")


# TODO: add last_messages route to return the last message only for all the discussions
@bp.route("/<user_id>", methods=("GET", "POST"))
@login_required
def get_or_create_message(user_id: int):
    """
    Mark as read all the messages return by GET where the current user is the destination user.
    """
    user_id = int(user_id)
    if request.method == "GET":
        users = [user_id, session["user_id"]]
        messages = Message.get(
            on_col=["author_user_id", "destination_user_id"],
            for_val=[users, users],
        ).fetchall()
        Message.update({"read": 1}, {"author_user_id": user_id, "destination_user_id": session["user_id"]})
        return Message.bulk_expose(messages, 200)
    if request.method == "POST":
        return Message.create(dict(request.form))

#@bp.route("/lasts", methods=("GET",))
#@login_required
#def get_all_last_messages():

