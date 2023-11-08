# Python
import os

# pymongo
from pymongo import MongoClient


class MongoDB:

    def __init__(self) -> None:
        username = os.getenv("")
        password = os.getenv("")
        path = "@main.v5svgs3.mongodb.net/?retryWrites=true&w=majority"
        test = os.getenv("IS_TEST_DB", None)

        atlas_url = f'mongodb+srv://{username}:{password}{path}'
        
        if test:
            self.__db_client = MongoClient(atlas_url).test
        else:
            self.__db_client = MongoClient(atlas_url).production
        
        self.users_db = self.__db_client.users


mongodb_client = MongoDB()
