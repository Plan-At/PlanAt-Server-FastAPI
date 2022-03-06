import json

def public_user_profile(raw_json: dict):
    return_json = {
        "person_id": raw_json["person_id"]
    }
    return return_json