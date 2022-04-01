# TODO change "name" to something else
def public_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
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
    for contact_method in input_json["contact"]:
        if contact_method["visibility"]["public"] is True:
            return_json["contact"].append({"type": contact_method["type"], "value": contact_method["value"]})
    return return_json

# TODO change "name" to something else
def private_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
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
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "event_id_list": input_json["event_id_list"]
    }
    return return_json

def universal_user_calendar_event(input_json: dict, person_id=""):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
        "event_id": input_json["event_id"],
        "access_control_list": input_json["access_control_list"],
        "start_time": input_json["start_time"],
        "end_time": input_json["end_time"],
        "display_name": input_json["display_name"],
        "description": input_json["description"],
        "type_list": input_json["type_list"],
        "tag_list": input_json["tag_list"]
    }
    for each_owner in input_json["access_control_list"]:
        if each_owner["canonical_name"] == "public":
            print("event is public")
            return return_json
        if each_owner["person_id"] == person_id:
            print("event person_id matched")
            return return_json
    return None
