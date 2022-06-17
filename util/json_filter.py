def universal_user_profile(input_json: dict):
    """
    To remove the ObjectID and metadate
    """
    print(input_json)
    return {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "naming": input_json["naming"],
        "picture": input_json["picture"],
        "status": input_json["status"],
        "about": input_json["about"],
        "contact_method_collection": input_json["contact_method_collection"]
    }


def universal_user_calendar_event_index(input_json: dict):
    """
    To remove the ObjectID
    """
    print(input_json)
    return {
        "structure_version": input_json["structure_version"],
        "person_id": input_json["person_id"],
        "event_id_list": input_json["event_id_list"]
    }


def universal_calendar_event(input_json: dict, required_permission_list: list, person_id: str):
    """
    Return False if user doesn't have sufficient permission
    """
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
