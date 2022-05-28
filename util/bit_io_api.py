import json
import requests

DB_USER_NAME: str = json.load(open("app.token.json"))['bit_io']['user_name']
DB_API_KEY: str = json.load(open("app.token.json"))['bit_io']['api_key']
API_ENDPOINT = "https://api.bit.io/api/v1beta/query/"


def execute(query_string: str):
    print(query_string)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DB_API_KEY}"
    }
    ret = requests.post(url=API_ENDPOINT, data=json.dumps({"query_string": query_string}), headers=headers)
    return ret.json()


def from_table(db_repo_name: str, table_name: str):
    return f"""FROM "{DB_USER_NAME}/{db_repo_name}"."{table_name}" """
