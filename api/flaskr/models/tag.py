import random
from typing import Tuple, Union

from flask import Blueprint, Response

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import CharField
from flaskr.utils import login_required


DEFAULT_TAGS = {
    'Red': '#F4854C',
    'Green': '#95CB1D',
    'Blue': '#8BD8FE',
    'Yellow': '#FDDC79',
    'Gold': '#F9F573',
    'Silver': '#C0CAD3',
    'Cristal': '#4FBA9F',
    'Ruby': '#CC2725',
    'Sapphire': '#2F64B1',
    'Fire Red': '#F4854C',
    'Leaf Green': '#95CB1D',
    'Emerald': '#2C9A38',
    'Diamond': '#007B96',
    'Perl': '#AB6783',
    'Platinum': '#FEFEFE',
    'Heart Gold': '#F9F573',
    'Soul Silver': '#C0CAD3',
    'Black': '#000000',
    'White': '#FFFFFF',
    'Black 2': '#AB949F',
    'White 2': '#D4E2DE',
    'X': '#50AFB1',
    'Y': '#EF7870',
    'Omega Ruby': '#CC2725',
    'Alpha Sapphire': '#2F64B1',
    'Sun': '#F7BD101',
    'Moon': '#14A0DE',
    'Ultra Sun': '#C37E58',
    'Ultra Moon': '#AA7BAF',
    "Let's Go Pikachu": '#FEE469',
    "Let's Go Evoli": '#D99F5C',
    'Sword': '#4785C1',
    'Shield': '#AD3F41',
    'Brillant Diamond': '#007B96',
    'Shinning Perl': '#AB6783',
    'Legends Arceus': '#75BF94',
    'Scarlet': '#D8443D',
    'Violet': '#B447B2',
    'Kanto': '#5D0D6E',
    'Johto': '#ED4353',
    'Hoenn': '#FED440',
    'Sinnoh': '#3CCDB4',
    'Unova': '#0FAC71',
    'Kalos': '#CB9DAE',
    'Alola': '#F6CCB0',
    'Galar': '#C684B5',
    'Hisui': '#806886'
}


class Tag(BaseModel):
    name = "tag"

    fields = {
        "name": CharField(primary_key=True, unique=True, required=True),
        "color": CharField(authorized_characters="^[0-9abcdefx]*$", )
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        form["color"] = str(hex(random.randint(0, 0xffffff)))
        return cls._create(form, "name")

    @classmethod
    def fill_table(cls) -> None:
        if not cls._list():
            cls.bulk_create(
                columns=("name", "color"),
                values=[(name, color) for name, color in DEFAULT_TAGS.items()]
            )


bp = Blueprint("tag", __name__, url_prefix="/tag")


@bp.route('/', methods=("GET",))
@login_required
def get_all_tags():
    return Tag.list()


@bp.route('/<tag_name>', methods=("GET",))
@login_required
def _get_or_create_tag(tag_name: str):
    return get_or_create_tag(tag_name)


def get_or_create_tag(tag_name: str):
    tag, status_code = Tag.expose("name", tag_name, 200)

    if status_code == 404:
        return Tag.create({"name": tag_name})

    return tag, status_code
