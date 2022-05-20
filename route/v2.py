# Builtin library
from typing import Optional, List
import sys
import json
from datetime import datetime
import time
import hashlib
import requests
import uuid

# Framework core library
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, StreamingResponse
from fastapi import APIRouter, Header, File, Query
from fastapi.responses import JSONResponse

# Local file
from util import random_content, json_body
from util.token_tool import get_person_id_with_token
import util.mongodb_data_api as DocumentDB

router = APIRouter()


@router.get("", tags=["V2"])
async def v2_endpoint():
    return JSONResponse(status_code=200, content={"status": "implementing"})


@router.post("/calendar/event/create", tags=["V2"])
async def v2_create_calendar_event(request: Request, req_body: json_body.CalendarEventObject, pa_token: str = Header(None)):
    mongoSession = requests.Session()
    print(dict(req_body))
    person_id = get_person_id_with_token(requests_session=mongoSession, pa_token=pa_token)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "no user found for this token", "pa_token": pa_token})
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
        return JSONResponse(status_code=400, content={"status": "person_id or canonical_name in access_control_list is required"})
    print(new_event_entry)
    # TODO async
    insert_query = DocumentDB.insert_one(target_collection="CalendarEventEntry", 
                                         document_body=new_event_entry,
                                         requests_session=mongoSession)
    print(insert_query)
    """add record to the index"""
    event_id_index = DocumentDB.find_one(target_collection="CalendarEventIndex", 
                                         find_filter={"person_id": person_id},
                                         requests_session=mongoSession)
    if event_id_index is None:
        return JSONResponse(status_code=404, content={"status": "user calender_event_index not found", "event_id": new_event_id})
    del event_id_index["_id"]  # If not remove _id when replace will get error
    event_id_index["event_id_list"].append(new_event_id)
    update_query = DocumentDB.replace_one(target_collection="CalendarEventIndex", 
                                          find_filter={"person_id": person_id},
                                          document_body=event_id_index, requests_session=mongoSession)
    print(update_query)
    if update_query["matchedCount"] != 1 and update_query["modifiedCount"] != 1:
        return JSONResponse(status_code=500, content={"status": "failed to insert index", "event_id": new_event_id})
    return JSONResponse(status_code=200, content={"status": "success", "event_id": new_event_id})


@router.post("/calendar/event/edit", tags=["V2"])
async def v2_edit_calendar_event():
    pass


@router.get("/calendar/event/get", tags=["V2"])
async def v2_get_calendar_event():
    pass
