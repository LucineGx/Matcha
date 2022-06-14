from typing import Tuple, Union

from flask import Blueprint, Response

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ChoiceField, FixedCharField

TYPES = {
    "Bug": "#A8B820",
    "Dark": "#705848",
    "Dragon": "#7038F8",
    "Electric": "#F8D030",
    "Fairy": "#EE99AC",
    "Fighting": "#C03028",
    "Fire": "#F08030",
    "Flying": "#A890F0",
    "Ghost": "#705898",
    "Grass": "#78C850",
    "Ground": "#E0C068",
    "Ice": "#98D8D8",
    "Normal": "#A8A878",
    "Poison": "#A040A0",
    "Psychic": "#F85888",
    "Rock": "#B8A038",
    "Steel": "#B8B8D0",
    "Water": "#6890F0",
}


# To do: clean up
class Type(BaseModel):
    name = "type"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True),
        "name": ChoiceField(max_length=8, choice=list(TYPES.keys())),
        "color": FixedCharField(length=7, authorized_characters="^[0-9#]*$", )
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        return cls._create(form, "name")

    @classmethod
    def fill_table(cls) -> None:
        cls.bulk_create(
            columns=("name", "color"),
            values=[(name, color) for name, color in TYPES.items()]
        )


bp = Blueprint("type", __name__, url_prefix="/types")


@bp.route('', methods=("GET",))
def list_types():
    return Type.list()
