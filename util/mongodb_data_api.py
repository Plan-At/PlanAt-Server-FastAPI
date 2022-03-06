import requests
import json


TOKEN = json.load(open("app.token.json"))


def find_one(target_db: str, target_collection: str, find_filter: dict):
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/findOne"
    payload = json.dumps({
        "dataSource": "Cluster1",
        "database": target_db,
        "collection": target_collection,
        "filter": find_filter
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": TOKEN["mongodb"]["data_api_key"]
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)["document"]
