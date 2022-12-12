import functools
from typing import Tuple, List, Any, Optional, Union

from flask import request, g, current_app
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

def assign_profile_picture(users: pd.DataFrame) -> pd.DataFrame:
    from flaskr.models import Picture
    return users.assign(**{
        'picture': lambda df: df['id'].apply(
            lambda user_id: Picture.get_user_profile_picture(user_id)
        )
    })


def get_gender_filter() -> str:
    if not g.user["gender"]:
        return ""
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


def get_excluded_users(with_liked: bool) -> str:
    if with_liked:
        excluded_users = get_blocked_users() + get_liked_users()
    else: 
        excluded_users = get_blocked_users()
    if excluded_users:
        return f'AND id NOT IN ({", ".join([str(user[0]) for user in excluded_users])}) '
    return ''


def get_blocked_users() -> str:
    from flaskr.models import BlockedUser
    return BlockedUser.get('user_id', g.user['id'], distinct='blocked_user_id').fetchall() or list()


def get_liked_users() -> str:
    from flaskr.models import Like
    return Like.get('guest_user_id', g.user['id'], distinct='host_user_id').fetchall() or list()


def execute_search(
    raw_values: List[Any],
    gender_orientation: str,
    excluded_users: str = '',
    age_interval: str = '',
    popularity_interval: str = '',
    tag_users: str = '',
) -> str:
    from flaskr.models import User
    query = f'''
        SELECT * FROM user
        WHERE {gender_orientation}
        {excluded_users}
        {age_interval}
        {popularity_interval}
        {tag_users}
    '''
    db = get_db()
    return pd.DataFrame(db.execute(query, raw_values).fetchall(), columns=list(User.fields))


def filter_distant_users(users: pd.DataFrame, default_threshold: Optional[float] = None) -> pd.DataFrame:
    user_geoloc = (g.user['lat'], g.user['lon'])
    users = users.assign(**{
        'distance_from_user': lambda df: (
            pd.Series(df[['lat', 'lon']].itertuples(index=False, name=None))
            .apply(lambda geoloc: distance.distance(geoloc, user_geoloc).km)
        ),
    })
    distance_threshold = request.args.get('distance_max', default_threshold)
    if distance_threshold:
        users = users[users['distance_from_user'].le(float(distance_threshold))]
    return users


def assign_likes(users: pd.DataFrame) -> pd.DataFrame:
    from flaskr.models import Like
    return users.assign(**{'liked': lambda df: df['id'].apply(Like.is_user_liked)})


def count_common_tags_points(users: pd.DataFrame) -> Union[pd.Series, int]:
    from flaskr.models import UserTag

    user_tags = UserTag.get('user_id', g.user['id']).fetchall()
    if user_tags:
        common_tags = pd.DataFrame(
            UserTag.get('tag_name', [tag['tag_name'] for tag in user_tags]).fetchall(),
            columns = list(UserTag.fields)
        )
        user_id_to_num_common_tags = common_tags.groupby('user_id').count()['tag_name']
        return users['id'].map(user_id_to_num_common_tags) * 2

    else:
        return 0


def count_popularity_diff_points(users: pd.DataFrame) -> pd.Series:
    populariry_diff_points = (
        users['public_popularity']
        .fillna(0)
        .apply(lambda popularity: 5 - abs(g.user['public_popularity'] - popularity) // 10)
    )
    populariry_diff_points.loc[populariry_diff_points < 0] = 0

    return populariry_diff_points
