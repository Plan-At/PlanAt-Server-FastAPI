def public_user_profile_5(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "naming": input_json["naming"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact_method_list": [],
        "public_tag_list": input_json["public_tag_list"],
        "public_friend_list": input_json["public_friend_list"],
        "public_team_list": input_json["public_team_list"]
    }
    for contact_method in input_json["contact_method_list"]:
        if contact_method["visibility"]["public"] is True:
            return_json["contact_method_list"].append(contact_method)
    return return_json


def private_user_profile_5(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "naming": input_json["naming"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact_method_list": input_json["contact_method_list"],
        "public_tag_list": input_json["public_tag_list"],
        "public_friend_list": input_json["public_friend_list"],
        "public_team_list": input_json["public_team_list"]
    }
    return return_json


def public_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "naming": input_json["naming"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact_method_collection": input_json["contact_method_collection"]
    }
    return return_json


def private_user_profile(input_json: dict):
    print(input_json)
    return_json = {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "naming": input_json["naming"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact_method_collection": input_json["contact_method_collection"]
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


def universal_calendar_event(input_json: dict, required_permission_list: list, person_id: str):
    # Return False if user doesn't have sufficient permission
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
        if each_owner["canonical_name"] == "public" or each_owner["person_id"] == person_id:
            print("is the controller: ", each_owner)
            for each_permission in required_permission_list:
                if each_permission in each_owner["permission_list"]:
                    print("have permission")
                    return return_json
    return False
