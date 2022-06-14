from typing import Tuple, Union

from flask import Blueprint, request, Response, session

from flaskr.db.utils import get_db
from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, CharField, ChoiceField, PositiveTinyIntegerField, ForeignKeyField, BooleanField
from flaskr.utils import login_required
from .user import User


get_bool_value = lambda value: 1 if (value is not None and int(value) != 0) else 0


class Profile(BaseModel):
    name = "profile"

    fields = {
        "user_id": ForeignKeyField(to=User, primary_key=True),
        "age": PositiveIntegerField(min=18, max=200, required=True),
        "gender": ChoiceField(max_length=6,  required=True, choice=["female", "male", "other"]),
        "search_female": BooleanField(),
        "search_male": BooleanField(),
        "search_other": BooleanField(),
        "short_bio": CharField(max_length=280, null=True),
        "public_popularity": PositiveTinyIntegerField(max=100, null=True),
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        db = get_db()
        form["user_id"] = session["user_id"]
        try:
            return cls._create(form, "user_id")
        except db.IntegrityError:
            return f"User {session['user_id']} has already defined a profile", 409
    
    @classmethod
    def compute_popularity_score(cls, user_id: int) -> None:
        from .like import Like
        from .visit import Visit

        num_likes = len(Like.get('host_user_id', user_id).fetchall())
        num_unique_visitors = len(Visit.get('host_user_id', user_id, distinct="guest_user_id").fetchall())
        popularity_score = (num_likes / num_unique_visitors) * 100

        if popularity_score > 0:
            cls.update(form={"public_popularity": popularity_score}, conditions={"user_id": user_id})



bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route('/', methods=('GET', 'POST', 'PUT', 'DELETE'))
@login_required
def self_profile():
    if request.method == "POST":
        return Profile.create(dict(request.form))

    if request.method == "GET":
        return Profile.expose("user_id", session["user_id"], 200)

    elif request.method == "PUT":
        return Profile.safe_update(request.form, "user_id", session["user_id"])

    elif request.method == "DELETE":
        Profile.delete("user_id", session["user_id"])
        return "Profile successfully deleted", 200


@bp.route('/<user_id>', methods=('GET',))
@login_required
def other_profile(user_id: int):
    # To do: don't count as visit if guest's id is the same as host id
    from .like import Like
    from .visit import Visit
    Visit.create({"host_user_id": user_id, "guest_user_id": session['user_id']})
    liked = Like.is_profile_liked(user_id)
    return Profile.expose("user_id", user_id, 200, custom_fields={"liked": liked})
