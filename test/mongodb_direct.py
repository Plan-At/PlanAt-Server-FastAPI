import pymongo
import json

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import MongoClient

TOKEN = json.load(open("app.token.json"))


def find_one(db_client: Database, collection: str, find_filter: dict):
    return db_client[collection].find_one(filter=find_filter)


def find_many(db_client: Database, collection: str, find_filter: dict):
    return [each for each in db_client[collection].find(filter=find_filter)]


def delete_one(db_client: Database, collection: str, find_filter: dict):
    return db_client[collection].delete_one(filter=find_filter)


def delete_many(db_client: Database, collection: str, find_filter: dict):
    return db_client[collection].delete_many(filter=find_filter)


if __name__ == "__main__":
    client = MongoClient(TOKEN["mongodb"]["driver_url"])
    db = client.get_database("PlanAtDev")
    print(db, type(db))
    print(db["User"], type(db["User"]))
    print(delete_one(db, "User", {"person_id": "1234567890_5"}))
    print(find_many(db, "TokenV3", {"person_id": "1234567890"}))
    print(delete_one(db, "TokenV3", {"token_value": ""}).deleted_count)
    print(delete_many(db, "TokenV3", {"person_id": "1234567890"}).deleted_count)
