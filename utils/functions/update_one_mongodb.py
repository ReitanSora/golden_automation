def update_one(db, collection_name, field_name, username, update_data):
    db[f'{collection_name}'].update_one(
        {f'{field_name}': username},
        {'$set': update_data},
        upsert=False
    )
