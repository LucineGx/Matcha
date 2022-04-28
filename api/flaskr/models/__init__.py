from flaskr.models.profile import Profile
from flaskr.models.tag import Tag
from flaskr.models.type import Type
from flaskr.models.egg_group import EggGroup
from flaskr.models.user import User

"""
The order of this list is important because some models contains foreign key that create a
dependency between them.
"""
models = [
    Type,
    EggGroup,
    Tag,
    User,
    Profile,
]
