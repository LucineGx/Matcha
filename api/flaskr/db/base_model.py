from typing import Any, Optional, Tuple, Union

from flask import jsonify, Response

from flaskr.db.utils import get_db
from flaskr.db.fields import Field


class BaseModel:
    name = None
    fields = None

    @classmethod
    def get(cls, on_col: str, for_val: Any) -> Optional[dict]:
        db = get_db()
        query = f"SELECT * FROM {cls.name} WHERE {on_col} = ?"
        return db.execute(query, [for_val]).fetchone()

    @classmethod
    def expose(cls, on_col: str, for_val: Any, status_code: int) -> Tuple[Union[str, Response], int]:
        instance = cls.get(on_col, for_val)
        if instance is None:
            return "Resource not found", 404
        return cls._expose(instance, status_code)

    @classmethod
    def _expose(cls, instance: dict, status_code: int) -> Tuple[Union[str, Response], int]:
        return jsonify({
            name: instance[name]
            for name, field in cls.fields.items()
            if field.expose
        }), status_code

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        raise NotImplementedError

    @classmethod
    def _create(cls, form: dict, identifier_field: str) -> Tuple[Union[str, Response], int]:
        db = get_db()
        try:
            cls.validate_form(form)
        except AssertionError as e:
            return str(e), 400
        field_names = tuple(form.keys())
        values = cls.format_values(form)
        query = f"INSERT INTO {cls.name} {field_names} VALUES ({', '.join(['?'] * len(field_names))})"
        db.execute(query, values)
        db.commit()
        return cls.expose(identifier_field, form[identifier_field], 201)

    @classmethod
    def validate_form(cls, form: dict, check_required: bool = True) -> None:
        for name, value in form.items():
            cls.fields[name].validate(name, value)
        if check_required:
            for name, field in cls.fields.items():
                if field.required:
                    assert name in form, f"Field {name} is mandatory"

    @classmethod
    def format_values(cls, instance: dict) -> Tuple[Any, ...]:
        return tuple(
            cls.fields[name].db_format(value)
            for name, value in instance.items()
        )

    @classmethod
    def safe_update(cls, form: dict, on_col: str, for_val: Any) -> Tuple[Union[str, Response], int]:
        db = get_db()
        if cls.get(on_col, for_val) is None:
            return "Resource not found", 404
        set_statement = ", ".join([f"{column} = ?" for column in form.keys()])
        where_statement = f"{on_col} = ?"
        try:
            cls.validate_form(form)
        except AssertionError as e:
            return str(e), 400
        values = list(cls.format_values(form)) + [for_val]
        query = f"UPDATE {cls.name} SET {set_statement} WHERE {where_statement}"
        db.execute(query, values)
        db.commit()
        return cls.expose(on_col, for_val, 201)

    @classmethod
    def update(cls, form: dict, conditions: dict) -> None:
        db = get_db()
        set_statement = ", ".join([f"{column} = ?" for column in form.keys()])
        where_statement = " AND ".join([f"{column} = ?" for column in conditions.keys()])
        values = list(form.values()) + list(conditions.values())
        query = f"UPDATE {cls.name} SET {set_statement} WHERE {where_statement}"
        db.execute(query, values)
        db.commit()

    @classmethod
    def delete(cls, on_col: str, for_val: Any) -> None:
        db = get_db()
        query = f"DELETE FROM {cls.name} WHERE {on_col} = ?"
        db.execute(query, [for_val])
        db.commit()

    @classmethod
    def create_table(cls):
        db = get_db()
        main_query = f"CREATE TABLE IF NOT EXISTS {cls.name}"
        fields_query = ", ".join([
            cls.get_field_creation_query(field, name)
            for name, field in cls.fields.items()
        ])
        query = main_query + " ( " + fields_query + " );"
        db.execute(query)
        db.commit()

    @classmethod
    def drop_table(cls):
        db = get_db()
        db.execute(f"DROP TABLE IF EXISTS {cls.name}")
        db.commit()

    @staticmethod
    def get_field_creation_query(field: Field, name: str) -> str:
        query = [name, field.type_name]
        if field.primary_key:
            query += ["PRIMARY KEY"]
            if field.auto_increment:
                query += ["AUTOINCREMENT"]
        if field.unique:
            query += ["UNIQUE"]
        if field.null is False:
            query += ["NOT NULL"]
        if field.default is not None:
            query += [f"DEFAULT {field.default}"]
        return " ".join(query)
