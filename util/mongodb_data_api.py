import requests
import json


TOKEN = json.load(open("app.token.json"))
DB_CLUSTER = "Cluster1"
DB_NAME = "PlanAtDev"


def find_one(target_collection: str, find_filter: dict, target_db: str=DB_NAME, requests_session=requests.Session()):
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/findOne"
    payload = json.dumps({
        "dataSource": DB_CLUSTER,
        "database": target_db,
        "collection": target_collection,
        "filter": find_filter
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": TOKEN["mongodb"]["data_api_key"],
        # "Connection": "Keep-Alive",
    }
    response = requests_session.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return json.loads(response.text)["document"]


def delete_one(target_collection: str, find_filter: dict, target_db: str=DB_NAME, requests_session=requests.Session()):
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/deleteOne"
    payload = json.dumps({
        "dataSource": DB_CLUSTER,
        "database": target_db,
        "collection": target_collection,
        "filter": find_filter
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": TOKEN["mongodb"]["data_api_key"],
        "Connection": "Keep-Alive",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def insert_one(target_collection: str, document_body: dict, target_db: str=DB_NAME, requests_session=requests.Session()):
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/insertOne"
    payload = json.dumps({
        "dataSource": DB_CLUSTER,
        "database": target_db,
        "collection": target_collection,
        "document": document_body
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": TOKEN["mongodb"]["data_api_key"],
        "Connection": "Keep-Alive",
    }
    response = requests_session.request("POST", url, headers=headers, data=payload)
    return response.json()


def replace_one(target_collection: str, find_filter: dict, document_body: dict, target_db: str=DB_NAME, requests_session=requests.Session()):
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/replaceOne"
    payload = json.dumps({
        "dataSource": DB_CLUSTER,
        "database": target_db,
        "collection": target_collection,
        "filter": find_filter,
        "replacement": document_body
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": TOKEN["mongodb"]["data_api_key"],
        "Connection": "Keep-Alive",
    }
    response = requests_session.request("POST", url, headers=headers, data=payload)
    return response.json()
