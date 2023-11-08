# database
from database.mongo_client import mongodb_client


def get_users_id_in_db():
    data: list = mongodb_client.users_db.find(
        {},
        {
            "id": 1,
            "_id": 0
        }
    )

    if len(data) == 0:
        return []

    return [str(item["id"]) for item in data]


def get_usernames_in_db():
    data: list = mongodb_client.users_db.find(
        {},
        {
            "username": 1,
            "_id": 0
        }
    )

    if len(data) == 0:
        return []

    return [str(item["username"]) for item in data]
