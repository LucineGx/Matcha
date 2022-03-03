

def create_single_instance(db, table_name: str, instance: dict, model: dict) -> None:
    fields = tuple(instance.keys())
    values = tuple(model[key]["db_format"](value) for key, value in instance.items())
    query = f"INSERT INTO {table_name} {fields} VALUES ({', '.join(['?'] * len(fields))})"
    db.execute(query, values)
    db.commit()


def update_instances(db, table_name: str, update: dict, conditions: dict) -> None:
    set_statement = ", ".join([f"{column} = ?" for column in update.keys()])
    where_statement = " AND ".join([f"{column} = ?" for column in conditions.keys()])
    all_values = list(update.values()) + list(conditions.values())
    query = f"UPDATE {table_name} SET {set_statement} WHERE {where_statement}"
    db.execute(query, all_values)
    db.commit()
