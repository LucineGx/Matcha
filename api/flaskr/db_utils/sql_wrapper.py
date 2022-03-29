from typing import Any, Dict

from flaskr.fields import Field
from flaskr.db import get_db


def format_values(model: Dict[str, Field], fields: dict) -> list:
    return [
        field.db_format(fields.get(name, None))
        for name, field in model.items()
    ]


def create_single_instance(model: Dict[str, Field], table_name: str, instance: dict, db) -> None:
    model_fields = {name: field for name, field in model.items() if field.create}
    fields = tuple(model_fields.keys())
    values = tuple(format_values(model_fields, instance))
    query = f"INSERT INTO {table_name} {fields} VALUES ({', '.join(['?'] * len(fields))})"
    db.execute(query, values)
    db.commit()


def get_single_instance(table_name: str, on_col: str, for_val: Any) -> dict:
    db = get_db()
    query = f"SELECT * FROM {table_name} WHERE {on_col} = ?"
    return db.execute(query, [for_val]).fetchone()


def update_instance(model: Dict[str, Field], table_name: str, update: dict, conditions: dict, should_format_values: bool = True) -> None:
    db = get_db()
    set_statement = ", ".join([f"{column} = ?" for column in update.keys()])
    where_statement = format_conditions(conditions)
    if should_format_values:
        values = format_values(model, update)
    else:
        values = list(update.values())
    all_values = values + list(conditions.values())
    query = f"UPDATE {table_name} SET {set_statement} WHERE {where_statement}"
    db.execute(query, all_values)
    db.commit()


def delete_instance(table_name: str, conditions: dict) -> None:
    db = get_db()
    where_statement = format_conditions(conditions)
    query = f"DELETE FROM {table_name} WHERE {where_statement}"
    db.execute(query, list(conditions.values()))
    db.commit()


def format_conditions(conditions: dict) -> str:
    return " AND ".join([f"{column} = ?" for column in conditions.keys()])


