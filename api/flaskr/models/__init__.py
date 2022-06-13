from flaskr.models.block import BlockedUser
from flaskr.models.egg_group import EggGroup
from flaskr.models.like import Like
from flaskr.models.picture import Picture
from flaskr.models.profile import Profile
from flaskr.models.tag import Tag
from flaskr.models.type import Type
from flaskr.models.user import User
from flaskr.models.user_tag import UserTag
from flaskr.models.visit import Visit

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
    UserTag,
    Picture,
    Like,
    Visit,
    BlockedUser
]
