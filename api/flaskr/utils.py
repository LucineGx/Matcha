import functools
from typing import Tuple, List, Any

from flask import request, g
import pandas as pd
from geopy import distance

from flaskr.db.utils import get_db


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return "Unauthorized", 401

        return view(**kwargs)

    return wrapped_view


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


def execute_search(
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
