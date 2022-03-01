

def create_single_instance(db, table_name: str, instance: dict, model: dict):
    fields = tuple(key for key in instance.keys() if key in model)
    values = tuple(model[key]["db_format"](value) for key, value in instance.items())
    query = f"INSERT INTO {table_name} {fields} VALUES ({', '.join(['?'] * len(fields))})"
    db.execute(query, values)
    db.commit()
