# database
from database.mongo_client import mongodb_client


def get_usernames_in_db():
    usernames: list = mongodb_client.users_db.find(
        {},
        {
            "username": 1,
            "_id": 0
        }
    )

    if len(usernames) == 0:
        return []

    return [str(username) for username in usernames]