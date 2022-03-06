import requests
import json
from constant import DummyData

if __name__ == "__main__":
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/insertOne"
    payload = json.dumps({
        "collection": "User",
        "database": "PlanAtDev",
        "dataSource": "Cluster1",
        "document": DummyData.USER_PROFILE
    })
    # url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/findOne"
    # payload = json.dumps({
    #     "collection": "User",
    #     "database": "PlanAtDev",
    #     "dataSource": "Cluster1",
    #     "filter": {"person_id": "1234567890"}
    # })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': json.load(open("app.token.json"))["mongodb"]["data_api_key"]
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
