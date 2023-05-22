from typing import Tuple, Union
from datetime import datetime

from flask import Response, session

from flaskr.db.base_model import BaseModel
from flaskr.db.fields import PositiveIntegerField, ForeignKeyField, DatetimeField
from flaskr.utils import login_required

from .user import User, bp


class Visit(BaseModel):
    """
    Users must be able to consult who visited their profile.
    """
    name = "visit"

    fields = {
        "id": PositiveIntegerField(primary_key=True, auto_increment=True),
        "host_user_id": ForeignKeyField(to=User, expose=False),
        "guest_user_id": ForeignKeyField(to=User),
        "visited_on": DatetimeField()
    }

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        response = cls._create(form, expose=False)
        from flaskr import socketio
        socketio.emit("NewVisit", {
            "destination_user_id": form["host_user_id"],
            "user_id": form["guest_user_id"],
            "datetime": datetime.strftime(datetime.now(), "%a, %d %b %Y %H:%M:%S GMT")
        })
        User.compute_popularity_score(form['host_user_id'])
        return response


@bp.route('/visits', methods=('GET',))
@login_required
def get_visits():
    visits = Visit.get('host_user_id', session['user_id']).fetchall()
    return Visit.bulk_expose(visits, 200)