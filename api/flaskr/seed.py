import os
from typing import List
from random import choices, choice, shuffle, randint
from itertools import repeat
from functools import partial

import click
from flask.cli import with_appcontext
from faker import Faker
from faker.providers import BaseProvider
from werkzeug.security import generate_password_hash

from flaskr.models import User, Picture, UserTag, Visit, Like
from flaskr.models.tag import DEFAULT_TAGS
from flaskr.utils import execute_search


times = partial(repeat, None)


@click.command('seed')
@click.argument('num')
@with_appcontext
def create_seed(num):
    """
    Generate a seed of several complete profiles
    """
    num = int(num)
    fake = Faker('fr_FR', use_weighting=False)
    fake.add_provider(CustomProvider)

    seed = [generate_profile(fake) for _ in times(num)]
    User.bulk_create(
        columns=(
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'custom_localisation',
            'lat',
            'lon',
            'confirmed',
            'age',
            'gender',
            'short_bio',
            'search_female',
            'search_male',
            'search_other'
        ),
        values=[tuple(profile.values()) for profile in seed]
    )
    first_id = User.get("email", seed[0]['email']).fetchone()['id']

    user_pictures = [get_pictures(fake, first_id + idx) for idx in range(num)]
    Picture.bulk_create(columns=('user_id', 'picture', 'main'), values=user_pictures)

    user_tags = [get_tags(fake, first_id + idx) for idx in range(num)]
    UserTag.bulk_create(columns=('user_id', 'tag_name', 'hidden'), values=[tag for single_user_tags in user_tags for tag in single_user_tags])

    for idx, user in enumerate(seed):
        generate_visits(fake, first_id + idx, user)
    
    for idx in range(num):
        User.compute_popularity_score(first_id + idx)
    

def generate_profile(fake: Faker) -> dict:
    profile = fake.profile()
    first_name, last_name = profile['name'].split(' ', 1)
    default_gender = 'male' if profile['sex'] == 'M' else 'female'
    gender = choices([default_gender, 'other'], [0.96, 0.04], k=1)[0]
    return { **{
        'email': profile['mail'],
        'username': profile['username'],
        'first_name': first_name,
        'last_name': last_name,
        'password': generate_password_hash('Azerty;123'),
        'custom_localisation': 1,
        # To do make sure the lat/lon are in France, if not use fake.local_latlng()
        'lat': float(profile['current_location'][0]),
        'lon': float(profile['current_location'][1]),
        'confirmed': 1,
        'age': fake.age(),
        'gender': gender,
        'short_bio': fake.text(max_nb_chars=280),
    }, **(fake.searched_genders(gender))}


def get_pictures(fake: Faker, user_id) -> tuple:
    return user_id, fake.picture(), 1


def get_tags(fake: Faker, user_id) -> List[tuple]:
    return [(user_id, tag_name, 0) for tag_name in fake.tags()]


def generate_visits(fake: Faker, user_id, user) -> List[tuple]:
    visited_users = fake.visit_users(user)
    visits = [(visited_user_id, user_id) for visited_user_id in visited_users['id']]
    likes = [(visited_user_id, user_id) for visited_user_id in visited_users[visited_users['liked'] == True]['id']]
    Visit.bulk_create(columns=('host_user_id', 'guest_user_id'), values=visits)
    if likes:
        Like.bulk_create(columns=('host_user_id', 'guest_user_id'), values=likes)


class CustomProvider(BaseProvider):
    def age(self) -> int:
        age_by_range = [
            randint(23, 35),
            randint(36, 43),
            choice(list(range(18, 23)) + list(range(44, 60)))
        ]
        return choices(age_by_range, [0.6, 0.25, 0.15])[0]
    
    def searched_genders(self, user_gender) -> dict:
        if user_gender == 'other':
            searched_genders = choices(
                [
                    ('female', 'other'),
                    ('female', 'male', 'other'),
                    ('male', 'other'),
                    ('male'),
                    ('female'),
                    ('other')
                ],
                [0.35, 0.3, 0.22, 0.05, 0.05, 0.03]
            )[0]
        else:
            opposite = 'female' if user_gender == 'male' else 'male'
            same = 'female' if user_gender == 'female' else 'male'
            searched_genders = choices(
                [
                    (opposite,),
                    ('female', 'male', 'other'),
                    (same, 'other'),
                    (opposite, 'other'),
                    (same,),
                    ('other'),
                    ('female', 'male')
                ],
                [0.6, 0.15, 0.12, 0.05, 0.05, 0.02, 0.01]
            )[0]
        return {
            f'search_{gender}': 1 if gender in searched_genders else 0
            for gender in ['female', 'male', 'other']
        }

    def picture(self) -> object:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = f'{root_dir}/../../resources/pp_{randint(1,15)}.jpg'
        with open(file_name, 'rb') as file:
            return file.read()
    
    def tags(self) -> List[str]:
        tag_names = list(DEFAULT_TAGS.keys())
        shuffle(tag_names)
        return [
            tag_names.pop()
            for _ in times(randint(1, 11))
        ]
    
    def visit_users(self, user: dict) -> List[int]:
        search_genders = [
            f"'{gender}'"
            for gender in {'male', 'female', 'other'}
            if user[f'search_{gender}']
        ]
        gender_orientation = f'gender IN ({", ".join(search_genders)}) AND search_{user["gender"]} = 1 '
        users = execute_search([], gender_orientation)
        num_visits = randint(1, 25)
        if num_visits < users.shape[0]:
            users = users.sample(num_visits)
        like_probabilities = [0.5, 0.5] if user['gender'] == 'male' else [0.3, 0.7]
        likes = [
            choices([True, False], like_probabilities)[0]
            for _ in times(users.shape[0])
        ]
        return users.assign(**{'liked': likes})
