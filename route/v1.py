from typing import Optional, List
import sys
import json
from datetime import datetime
import time
import hashlib
import requests

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from fastapi import APIRouter, Header, File, Query
from fastapi.responses import JSONResponse

import util.mongodb_data_api as DocumentDB
import util.json_filter as JSONFilter
from util.token_tool import match_token_with_person_id, check_token_exist, find_person_id_with_token
from util import json_body, random_content, image4io
from constant import ServerConfig, AuthConfig, ContentLimit

router = APIRouter()


@router.get("/v1", tags=["V1"])
def v1(request: Request):
    return JSONResponse(status_code=200, content={"status": "deprecate-ing"})


@router.get("/v1/auth/token/validate", tags=["V1"])
def v1_auth_token_validate(request: Request, pa_token: str):
    validate_token_result = check_token_exist(auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    else:
        return JSONResponse(status_code=200, content={"status": "valid"})


@router.post("/v1/create/user", tags=["V1"])
def v1_create_user(request: Request, user_profile: json_body.UserProfileObject, password: str = Header(None)):
    person_id = random_content.get_int(length=10)
    return JSONResponse(status_code=200, content={"status": "created", "body": user_profile, "person_id": person_id,
                                                  "password": password})


@router.get("/v1/public/user/profile", tags=["V1"])
def v1_public_user_profile(request: Request, person_id: str):
    if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
    db_query = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "user not found"})
    return JSONFilter.public_user_profile(input_json=db_query)


@router.get("/v1/private/user/profile", tags=["V1"])
def v1_private_user_profile(request: Request, person_id: str, pa_token: str = Header(None)):
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
    db_query = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "user not found"})
    return JSONFilter.private_user_profile(input_json=db_query)


@router.post("/v1/update/user/profile/name/display_name", tags=["V1"])
def v1_update_user_profile_name_displayName(request: Request, person_id: str, pa_token: str = Header(None),
                                            request_body: json_body.UpdateUserProfileName_DisplayName = None):
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    if len(request_body.display_name) > ContentLimit.DISPLAY_NAME_LENGTH:
        return JSONResponse(status_code=400, content={"status": "new display_name too long"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user not found"})
    del old_profile["_id"]
    old_profile["naming"]["display_name"] = request_body.display_name
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "success"})
    return JSONResponse(status_code=500, content={"status": "failed"})


@router.post("/v1/update/user/profile/about/description", tags=["V1"])
def v1_update_user_profile_about_description(request: Request, person_id: str, pa_token: str = Header(None),
                                             request_body: json_body.UpdateUserProfileAbout_Description = None):
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    if len(request_body.short_description) > ContentLimit.SHORT_DESCRIPTION:
        return JSONResponse(status_code=400, content={"status": "new short_description too long"})
    elif len(request_body.full_description) > ContentLimit.LONG_DESCRIPTION:
        return JSONResponse(status_code=400, content={"status": "new full_description too long"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user not found"})
    del old_profile["_id"]
    old_profile["about"]["short_description"] = request_body.short_description
    old_profile["about"]["full_description"] = request_body.full_description
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "success"})
    return JSONResponse(status_code=500, content={"status": "failed"})


@router.post("/v1/update/user/profile/status", tags=["V1"])
def v1_update_user_profile_status(request: Request, person_id: str, pa_token: str = Header(None),
                                  request_body: json_body.UpdateUserProfileStatus = None):
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    if len(request_body.current_status) > ContentLimit.USER_STATUS:
        return JSONResponse(status_code=400, content={"status": "new current_status too long"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user not found"})
    del old_profile["_id"]
    old_profile["status"]["current_status"] = request_body.current_status
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "success"})
    return JSONResponse(status_code=500, content={"status": "failed"})


# All of them are copy and pasted
@router.post("/v1/update/user/profile/contact/email_primary", tags=["V1"])
def v1_update_user_profile_contact_email_primary(request: Request, full_address: str, pa_token: str = Header(None)):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id},
                                      requests_session=mongoSession)
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user profile not found", "person_id": person_id})
    del old_profile["_id"]
    old_profile["contact_method_collection"]["email_primary"]["full_address"] = full_address
    old_profile["contact_method_collection"]["email_primary"]["domain_name"] = full_address.split("@")[1]
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "success", "full_address": full_address})
    return JSONResponse(status_code=500, content={"status": "failed to update"})


@router.post("/v1/update/user/profile/contact/phone", tags=["V1"])
def v1_update_user_profile_contact_phone(request: Request, country_code: str, regular_number: str,
                                         pa_token: str = Header(None)):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id},
                                      requests_session=mongoSession)
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user profile not found", "person_id": person_id})
    del old_profile["_id"]
    old_profile["contact_method_collection"]["phone"]["country_code"] = country_code
    old_profile["contact_method_collection"]["phone"]["regular_number"] = regular_number
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "success", "country_code": country_code,
                                                      "regular_number": regular_number})
    return JSONResponse(status_code=500, content={"status": "failed to update"})


@router.post("/v1/update/user/profile/contact/physical_address", tags=["V1"])
def v1_update_user_profile_contact_physical_address(request: Request, street_address: str, city: str, province: str,
                                                    country: str, continent: str, post_code: str,
                                                    pa_token: str = Header(None)):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id},
                                      requests_session=mongoSession)
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user profile not found", "person_id": person_id})
    del old_profile["_id"]
    old_profile["contact_method_collection"]["physical_address"]["street_address"] = street_address
    old_profile["contact_method_collection"]["physical_address"]["city"] = city
    old_profile["contact_method_collection"]["physical_address"]["province"] = province
    old_profile["contact_method_collection"]["physical_address"]["country"] = country
    old_profile["contact_method_collection"]["physical_address"]["continent"] = continent
    old_profile["contact_method_collection"]["physical_address"]["post_code"] = post_code
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200,
                            content={"status": "success", "street_address": street_address, "city": city,
                                     "province": province, "country": country, "continent": continent,
                                     "post_code": post_code})
    return JSONResponse(status_code=500, content={"status": "failed to update"})


@router.post("/v1/update/user/profile/contact/twitter", tags=["V1"])
def v1_update_user_profile_contact_twitter(request: Request, user_name: str, user_handle: str, user_id: str,
                                           pa_token: str = Header(None)):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id},
                                      requests_session=mongoSession)
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user profile not found", "person_id": person_id})
    del old_profile["_id"]
    old_profile["contact_method_collection"]["twitter"]["user_name"] = user_name
    old_profile["contact_method_collection"]["twitter"]["user_handle"] = user_handle
    old_profile["contact_method_collection"]["twitter"]["user_id"] = user_id
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200,
                            content={"status": "success", "user_name": user_name, "user_handle": user_handle,
                                     "user_id": user_id})
    return JSONResponse(status_code=500, content={"status": "failed to update"})


@router.post("/v1/update/user/profile/picture", tags=["V1"])
def v1_update_user_profile_picture(request: Request, image_url: str, target: str = "avatar",
                                   pa_token: str = Header(None)):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id},
                                      requests_session=mongoSession)
    if old_profile is None:
        return JSONResponse(status_code=404, content={"status": "user profile not found", "person_id": person_id})
    del old_profile["_id"]
    if target == "avatar":
        old_profile["picture"]["avatar"]["original"]["image_url"] = image_url
    elif target == "background":
        old_profile["picture"]["background"]["original"]["image_url"] = image_url
    update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id},
                                          document_body=old_profile, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        return JSONResponse(status_code=200,
                            content={"status": "success", "target_image": target, "image_url": image_url})
    return JSONResponse(status_code=500, content={"status": "failed to update"})


@router.get("/v1/private/user/calendar/event/index", tags=["V1"])
def v1_private_user_calendar_event_index(request: Request, person_id: str, pa_token: str = Header(None)):
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token)
    if validate_token_result != True:
        return validate_token_result
    if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
    db_query = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id})
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "user not found"})
    return JSONFilter.private_user_calendar_event_index(input_json=db_query)


# TODO more efficient way to filter out
@router.get("/v1/public/user/calendar/event/index", tags=["V1"])
def v1_public_user_calendar_event_index(request: Request, person_id: str):
    if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
    db_query = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id})
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "user not found"})
    filtered_result = {
        "structure_version": db_query["structure_version"],
        "person_id": db_query["person_id"],
        "event_id_list": []
    }
    for each_event_id in db_query["event_id_list"][:ContentLimit.PUBLIC_EVENT_ID_INDEX]:
        find_query = DocumentDB.find_one(target_collection="CalendarEventEntry",
                                         find_filter={"event_id": each_event_id})
        if find_query != None:
            if find_query["visibility"] == "public":
                filtered_result["event_id_list"].append(each_event_id)
    return JSONResponse(status_code=200, content=filtered_result)


# TODO check is the event_id already being used
@router.post("/v1/add/user/calendar/event", tags=["V1"])
def v1_add_user_calendar_event(request: Request, person_id: str, pa_token: str = Header(None),
                               req_body: json_body.CalendarEventObject = None):
    mongoSession = requests.Session()
    print(dict(req_body))
    validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=pa_token,
                                                       requests_session=mongoSession)
    if validate_token_result != True:
        return validate_token_result
    """add the event detail"""
    new_event_id = int(str(int(datetime.now().timestamp())) + str(random_content.get_int(length=6)))
    if len(str(new_event_id)) != 16:
        raise Exception("random did not generator correct length of number")
    new_event_entry = {
        "structure_version": 4,
        "event_id": new_event_id,
        "access_control_list": [],
        "start_time": {
            "text": req_body.start_time.text,
            "timestamp_int": req_body.start_time.timestamp_int,
            "timezone_name": req_body.start_time.timezone_name,
            "timezone_offset": req_body.start_time.timezone_offset
        },
        "end_time": {
            "text": req_body.end_time.text,
            "timestamp_int": req_body.end_time.timestamp_int,
            "timezone_name": req_body.end_time.timezone_name,
            "timezone_offset": req_body.end_time.timezone_offset
        },
        "display_name": req_body.display_name,
        "description": req_body.description,
        "type_list": [],
        "tag_list": []
    }
    for each_type in req_body.type_list:
        new_event_entry["type_list"].append({"type_id": each_type.type_id, "display_name": each_type.display_name})
    for each_tag in req_body.tag_list:
        new_event_entry["tag_list"].append({"tag_id": each_tag.tag_id, "display_name": each_tag.display_name})
    least_one_access_control = False
    for each_access_control in req_body.access_control_list:
        print(each_access_control)
        if (each_access_control.canonical_name != None) or (each_access_control.person_id != None):
            new_event_entry["access_control_list"].append({
                "canonical_name": each_access_control.canonical_name,
                "person_id": each_access_control.person_id,
                "permission_list": each_access_control.permission_list
            })
            least_one_access_control = True
    if not least_one_access_control:
        return JSONResponse(status_code=400,
                            content={"status": "person_id or canonical_name in access_control_list is required"})
    print(new_event_entry)
    insert_query = DocumentDB.insert_one(target_collection="CalendarEventEntry", document_body=new_event_entry,
                                         requests_session=mongoSession)
    print(insert_query)
    """add record to the index"""
    event_id_index = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id},
                                         requests_session=mongoSession)
    if event_id_index is None:
        return JSONResponse(status_code=404, content={"status": "user calender_event_index not found"})
    del event_id_index["_id"]  # If not remove _id when replace will get error
    event_id_index["event_id_list"].append(new_event_id)
    update_query = DocumentDB.replace_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id},
                                          document_body=event_id_index, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
        pass
    else:
        return JSONResponse(status_code=500, content={"status": "failed to insert index"})
    return JSONResponse(status_code=200, content={"status": "success", "event_id": new_event_id})


@router.post("/v1/update/user/calendar/event", tags=["V1"])
def v1_add_user_calendar_event(request: Request, event_id: int, req_body: json_body.CalendarEventObject,
                               pa_token: str = Header(None)):
    mongoSession = requests.Session()
    print(dict(req_body))
    # Check user input
    if len(str(event_id)) != 16:
        return JSONResponse(status_code=400, content={"status": "malformed event_id"})
    # Get person_id from token
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    # Check is have sufficient permission to modify the event
    find_query = DocumentDB.find_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id},
                                     requests_session=mongoSession)
    print(find_query)
    if find_query == None:
        return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
    # The event_id in DB is int
    processed_find_query = JSONFilter.universal_user_calendar_event(input_json=find_query, person_id=person_id,
                                                                    required_permission_list=["edit_full"])
    if processed_find_query == False:
        return JSONResponse(status_code=403,
                            content={"status": "unable to modify current calendar_event with current token",
                                     "event_id": event_id})
    # Add the event detail
    # Copy and paste the create event
    updated_event_entry = {
        "structure_version": 4,
        "event_id": event_id,
        "access_control_list": [],
        "start_time": {
            "text": req_body.start_time.text,
            "timestamp_int": req_body.start_time.timestamp_int,
            "timezone_name": req_body.start_time.timezone_name,
            "timezone_offset": req_body.start_time.timezone_offset
        },
        "end_time": {
            "text": req_body.end_time.text,
            "timestamp_int": req_body.end_time.timestamp_int,
            "timezone_name": req_body.end_time.timezone_name,
            "timezone_offset": req_body.end_time.timezone_offset
        },
        "display_name": req_body.display_name,
        "description": req_body.description,
        "type_list": [],
        "tag_list": []
    }
    for each_type in req_body.type_list:
        updated_event_entry["type_list"].append({"type_id": each_type.type_id, "display_name": each_type.display_name})
    for each_tag in req_body.tag_list:
        updated_event_entry["tag_list"].append({"tag_id": each_tag.tag_id, "display_name": each_tag.display_name})
    least_one_access_control = False
    for each_access_control in req_body.access_control_list:
        print(each_access_control)
        if (each_access_control.canonical_name != None) or (each_access_control.person_id != None):
            updated_event_entry["access_control_list"].append({
                "canonical_name": each_access_control.canonical_name,
                "person_id": each_access_control.person_id,
                "permission_list": each_access_control.permission_list
            })
            least_one_access_control = True
    if not least_one_access_control:
        return JSONResponse(status_code=400,
                            content={"status": "person_id or canonical_name in access_control_list is required"})
    print(updated_event_entry)
    insert_query = DocumentDB.replace_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id},
                                          document_body=updated_event_entry, requests_session=mongoSession)
    print(insert_query)
    return JSONResponse(status_code=200, content={"status": "success", "event_id": event_id})


@router.get("/v1/universal/user/calendar/event", tags=["V1"])
def v1_universal_user_calendar_event(request: Request, event_id: int, pa_token: Optional[str] = Header("")):
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    if len(str(event_id)) != 16:
        return JSONResponse(status_code=400, content={"status": "malformed event_id"})
    find_query = DocumentDB.find_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id},
                                     requests_session=mongoSession)
    if find_query == None:
        return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
    processed_find_query = JSONFilter.universal_user_calendar_event(input_json=find_query, person_id=person_id,
                                                                    required_permission_list=["read_full"])
    if processed_find_query != False:
        return JSONResponse(status_code=200, content=processed_find_query)
    else:
        return JSONResponse(status_code=403,
                            content={"status": f"unable to access calendar_event {event_id} with current token"})


@router.get("/v1/universal/user/calendar/multipleEvent", tags=["V1"])
def v1_universal_user_calendar_event(request: Request, event_id_list: List[int] = Query(None),
                                     pa_token: Optional[str] = Header("")):
    print(event_id_list)
    mongoSession = requests.Session()
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    result_calendar_event = []
    for event_id in event_id_list:
        try:
            if len(str(event_id)) != 16:
                result_calendar_event.append({"status": "malformed event_id", "event_id": event_id})
            else:
                find_query = DocumentDB.find_one(target_collection="CalendarEventEntry",
                                                 find_filter={"event_id": event_id}, requests_session=mongoSession)
                if find_query is None:
                    result_calendar_event.append({"status": "calendar_event not found", "event_id": event_id})
                processed_find_query = JSONFilter.universal_user_calendar_event(
                    input_json=find_query,
                    person_id=person_id,
                    required_permission_list=["read_full"])
                if processed_find_query != False:
                    result_calendar_event.append(processed_find_query)
        except (Exception, OSError, IOError) as e:
            print(e)
            result_calendar_event.append({"status": str(e), "event_id": event_id})
    return JSONResponse(status_code=200, content={"status": "finished", "result": result_calendar_event})


@router.post("/v1/delete/user/calendar/event", tags=["V1"])
def v1_delete_user_calendar_event(request: Request, event_id: int, pa_token: str = Header(None)):
    mongoSession = requests.Session()
    if len(str(event_id)) != 16:
        return JSONResponse(status_code=400, content={"status": "malformed event_id"})
    person_id = find_person_id_with_token(auth_token=pa_token, requests_session=mongoSession)
    find_query = DocumentDB.find_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id})
    if find_query is None:
        return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
    processed_find_query = JSONFilter.universal_user_calendar_event(input_json=find_query, person_id=person_id,
                                                                    required_permission_list=["delete"])
    if processed_find_query == False:
        return JSONResponse(status_code=403,
                            content={"status": f"unable to delete calendar_event {event_id} with current token"})
    # else:
    #     return JSONResponse(status_code=200, content={"status": "have sufficient permission but CalendarEvent not deleted yet"})
    deletion_query = DocumentDB.delete_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id},
                                           requests_session=mongoSession)
    print(deletion_query)
    if deletion_query is None:
        return JSONResponse(status_code=404,
                            content={"status": "calendar_event not found when trying to delete", "event_id": event_id})
    if deletion_query["deletedCount"] != 1:
        return JSONResponse(status_code=404,
                            content={"status": "calendar_event deleted but some error occurred", "event_id": event_id})
    """remove from the index"""
    event_id_index = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id},
                                         requests_session=mongoSession)
    if event_id_index is None:
        return JSONResponse(status_code=404, content={"status": "user calendar_event_index not found"})
    del event_id_index["_id"]  # If not remove _id when replace will get error
    event_id_index["event_id_list"].remove(event_id)
    update_query = DocumentDB.replace_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id},
                                          document_body=event_id_index,
                                          requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] != 1 and update_query["modifiedCount"] != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update index but calendar_event still deleted",
                                     "event_id": event_id})
    return JSONResponse(status_code=200, content={"status": "deletion success", "event_id": event_id})


@router.post("/v1/registration/user", tags=["V1"])
def v1_registration_user(request: Request):
    return JSONResponse(status_code=200, content={"status": "success", "person_id": "", "token": ""})


@router.get("/v1/user/person_id", tags=["V1"])
def v1_get_user_person_id(request: Request, pa_token: str = Header(None)):
    check_result = find_person_id_with_token(auth_token=pa_token)
    if check_result is not None:
        return JSONResponse(status_code=200, content={"status": "success", "person_id": check_result})
    else:
        return JSONResponse(status_code=400, content={"status": "failed"})


@router.post("/v1/auth/unsafe/login", tags=["V1"])
def v1_auth_unsafe_login(request: Request, name_and_password: json_body.UnsafeLoginBody):
    mongoSession = requests.Session()
    credential_query = DocumentDB.find_one("LoginV1", find_filter={"person_id": name_and_password.person_id},
                                           requests_session=mongoSession)
    print(credential_query)
    # the hash string generated using hashlib is lowercase
    if (credential_query is None) or not (
            hashlib.sha512(name_and_password.password.encode("utf-8")).hexdigest() == credential_query["password_hash"]):
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match", "person_id": name_and_password.person_id,
                                     "password": name_and_password.password})
    # Checking if the same token already being use
    # There is no do-while loop in Python
    while True:
        generated_token = random_content.generator_access_token(length=AuthConfig.TOKEN_LENGTH)
        current_checking_query = DocumentDB.find_one("TokenV1", find_filter={"token_value": generated_token},
                                                     requests_session=mongoSession)
        if current_checking_query is None:
            break
    token_record_query = DocumentDB.insert_one(
        "TokenV1",
        document_body={
            "structure_version": 2,
            "person_id": name_and_password.person_id,
            "token_value": generated_token,
            "token_hash": hashlib.sha512(generated_token.encode("utf-8")).hexdigest()
        },
        requests_session=mongoSession)
    print(token_record_query)
    if (token_record_query is not None) and ("insertedId" in token_record_query):
        return JSONResponse(status_code=200, content={"status": "success", "pa_token": generated_token})
    else:
        return JSONResponse(status_code=500,
                            content={"status": "token generated but failed to insert that token to database"})


@router.post("/v1/auth/unsafe/logout", tags=["V1"])
def v1_auth_unsafe_logout(request: Request, pa_token: str = Header(None)):
    mongoSession = requests.Session()
    # Lack of extra verification
    # But just assuming the token not leaking to hecker or any bad actors
    token_deletion_query = DocumentDB.delete_one(
        "TokenV1",
        find_filter={"token_value": pa_token},
        requests_session=mongoSession)
    print(token_deletion_query)
    if token_deletion_query is None:
        return JSONResponse(status_code=500, content={"status": "failed to remove the old token to database"})
    elif token_deletion_query["deletedCount"] == 0:
        return JSONResponse(status_code=404, content={"status": "token not found", "pa_token": pa_token})
    elif token_deletion_query["deletedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "deleted", "pa_token": pa_token})


# TODO: revoke existing session/token
@router.post("/v1/auth/unsafe/password", tags=["V1"])
def v1_auth_unsafe_change_password(request: Request, old_password: json_body.UnsafeLoginBody,
                                   new_password: json_body.UnsafeLoginBody):
    mongoSession = requests.Session()
    credential_verify_query = DocumentDB.find_one("LoginV1", find_filter={"person_id": old_password.person_id},
                                                  requests_session=mongoSession)
    print(credential_verify_query)
    # verify the old password
    if (credential_verify_query is None) or not (
            hashlib.sha512(old_password.password.encode("utf-8")).hexdigest() == credential_verify_query[
        "password_hash"]):
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match", "person_id": old_password.person_id,
                                     "password": old_password.password})
    new_credential_entry = {
        "structure_version": 1,
        "person_id": old_password.person_id,
        "password_hash": hashlib.sha512(new_password.password.encode("utf-8")).hexdigest(),
        "password_length": len(new_password.password),
    }
    credential_update_query = DocumentDB.replace_one("LoginV1", find_filter={"person_id": old_password.person_id},
                                                     document_body=new_credential_entry, requests_session=mongoSession)
    print(credential_update_query)
    if credential_update_query["matchedCount"] != 1 and credential_update_query[
        "modifiedCount"] != 1:  # trying to make the break in the first place, if no error might proceed to other steps
        return JSONResponse(status_code=500, content={"status": "failed to update", "person_id": old_password.person_id,
                                                      "password": old_password.password})
    else:
        return JSONResponse(status_code=200, content={"status": "success", "voided": old_password.password})


@router.post("/v1/hosting/image", tags=["V1"])
def v1_upload_image(request: Request, image_file: bytes = File(..., max_length=ContentLimit.IMAGE_SIZE)):
    resp = image4io.uploadImage(
        authorization=image4io.calculate_basic_auth(
            api_key=json.load(open("app.token.json"))["image4io"]["api_key"],
            api_secret=json.load(open("app.token.json"))["image4io"]["api_secret"]),
        local_file_bytes=image_file,
        local_file_name=image4io.generate_file_name(local_file_bytes=image_file),
        remote_folder_path=ServerConfig.IMAGEBED_FOLDER)
    if resp.status_code != 200:
        return JSONResponse(status_code=500, content={"status": "image upload failed"})
    else:
        image_info = json.loads(resp.text)
        report_card = {
            "structure_version": 1,
            "image_url": image_info["uploadedFiles"][0]["url"],
            "image_id": "",
            "image_file_name": image_info["uploadedFiles"][0]["userGivenName"],
            "image_file_path": image_info["uploadedFiles"][0]["name"],
            "image_size": image_info["uploadedFiles"][0]["size"],
            "image_width": image_info["uploadedFiles"][0]["width"],
            "image_height": image_info["uploadedFiles"][0]["height"],
            "hosting_provider": "image4io"
        }
        db_action_result = DocumentDB.insert_one(target_collection="ImageHosting", document_body=report_card)
        print(db_action_result)
        return JSONResponse(status_code=201,
                            content={"status": "success", "image_url": image_info["uploadedFiles"][0]["url"]})
