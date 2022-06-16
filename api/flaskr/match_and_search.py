import pandas as pd
from geopy import distance
from typing import List, Any

from flask import request, g

from flaskr.models import User, BlockedUser, Like, Tag, UserTag
from flaskr.models.user import bp
from flaskr.utils import login_required, get_db


@bp.route('/match-me', methods=('GET',))
@login_required
def match_me():
    # Remove self, blocked and liked users from the result
    # To do: uncomment those when seed is ready for greater tests
    # blocked_user_ids = [row[0] for row in BlockedUser.get('user_id', g.user['id'], distinct='blocked_user_id').fetchall()]
    # liked_user_ids = [row[0] for row in Like.get('guest_user_id', g.user['id'], distinct='host_user_id').fetchall()]
    # excluded_from_match = list(set(blocked_user_ids + liked_user_ids)) + [g.user['id']]

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
        # excluded_cols=['id'],
        # excluded_vals=[excluded_from_match]
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
    pass


def build_search_query(
    table: str,
    gender_orientation: str,
    age_diff: str,
    popularity_diff: str,
    distance: str,
    tags: str
) -> str:
    return f'''
        SELECT * FROM {table}
        WHERE {gender_orientation}
        {age_diff}
        {popularity_diff}
        {distance}
        {tags}
    '''


def expose_request_results(query: str, values: List[Any]):
    db = get_db()
    results = (
        pd.DataFrame(db.execute(query, values).fetchall(), columns=list(User.fields))
        .pipe(assign_user_tags)
        .assign(**{
            'liked': lambda df: df['id'].apply(Like.is_user_liked)
        })
    )
    return User.bulk_expose(results.to_dict(orient='records'), 200, custom_fields=['tags', 'liked'])
