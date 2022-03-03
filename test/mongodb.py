import pymongo
import json

if __name__ == "__main__":
    my_token = json.load(open("app.token.json"))
    mongodb_client = pymongo.MongoClient(my_token["mongodb"]["driver_url"])

    my_db = mongodb_client.list_database_names()
    print(my_db)
