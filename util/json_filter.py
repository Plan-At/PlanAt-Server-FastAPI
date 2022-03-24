def public_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "person_id": input_json["person_id"],
        "name": input_json["name"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact": [],
        "public_tag_list": input_json["public_tag_list"],
        "public_friend_list": input_json["public_friend_list"],
        "public_team_list": input_json["public_team_list"]
    }
    contact_method_list = []
    for contact_method in input_json["contact"]:
        if contact_method["visibility"]["public"] is True:
            contact_method_list.append({"type": contact_method["type"], "value": contact_method["value"]})
    return_json["contact"] = contact_method_list
    return return_json

def private_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "person_id": input_json["person_id"],
        "name": input_json["name"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact": input_json["contact"],
        "public_tag_list": input_json["public_tag_list"],
        "public_friend_list": input_json["public_friend_list"],
        "public_team_list": input_json["public_team_list"]
    }
    return return_json
    
def private_user_calendar_event_index(input_json: dict):
    print(input_json)
    return_json = {
        "person_id": input_json["person_id"],
        "event_id_list": input_json["event_id_list"]
    }
    return return_json