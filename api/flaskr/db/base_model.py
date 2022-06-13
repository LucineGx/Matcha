from typing import Any, Optional, Tuple, Union, List

from flask import jsonify, Response

from flaskr.db.utils import get_db
from flaskr.db.fields import Field, ForeignField


class BaseModel:
    name = None
    fields = None

    @classmethod
    def bulk_create(cls, columns: Tuple[str, ...], values: List[Tuple[Any, ...]]) -> None:
        """
        The values must follow the format
        [
            (val1, val2, val3),
            (val1, val2, val3),
            ...
        ]
        for columns (col1, col2, col3)
        """
        db = get_db()
        query = f"INSERT INTO {cls.name} {columns} VALUES {', '.join([str(row) for row in values])};"
        db.execute(query)
        db.commit()

    @classmethod
    def bulk_expose(cls, instances: list, status_code: int) -> Tuple[Union[str, Response], int]:
        return jsonify(
            [
                {
                    name: instance[name]
                    for name, field in cls.fields.items()
                    if field.expose
                }
                for instance in instances
            ]
        ), status_code

    @classmethod
    def bulk_get(cls, on_cols: List[str], for_vals: List[Any]):
        db = get_db()
        where = [f"{col} = ?" for col in on_cols]
        query = f"SELECT * FROM {cls.name} WHERE {' AND '.join(where)}"
        return db.execute(query, for_vals).fetchall()
    
    #@classmethod
    #def cascade_delete(cls, object_id: int) -> None:
    #    from flaskr.models import models
    #    for model in models:
    #        for field in 

    @classmethod
    def create(cls, form: dict) -> Tuple[Union[str, Response], int]:
        raise NotImplementedError

    @classmethod
    def _create(cls, form: dict, identifier_field: str = "", expose: bool = True) -> Tuple[Union[str, Response], int]:
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
        if expose:
            return cls.expose(identifier_field, form[identifier_field], 201)
        else:
            return f"{cls.name} created with success", 201

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
    def delete(cls, on_col: Union[str, List[str]], for_val: Any) -> None:
        db = get_db()
        if isinstance(on_col, str):
            query = f"DELETE FROM {cls.name} WHERE {on_col} = ?"
            db.execute(query, [for_val])
        elif isinstance(on_col, list):
            where = [f"{col} = ?" for col in on_col]
            query = f"DELETE FROM {cls.name} WHERE {' AND '.join(where)}"
            db.execute(query, for_val)
        db.commit()

    @classmethod
    def drop_table(cls) -> None:
        db = get_db()
        db.execute(f"DROP TABLE IF EXISTS {cls.name}")
        db.commit()

    @classmethod
    def expose(
        cls, on_col: str, for_val: Any, status_code: int, custom_fields: Optional[dict] = None
    ) -> Tuple[Union[str, Response], int]:
        instance = cls.get(on_col, for_val).fetchone()
        if instance is None:
            return "Resource not found", 404
        return cls._expose(instance, status_code, custom_fields)

    @classmethod
    def _expose(
        cls, instance: dict, status_code: int, custom_fields: Optional[dict] = None
    ) -> Tuple[Union[str, Response], int]:
        exposed_fields = {
            name: instance[name]
            for name, field in cls.fields.items()
            if field.expose
        }
        if custom_fields is not None:
            exposed_fields.update(custom_fields)
        return jsonify(exposed_fields), status_code

    @classmethod
    def fill_table(cls) -> None:
        """
        Called after table creation.
        """
        pass

    @classmethod
    def format_values(cls, instance: dict) -> Tuple[Any, ...]:
        return tuple(
            cls.fields[name].db_format(value)
            for name, value in instance.items()
        )

    @classmethod
    def get(cls, on_col: Union[str, List[str]], for_val: Any) -> Optional[dict]:
        db = get_db()
        if isinstance(on_col, str):
            if isinstance(for_val, list):
                query = f"SELECT * FROM {cls.name} WHERE {on_col} IN ({', '.join(['?' for val in for_val])})"
                return db.execute(query, for_val)
            else:
                query = f"SELECT * FROM {cls.name} WHERE {on_col} = ?"
                return db.execute(query, [for_val])
        elif isinstance(on_col, list):
            where = [
                f"{col} in ?"
                if isinstance(val, list)
                else f"{col} = ?"
                for col, val in zip(on_col, for_val)
            ]
            query = f"SELECT * FROM {cls.name} WHERE {' AND '.join(where)}"
            return db.execute(query, for_val)

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

    @classmethod
    def list(cls) -> Tuple[Union[str, Response], int]:
        instances = cls._list()
        return cls.bulk_expose(instances, 200)

    @classmethod
    def _list(cls) -> list:
        db = get_db()
        query = f"SELECT * FROM {cls.name}"
        return db.execute(query).fetchall()

    @classmethod
    def safe_update(cls, form: dict, on_col: str, for_val: Any) -> Tuple[Union[str, Response], int]:
        db = get_db()
        if cls.get(on_col, for_val) is None:
            return "Resource not found", 404
        set_statement = ", ".join([f"{column} = ?" for column in form.keys()])
        where_statement = f"{on_col} = ?"
        try:
            cls.validate_form(form, check_required=False)
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
    def validate_form(cls, form: dict, check_required: bool = True) -> None:
        for name, value in form.items():
            assert name in cls.fields, f"Unknown field {name}"
            cls.fields[name].validate(name, value)
            if cls.fields[name].unique:
                cls.validate_uniqueness(name, value)
        if check_required:
            for name, field in cls.fields.items():
                if field.required:
                    assert name in form, f"Field {name} is mandatory"
    
    @classmethod
    def validate_uniqueness(cls, on_col: str, for_val: Any) -> None:
        duplicate = cls.get(on_col, for_val).fetchone()
        assert duplicate is None, f"{on_col} {for_val} already in used"
