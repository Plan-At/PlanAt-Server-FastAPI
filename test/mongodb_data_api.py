import requests
import json

USER_PROFILE = {
        "person_id": "1234567890",
        "metadata": {
            "uuid": "6cb63b46-00ce-4433-a7e1-c839e94c1315",
            "seed": "56467484686",
            "registration_timestamp": "1646081914"
        },
        "name": {
            "unique_name": "abced",
            "display_name": "HelloWorld",
            "localization": [],
            "historical_name": [],
            "searchable": True
        },
        "picture": {
            "avatar": {
                "regular": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/avatar/s=64/HW",
                },
                "full": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/avatar/s=128/HW",
                }},
            "background": {
                "regular": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
                },
                "full": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
                }}},
        "status": {
            "current_status": "Developing",
            "until": {
                "text": "Extraday 13AM",
                "timestamp": "",
                "timezone_name": "Mars",
                "timezone_offset": ""
            },
            "default_status": "Alive"},
        "about": {
            "short_description": "I",
            "full_description": "I'm here"},
        "contact": {
            "email": {
                "domain": "example.com",
                "value": "example@example.com",
                "visibility": {
                    "public": True,
                    "searchable": True,
                    "organization_default": True,
                    "organization_visible": [],
                    "organization_invisible": [],
                    "friend_default": True,
                    "friend_visible": [],
                    "friend_invisible": []
                },
                "receive_contact": True},
            "phone": {
                "country_code": "",
                "bare_value": "1234567890",
                "visibility": {
                    "public": True,
                    "searchable": True,
                    "organization_default": True,
                    "organization_visible": [],
                    "organization_invisible": [],
                    "friend_default": True,
                    "friend_visible": [],
                    "friend_invisible": []
                },
                "receive_contact": True}},
        "usergroup": [],
        "public_tags": [
            {"tag_id": "123", "name": "OP"}],
        "public_friends": [
            {"person_id": "", "name": ""}],
        "public_teams": [
            {"org_id": "", "name": ""}]}

if __name__ == "__main__":
    # url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/insertOne"
    # payload = json.dumps({
    #     "collection": "User",
    #     "database": "PlanAtDev",
    #     "dataSource": "Cluster1",
    #     "document": USER_PROFILE
    # })
    url = "https://data.mongodb-api.com/app/data-whsfw/endpoint/data/beta/action/findOne"
    payload = json.dumps({
        "collection": "User",
        "database": "PlanAtDev",
        "dataSource": "Cluster1",
        "filter": {"person_id": "1234567890"}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': json.load(open("app.token.json"))["mongodb"]["data_api_key"]
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
