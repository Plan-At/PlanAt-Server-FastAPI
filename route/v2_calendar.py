# Builtin library
from typing import Optional, List

# Framework core library
from starlette.requests import Request
from fastapi import APIRouter, Header, Query
from fastapi.responses import JSONResponse

# Local file
from util import random_content, json_body
from util.token_tool import get_person_id_with_token
import util.pymongo_wrapper as DocumentDB
import util.json_filter as JSONFilter
from constant import DBName

router = APIRouter()


@router.post("/event/create")
async def v2_create_calendar_event(request: Request, req_body: json_body.CalendarEvent, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    print(dict(req_body))
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "no user found for this token", "pa_token": pa_token})
    """add the event detail"""
    new_event_id = random_content.generate_event_id()
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
        return JSONResponse(status_code=400, content={"status": "person_id or canonical_name in access_control_list is required"})
    print(new_event_entry)
    insert_query = DocumentDB.insert_one(collection=DBName.CALENDAR_EVENT,
                                         document_body=new_event_entry,
                                         db_client=db_client)
    print(insert_query.inserted_id)
    """add record to the index"""
    index_update_query = DocumentDB.update_one(
        collection=DBName.CALENDAR_EVENT_INDEX,
        find_filter={"person_id": person_id},
        changes={"$push": {"event_id_list": new_event_id}},
        db_client=db_client)
    print(index_update_query)
    if index_update_query.matched_count != 1 and index_update_query.modified_count != 1:
        return JSONResponse(status_code=500, content={"status": "failed to insert index", "event_id": new_event_id})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success", "event_id": new_event_id})


@router.post("/event/edit")
async def v2_edit_calendar_event(request: Request,
                                 event_id: int,
                                 req_body: json_body.CalendarEvent,
                                 pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    print(dict(req_body))
    # Check user input
    if len(str(event_id)) != 16:
        return JSONResponse(status_code=400, content={"status": "malformed event_id"})
    # Get person_id from token
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    # Check is have sufficient permission to modify the event
    find_query = DocumentDB.find_one(collection=DBName.CALENDAR_EVENT,
                                     find_filter={"event_id": event_id},
                                     db_client=db_client)
    print(find_query)
    if find_query is None:
        return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
    # The event_id in DB is int
    processed_find_query = JSONFilter.universal_calendar_event(input_json=find_query,
                                                               person_id=person_id,
                                                               required_permission_list=["edit_full"])
    if not processed_find_query:
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
        if (each_access_control.canonical_name is not None) or (each_access_control.person_id is not None):
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
    insert_query = DocumentDB.replace_one(collection=DBName.CALENDAR_EVENT,
                                          find_filter={"event_id": event_id},
                                          document_body=updated_event_entry,
                                          db_client=db_client)
    print(insert_query)
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success", "event_id": event_id})


@router.post("/event/delete")
async def v2_delete_calendar_event(request: Request, event_id: int, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    if len(str(event_id)) != 16:
        return JSONResponse(status_code=400, content={"status": "malformed event_id"})
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    find_query = DocumentDB.find_one(collection="CalendarEventEntry", find_filter={"event_id": event_id}, db_client=db_client)
    if find_query is None:
        mongo_client.close()
        return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
    processed_find_query = JSONFilter.universal_calendar_event(input_json=find_query,
                                                               person_id=person_id,
                                                               required_permission_list=["delete"])
    if not processed_find_query:
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": f"unable to delete calendar_event {event_id} with current token"})
    deletion_query = DocumentDB.delete_one(collection=DBName.CALENDAR_EVENT,
                                           find_filter={"event_id": event_id},
                                           db_client=db_client)
    print(deletion_query)
    if deletion_query.deleted_count == 0:
        return JSONResponse(status_code=404,
                            content={"status": "calendar_event not found when trying to delete", "event_id": event_id})
    if deletion_query.deleted_count != 1:
        return JSONResponse(status_code=404,
                            content={"status": "calendar_event deleted but some error occurred", "event_id": event_id})
    """remove from the index"""
    update_query = DocumentDB.update_one(collection=DBName.CALENDAR_EVENT_INDEX,
                                         find_filter={"person_id": person_id},
                                         changes={"$pull": {"event_id_list": event_id}},
                                         db_client=db_client)
    print(update_query)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update index but calendar_event still deleted",
                                     "event_id": event_id})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "deletion success", "event_id": event_id})


@router.get("/event/get")
async def v2_get_calendar_event(request: Request,
                                event_id_list: List[int] = Query(None),
                                pa_token: Optional[str] = Header("")):
    print(event_id_list)
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "user not found"})
    result_calendar_event = []
    for event_id in event_id_list:
        try:
            if len(str(event_id)) != 16:
                result_calendar_event.append({"status": "malformed event_id", "event_id": event_id})
            else:
                find_query = DocumentDB.find_one(collection=DBName.CALENDAR_EVENT,
                                                 find_filter={"event_id": event_id},
                                                 db_client=db_client)
                if find_query is None:
                    result_calendar_event.append({"status": "calendar_event not found", "event_id": event_id})
                processed_find_query = JSONFilter.universal_calendar_event(input_json=find_query,
                                                                           person_id=person_id,
                                                                           required_permission_list=["read_full"])
                if processed_find_query:
                    result_calendar_event.append(processed_find_query)
        except (Exception, OSError, IOError) as e:
            print(e)
            result_calendar_event.append({"status": str(e), "event_id": event_id})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "finished", "result": result_calendar_event})


@router.get("/event/index")
async def v2_get_calendar_event_index(request: Request, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    db_query = DocumentDB.find_one(collection=DBName.CALENDAR_EVENT_INDEX, find_filter={"person_id": person_id}, db_client=db_client)
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "CalendarEvent index for this user not found", "person_id": person_id})
    mongo_client.close()
    return JSONFilter.universal_user_calendar_event_index(input_json=db_query)
