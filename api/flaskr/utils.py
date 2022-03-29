import functools
from typing import Optional, Dict
from flask import g, jsonify

from flaskr.fields import Field


def validate_creation_form(model: Dict[str, Field], form: dict) -> Optional[str]:
    # To do: add more constraints and checks !
    for name, field in model.items():
        if field.required is True:
            if name not in form or form[name] is None:
                return f"{name} is required"


def expose_model_instance(model: Dict[str, Field], instance: dict):
    return jsonify({name: instance[name] for name, field in model.items() if field.get}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return "Unauthorized", 401

        return view(**kwargs)

    return wrapped_view
