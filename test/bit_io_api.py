import json
import requests

if __name__ == "__main__":
    TOKEN = json.load(open("app.token.json"))

    url = "https://api.bit.io/api/v1beta/query/"

    query_string = f"""SELECT * FROM "{TOKEN['bit_io']['user_name']}/{TOKEN['bit_io']['repo_name']}"."atl_home_sales" """
    print(query_string)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN['bit_io']['api_key']}"
    }
    ret = requests.post(url=url, data=json.dumps({"query_string": query_string}), headers=headers)
    print(ret.status_code)
    print(ret.text)
    print(type(ret.json()))
    print(ret.json())
