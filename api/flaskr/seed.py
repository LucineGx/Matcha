import click
from flask.cli import with_appcontext
from faker import Faker
from faker.providers import BaseProvider
from random import choices, choice
from werkzeug.security import generate_password_hash

from flaskr.models import User


@click.command('seed')
@click.argument('num')
@with_appcontext
def create_seed(num):
    """
    Generate a seed of several complete profiles
    """
    seed = [generate_profile() for _ in range(int(num))]
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
    

def generate_profile() -> dict:
    fake = Faker('fr_FR')
    fake.add_provider(CustomProvider)
    profile = fake.profile()
    first_name, last_name = profile['name'].split(' ', 1)
    default_gender = 'male' if profile['sex'] == 'M' else 'female'
    gender = choices([default_gender, 'other'], [0.96, 0.04], k=1)[0]
    return { **{
        'email': profile['mail'],
        'username': profile['username'],
        'first_name': first_name,
        'last_name': last_name,
        'password': generate_password_hash(fake.password()),
        'custom_localisation': 1,
        'lat': float(profile['current_location'][0]),
        'lon': float(profile['current_location'][1]),
        'confirmed': 1,
        'age': fake.age(),
        'gender': gender,
        'short_bio': fake.text(max_nb_chars=280),
    }, **(fake.searched_genders(gender))}


class CustomProvider(BaseProvider):
    def age(self) -> int:
        age_by_range = [
            choice(range(23, 36)),
            choice(range(36, 44)),
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
