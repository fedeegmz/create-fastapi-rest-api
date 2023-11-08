# PyMongo
from pymongo import MongoClient

# security
from security.config import settings


class MongoDB:

    def __init__(self) -> None:
        username = settings.mongodb_user
        password = settings.mongodb_password
        host = settings.mongodb_host
        test = settings.is_test_db

        atlas_url = f'mongodb+srv://{username}:{password}{host}'
        
        if test:
            self.__db_client = MongoClient(atlas_url).test
        else:
            self.__db_client = MongoClient(atlas_url).production
        
        self.users_db = self.__db_client.users


mongodb_client = MongoDB()
