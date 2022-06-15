import pandas as pd
from geopy import distance
from typing import Tuple, Union

from flask import Blueprint, request, session, Response, jsonify, g
from werkzeug.security import generate_password_hash

from flaskr.db.utils import get_db
from flaskr.db.fields import CharField, PositiveIntegerField, DatetimeField, do_nothing, BooleanField, FloatField, ChoiceField, PositiveTinyIntegerField
from flaskr.db.base_model import BaseModel
from flaskr.utils import login_required
from flaskr.validators import validate_email, validate_password


# To do: email should be exposed for self, but not for other users
class User(BaseModel):
    name = "user"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True),
        "email": CharField(
            max_length=64, authorized_characters="^[a-zA-Z0-9_\-.@]*$", unique=True, null=False, required=True, custom_validate=validate_email, expose=False
        ),
        "username": CharField(unique=True, required=True),
        "first_name": CharField(required=True, expose=False),
        "last_name": CharField(required=True, expose=False),
        "password": CharField(
            min_length=8,
            authorized_characters="^[a-zA-Z0-9_\-.#^¨%,;:?!@]*$",
            required=True,
            expose=False,
            custom_validate=validate_password,
            db_format=generate_password_hash
        ),
        "custom_localisation": BooleanField(expose=False),
        "lat": FloatField(min=-90, max=90, required=True, default=48.8966148),
        "lon": FloatField(min=-180, max=180, required=True, default=2.3183559),
        "created_on": DatetimeField(),
        "confirmed": BooleanField(db_format=do_nothing, expose=False),
        "confirmation_token": CharField(unique=True, null=True, expose=False), # To do: call create_confirmation_token in register function
        "password_reinit_token": CharField(unique=True, null=True, expose=False),
        "age": PositiveIntegerField(min=18, max=200, null=True),
        "gender": ChoiceField(max_length=6, choice=["female", "male", "other"], null=True),
        "search_female": BooleanField(default=True),
        "search_male": BooleanField(default=True),
        "search_other": BooleanField(default=True),
        "short_bio": CharField(max_length=280, null=True),
        "public_popularity": PositiveTinyIntegerField(max=100, null=True),
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        db = get_db()
        try:
            return cls._create(form, "username")
        except db.IntegrityError:
            return f"{form['email']} is already registered", 409
    
    @classmethod
    def compute_popularity_score(cls, user_id: int) -> None:
        from .like import Like
        from .visit import Visit

        num_likes = len(Like.get('host_user_id', user_id).fetchall())
        num_unique_visitors = len(Visit.get('host_user_id', user_id, distinct="guest_user_id").fetchall())
        popularity_score = (num_likes / num_unique_visitors) * 100

        if popularity_score > 0:
            cls.update(form={"public_popularity": popularity_score}, conditions={"id": user_id})


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=('GET', 'PUT', 'DELETE'))
@login_required
def user():
    if request.method == 'GET':
        user = {
            name: value
            for name, value in dict(g.user).items()
            if User.fields[name].expose
            or name in ['email', 'first_name', 'last_name', 'custom_localisation']
        }
        return jsonify(user), 200

    elif request.method == 'PUT':
        if "username" in request.form:
            return "Unmuttable username", 401
        return User.safe_update(request.form, "id", g.user["id"])

    elif request.method == "DELETE":
        User.delete("id", g.user["id"])
        session.clear()
        return "User successfully deleted", 200



@bp.route('/<user_id>', methods=('GET',))
@login_required
def other_user(user_id: int):
    # To do: don't count as visit if guest's id is the same as host id
    from .like import Like
    from .visit import Visit
    Visit.create({"host_user_id": user_id, "guest_user_id": g.user["id"]})
    liked = Like.is_user_liked(user_id)
    return User.expose("id", user_id, 200, custom_fields={"liked": liked})


@bp.route('/match-me', methods=('GET',))
@login_required
def match_me():
    # select only relevant genders for the user
    search_genders = [
        gender
        for gender in {'male', 'female', 'other'}
        if g.user[f'search_{gender}']
    ]
    matching_users = User.get('gender', search_genders).fetchall()
    if not matching_users:
        return "No user found for given criteria", 404
    
    # keep user at suitable distance from the user
    user_geoloc = (g.user['lat'], g.user['lon'])
    matching_users = pd.DataFrame(matching_users, columns=list(User.fields)).assign(**{
        'distance_from_match': lambda df: (
            pd.Series(df[['lat', 'lon']].itertuples(index=False, name=None))
            .apply(lambda geoloc: distance.distance(geoloc, user_geoloc).km)
        )
    })
    distance_threshold = float(request.args.get('distance_max', 50))

    matching_users = matching_users[matching_users['distance_from_match'].le(distance_threshold)]

    # Count comon tags with each matching user
    from flaskr.models import UserTag
    user_tags = UserTag.get('user_id', g.user['id']).fetchall()
    if user_tags:
        matched_tags = pd.DataFrame(UserTag.get('tag_name', [tag['tag_name'] for tag in user_tags]).fetchall(), columns=list(UserTag.fields))
        user_id_to_num_matched_tags = matched_tags.groupby('user_id').count()['tag_name']
        tag_points = matching_users['id'].map(user_id_to_num_matched_tags) * 2
    else:
        tag_points = 0
    matching_users = matching_users.assign(**{'tag_points': tag_points})

    # To do: provide a user from mathing himself
    # To do: remove blocked and liked users from the result
    # To do: expose tags for each user
    return jsonify(matching_users.to_dict(orient='records')), 200
