from typing import Tuple, Union, List, Any

from flask import Blueprint, request, session, Response, jsonify, g
from werkzeug.security import generate_password_hash
import pandas as pd
from geopy import distance

from flaskr.utils import login_required
from flaskr.db.utils import get_db
from flaskr.db.fields import CharField, PositiveIntegerField, DatetimeField, do_nothing, BooleanField, FloatField, ChoiceField, PositiveTinyIntegerField
from flaskr.db.base_model import BaseModel
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
        "first_name": CharField(required=True),
        "last_name": CharField(required=True),
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
            or name in ['email', 'custom_localisation']
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


@bp.route('/<user_id>/', methods=('GET',))
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
    from flaskr.models import BlockedUser, Like, UserTag
    # To do: clean code and use as much logic as possible fron search

    # Remove self, blocked and liked users from the result
    # To do: uncomment those when seed is ready for greater tests
    blocked_user_ids = [row[0] for row in BlockedUser.get('user_id', g.user['id'], distinct='blocked_user_id').fetchall()]
    liked_user_ids = [row[0] for row in Like.get('guest_user_id', g.user['id'], distinct='host_user_id').fetchall()]
    excluded_from_match = list(set(blocked_user_ids + liked_user_ids)) + [g.user['id']]

    # select only relevant genders for the user, and reciprocally 
    search_genders = [
        gender
        for gender in {'male', 'female', 'other'}
        if g.user[f'search_{gender}']
    ]
    matching_users = User.bulk_get(
        on_cols=['gender', f'search_{g.user["gender"]}'], 
        for_vals=[search_genders, 1],
        # To do: uncomment those when seed is ready for greater tests
        excluded_cols=['id'],
        excluded_vals=[excluded_from_match]
    )
    if not matching_users:
        return "No user found for given criteria", 404
    
    # Keep user at suitable distance from the user
    user_geoloc = (g.user['lat'], g.user['lon'])
    matching_users = pd.DataFrame(matching_users, columns=list(User.fields)).assign(**{
        'distance_from_match': lambda df: (
            pd.Series(df[['lat', 'lon']].itertuples(index=False, name=None))
            .apply(lambda geoloc: distance.distance(geoloc, user_geoloc).km)
        ),
        'public_popularity' : lambda df: df['public_popularity'].fillna(0)
    })
    distance_threshold = float(request.args.get('distance_max', 50))

    matching_users = matching_users[matching_users['distance_from_match'].le(distance_threshold)]

    if not matching_users.empty:
        # Count comon tags with each matching user
        user_tags = UserTag.get('user_id', g.user['id']).fetchall()
        if user_tags:
            matched_tags = pd.DataFrame(
                UserTag.get('tag_name', [tag['tag_name'] for tag in user_tags]).fetchall(),
                columns=list(UserTag.fields)
            )
            user_id_to_num_matched_tags = matched_tags.groupby('user_id').count()['tag_name']
            tag_points = matching_users['id'].map(user_id_to_num_matched_tags) * 2
        else:
            tag_points = 0
        matching_users = matching_users.assign(**{'tag_points': tag_points})

        # Count popularity diff points with each matching user
        matching_users = matching_users.assign(**{
            'popularity_points': lambda df: (
                df['public_popularity']
                .apply(lambda popularity: 5 - abs(g.user['public_popularity'] - popularity) // 10)
            ).fillna(0)
        })
        matching_users.loc[matching_users['popularity_points'] < 0, 'popularity_points'] = 0

        # Sum points, sorts, keep the first 10th results
        matching_users = matching_users.assign(**{
            'matching_score': matching_users['tag_points'] + matching_users['popularity_points']
        }).sort_values('matching_score', ascending=False).head(10)

        # Expose tags for each user
        matching_users = assign_user_tags(matching_users)

    # To do: clean-up custom_fields points and score when testing phase is over
    return User.bulk_expose(matching_users.to_dict(orient='records'), 200, custom_fields=['distance_from_match' 'tag_points', 'popularity_points', 'matching_score', 'tags'])


def assign_user_tags(users: pd.DataFrame) -> pd.DataFrame:
    from flaskr.models import Tag, UserTag
    return users.assign(**{
        'tags': lambda df: df['id'].apply(
            lambda user_id: [
                dict(Tag.get('name', user_tag['tag_name']).fetchone())
                for user_tag in UserTag.get('user_id', user_id).fetchall()
            ]
        )
    })


@bp.route('/search', methods=('GET',))
@login_required
def search_users():
    gender_orientation = get_gender_filter()
    age_interval, age_values = get_interval_filter('age')
    popularity_interval, popularity_values = get_interval_filter('public_popularity')
    tag_users = get_tag_filter()
    blocked_users = get_blocked_users()

    users = (
        execute_query(
            gender_orientation,
            age_interval,
            popularity_interval,
            tag_users,
            blocked_users,
            age_values + popularity_values
        ).pipe(filter_distant_users)
        .pipe(assign_user_tags)
        .pipe(assign_likes)
    )
    return User.bulk_expose(users.to_dict(orient='records'), 200, custom_fields=['distance_from_user', 'tags', 'liked'])



def get_gender_filter() -> str:
    search_genders = [
        f"'{gender}'"
        for gender in {'male', 'female', 'other'}
        if g.user[f'search_{gender}']
    ]
    return f'gender IN ({", ".join(search_genders)}) AND search_{g.user["gender"]} = 1 '


def get_interval_filter(field: str) -> Tuple[str, list]:
    min = request.args.get(f'{field}_min', None)
    max = request.args.get(f'{field}_max', None)

    greater_than = f'AND {field} >= ? ' if min else ''
    lower_than = f'AND {field} <= ? ' if max else ''

    min_val = [min] if min else []
    max_val = [max] if max else []

    return greater_than + lower_than, min_val + max_val


def get_tag_filter() -> str:
    from flaskr.models import UserTag
    if requested_tags:= request.args.get("tags", None):
        user_ids = UserTag.get('tag_name', requested_tags.split('+'), distinct='user_id').fetchall()
        if user_ids:
            return f'AND id IN ({", ".join([str(user[0]) for user in user_ids])}) '
    return ''


def get_blocked_users() -> str:
    from flaskr.models import BlockedUser
    user_ids = BlockedUser.get('user_id', g.user['id'], distinct='blocked_user_id').fetchall()
    if user_ids:
        return f'AND id NOT IN ({", ".join([str(user[0]) for user in user_ids])}) '
    return ''


def execute_query(
    gender_orientation: str,
    age_interval: str,
    popularity_interval: str,
    tag_users: str,
    blocked_users: str,
    raw_values: List[Any]
) -> str:
    query = f'''
        SELECT * FROM user
        WHERE {gender_orientation}
        {age_interval}
        {popularity_interval}
        {tag_users}
        {blocked_users}
    '''
    db = get_db()
    return pd.DataFrame(db.execute(query, raw_values).fetchall(), columns=list(User.fields))


def filter_distant_users(users: pd.DataFrame) -> pd.DataFrame:
    user_geoloc = (g.user['lat'], g.user['lon'])
    users = users.assign(**{
        'distance_from_user': lambda df: (
            pd.Series(df[['lat', 'lon']].itertuples(index=False, name=None))
            .apply(lambda geoloc: distance.distance(geoloc, user_geoloc).km)
        ),
    })
    distance_threshold = request.args.get('distance_max', None)
    if distance_threshold:
        users = users[users['distance_from_user'] <= float(distance_threshold)]
    return users


def assign_likes(users: pd.DataFrame) -> pd.DataFrame:
    from flaskr.models import Like
    return users.assign(**{'liked': lambda df: df['id'].apply(Like.is_user_liked)})
