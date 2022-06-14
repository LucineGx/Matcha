from typing import Tuple, Union

from flask import Blueprint, Response

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ChoiceField, FixedCharField

EGG_GROUPS = {
    "Amorphous": "#8A8A8A",
    "Bug": "#AAC22A",
    "Ditto": "#A664BF",
    "Dragon": "#7A42FF",
    "Fairy": "#FFC8F0",
    "Field": "#E0C068",
    "Flying": "#B29AFA",
    "Grass": "#82D25A",
    "Human-like": "#D29682",
    "Mineral": "#7A6252",
    "Monster": "#D25064",
    "Undiscovered": "#333333",
    "Water 1": "#97B5FD",
    "Water 2": "#729AFA",
    "Water 3": "#5876BE",
}


# To do: cleab up
class EggGroup(BaseModel):
    name = "egg_group"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True),
        "name": ChoiceField(max_length=8, choice=list(EGG_GROUPS.keys())),
        "color": FixedCharField(length=7, authorized_characters="^[0-9#]*$", )
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        return cls._create(form, "name")

    @classmethod
    def fill_table(cls) -> None:
        cls.bulk_create(
            columns=("name", "color"),
            values=[(name, color) for name, color in EGG_GROUPS.items()]
        )


bp = Blueprint("egg_group", __name__, url_prefix="/egg_groups")


@bp.route('', methods=("GET",))
def list_types():
    return EggGroup.list()
