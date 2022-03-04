from typing import Any

from flaskr.db import get_db


def format_values(model: dict, fields: dict) -> list:
    return [
        model[key]["db_format"](value)
        for key, value in fields.items()
    ]


def format_conditions(conditions: dict) -> str:
    return " AND ".join([f"{column} = ?" for column in conditions.keys()])


def create_single_instance(db, model: dict, table_name: str, instance: dict) -> None:
    fields = tuple(instance.keys())
    values = tuple(format_values(model, instance))
    query = f"INSERT INTO {table_name} {fields} VALUES ({', '.join(['?'] * len(fields))})"
    db.execute(query, values)
    db.commit()


def get_single_instance(table_name: str, on_col: str, for_val: Any) -> dict:
    db = get_db()
    query = f"SELECT * FROM {table_name} WHERE {on_col} = ?"
    return db.execute(query, [for_val]).fetchone()


def update_instance(model: dict, table_name: str, update: dict, conditions: dict) -> None:
    db = get_db()
    set_statement = ", ".join([f"{column} = ?" for column in update.keys()])
    where_statement = format_conditions(conditions)
    all_values = format_values(model, update) + list(conditions.values())
    query = f"UPDATE {table_name} SET {set_statement} WHERE {where_statement}"
    db.execute(query, all_values)
    db.commit()


def delete_instance(table_name: str, conditions: dict) -> None:
    db = get_db()
    where_statement = format_conditions(conditions)
    query = f"DELETE FROM {table_name} WHERE {where_statement}"
    db.execute(query, list(conditions.values()))
    db.commit()


