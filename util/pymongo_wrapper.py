from typing import List
import json

from pymongo import MongoClient
from pymongo.database import Database

TOKEN = json.load(open("app.token.json"))


def get_client():
    return MongoClient(TOKEN["mongodb"]["driver_url"]).get_database("PlanAtDev")


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
