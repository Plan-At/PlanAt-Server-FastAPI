import json
from typing import List

from pymongo.database import Database
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


def insert_one(db_client: Database, collection: str, document_body: dict):
    # TODO figure out what will be return if operation not successful
    return db_client[collection].insert_one(document=document_body)


def insert_many(db_client: Database, collection: str, document_body: List[dict]):
    # TODO figure out what will be return if operation not successful
    return db_client[collection].insert_many(documents=document_body)


def replace_one(db_client: Database, collection: str, find_filter: dict, document_body: dict):
    return db_client[collection].replace_one(filter=find_filter, replacement=document_body)


def update_one(db_client: Database, collection: str, find_filter: dict, changes: dict):
    return db_client[collection].update_one(filter=find_filter, update=changes)


if __name__ == "__main__":
    client = MongoClient(TOKEN["mongodb"]["driver_url"])
    db = client.get_database("PlanAtDev")
    # print(db, type(db))
    # print(db["User"], type(db["User"]))
    # print(delete_one(db, "User", {"person_id": "1234567890_5"}))
    # print(find_many(db, "TokenV3", {"person_id": "1234567890"}))
    # print(delete_one(db, "TokenV3", {"token_value": ""}).deleted_count)
    # print(delete_many(db, "TokenV3", {"person_id": "1234567890"}).deleted_count)
    # print(insert_one(db, "TokenV3", {"a": "b"}).inserted_id)
    # print(insert_many(db, "TokenV3", [{}, {}]).inserted_ids)
    # _replace_one = replace_one(db, "TokenV3", {"a": "b"}, {"a": "x"})
    # print(_replace_one.matched_count, _replace_one.modified_count)
    # _update_one = update_one(db, "CalendarEventIndex", {"person_id": "1"}, {"$push": {"event_id_list": 114514}})
    # print(_update_one.matched_count, _update_one.modified_count)
    _update_one = update_one(db, "CalendarEventIndex", {"person_id": "1"}, {"$pull": {"event_id_list": 114514}})
    print(_update_one.matched_count, _update_one.modified_count)
