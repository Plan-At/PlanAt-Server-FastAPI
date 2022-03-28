import sys
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import RedirectResponse
import hashlib
from constant import DummyData, ServerConfig, AuthConfig, RateLimitConfig, MediaAssets, ContentLimit
import util.mongodb_data_api as DocumentDB
import util.bit_io_api as RelationalDB
import util.json_filter as JSONFilter
from util.validate_token import match_token_with_person_id, check_token_exist
from util import json_body, random_content
from typing import Optional, List

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger = open(file="fast_demo.log", mode="a", encoding="utf-8")
    logger.write(f"time={str(datetime.now())} ip={request.client.host} method={request.method} path=\"{request.url.path}\" ")
    response = await call_next(request)
    logger.write(f"completed_in={(datetime.now() - start_time).microseconds / 1000}ms status_code={response.status_code}\n")
    return response


@app.get("/")
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def hello_world(request: Request):
    return JSONResponse(status_code=200, content={"message": "hello, documentation available at /docs"})


@app.get("/favicon.ico")
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def get_favicon(request: Request):
    return RedirectResponse(url=MediaAssets.FAVICON)


@app.get("/ip", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def request_ip(request: Request):
    return JSONResponse(status_code=200, content={"ip": get_remote_address(request=request)})


@app.get("/header", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def request_header(request: Request):
    return JSONResponse(status_code=200, content=dict(request.headers))


@app.get("/version", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def api_version(request: Request):
    return JSONResponse(status_code=200, content={"version": ServerConfig.CURRENT_VERSION})


@app.get("/status", tags=["General Methods"])
@limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
def api_status(request: Request):
    return JSONResponse(status_code=501, content={"status": "not implemented"})


@app.get("/server/list", tags=["General Methods"])
@limiter.limit(RateLimitConfig.HIGH_SENSITIVITY)
def api_server_list(request: Request):
    return JSONResponse(status_code=200, content={"server_list": ServerConfig.API_SERVER_LIST})


@app.get("/server/assignment", tags=["General Methods"])
@limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
def api_server_assignment(request: Request):
    return JSONResponse(status_code=200, content={"recommended_servers": [{"priority": 0, "load": 0, "name": "", "URL": "", "provider": "", "location": ""}]})


class DummyMethod:
    @app.get("/dummy", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.NO_COMPUTE)
    def dummy(request: Request):
        return {"status": "ok"}


    @app.get("/dummy/user/profile", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def dummy_user_profile(request: Request):
        return DummyData.USER_PROFILE


    @app.get("/dummy/user/calendar", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.SOME_DB)
    def dummy_user_calendar(request: Request):
        return DummyData.USER_CALENDAR


    @app.get("/dummy/auth/decrypt", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.LESS_COMPUTE)
    def dummy_auth_decrypt(request: Request, encrypted_sha512_string: str, auth_token: str, timestamp: str):
        if len(auth_token) == AuthConfig.TOKEN_LENGTH:
            if hashlib.sha512((auth_token + timestamp).encode("utf-8")).hexdigest() == encrypted_sha512_string:
                return {"auth_status": "ok"}
            else:
                return {"auth_status": "failed", "error": "auth_token not match"}
        else:
            return {"auth_status": "failed", "error": "invalid auth_token format"}


class V1:
    @app.get("/v1", tags=["V1"])
    @limiter.limit(RateLimitConfig.NO_COMPUTE)
    def v1(request: Request):
        return JSONResponse(status_code=200, content={"status": "ok"})


    @app.get("/v1/auth/token/validate", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_auth_token_validate(request: Request, auth_token: str):
        validate_token_result = check_token_exist(auth_token=auth_token)
        if validate_token_result != True: 
            return validate_token_result
        else:
            return JSONResponse(status_code=200, content={"status": "valid"})

    @app.get("/v1/public/stats", tags=["V1"])
    @limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
    def v1_public_stats(request: Request):
        return JSONResponse(status_code=501, content={"status": "not implemented"})


    @app.get("/v1/restricted/stats", tags=["V1"])
    @limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
    def v1_restricted_stats(request: Request):
        return JSONResponse(status_code=501, content={"status": "not implemented"})


    @app.get("/v1/public/user/profile", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_public_user_profile(request: Request, person_id: str):
        if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
            return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
        db_query = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
        if db_query is None: 
            return JSONResponse(status_code=403, content={"status": "user not found"})
        return JSONFilter.public_user_profile(input_json=db_query)


    @app.get("/v1/private/user/profile", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_private_user_profile(request: Request, person_id: str, token: str=Header(None)):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
            return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
        db_query = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
        if db_query is None: 
            return JSONResponse(status_code=403, content={"status": "user not found"})
        return JSONFilter.private_user_profile(input_json=db_query)

    
    @app.post("/v1/update/user/profile", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_update_user_profile(request: Request, person_id: str, token: str=Header(None)):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
            return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
        return JSONResponse(status_code=501, content={"status": "not implemented"})


    @app.post("/v1/update/user/profile/name/display_name", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_update_user_profile_name_displayName(request: Request, person_id: str, token: str=Header(None), request_body: json_body.UpdateUserProfileName_DisplayName=None):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        if len(request_body.display_name) > ContentLimit.DISPLAY_NAME_LENGTH: 
            return JSONResponse(status_code=400, content={"status": "new display_name too long"})
        old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
        if old_profile is None: 
            return JSONResponse(status_code=404, content={"status": "user not found"})
        del old_profile["_id"]
        old_profile["name"]["display_name"] = request_body.display_name
        update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id}, document_body=old_profile)
        print(update_query)
        if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
            return JSONResponse(status_code=200, content={"status": "success"})
        return JSONResponse(status_code=500, content={"status": "failed"})


    @app.post("/v1/update/user/profile/about/description", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_update_user_profile_about_description(request: Request, person_id: str, token: str=Header(None), request_body: json_body.UpdateUserProfileAbout_Description=None):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
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
        update_query = DocumentDB.replace_one( target_collection="User", find_filter={"person_id": person_id}, document_body=old_profile)
        print(update_query)
        if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
            return JSONResponse(status_code=200, content={"status": "success"})
        return JSONResponse(status_code=500, content={"status": "failed"})


    
    @app.post("/v1/update/user/profile/status", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_update_user_profile_status(request: Request, person_id: str, token: str=Header(None), request_body: json_body.UpdateUserProfileStatus=None):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        if len(request_body.current_status) > ContentLimit.USER_STATUS: 
            return JSONResponse(status_code=400, content={"status": "new current_status too long"})
        old_profile = DocumentDB.find_one(target_collection="User", find_filter={"person_id": person_id})
        if old_profile is None: 
            return JSONResponse(status_code=404, content={"status": "user not found"})
        del old_profile["_id"]
        old_profile["status"]["current_status"] = request_body.current_status
        update_query = DocumentDB.replace_one(target_collection="User", find_filter={"person_id": person_id}, document_body=old_profile)
        print(update_query)
        if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
            return JSONResponse(status_code=200, content={"status": "success"})
        return JSONResponse(status_code=500, content={"status": "failed"})


    @app.get("/v1/public/search/user", tags=["V1"])
    @limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
    def v1_public_search_user(request: Request):
        return JSONResponse(status_code=501, content={"status": "not implemented"})


    @app.get("/v1/public/search/team", tags=["V1"])
    @limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
    def v1_public_search_team(request: Request):
        return JSONResponse(status_code=501, content={"status": "not implemented"})

    
    @app.get("/v1/private/user/calendar/event/index", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_private_user_calendar_event_index(request: Request, person_id: str, token: str = Header(None)):
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
            return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
        db_query = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id})
        if db_query is None: 
            return JSONResponse(status_code=403, content={"status": "user not found"})
        return JSONFilter.private_user_calendar_event_index(input_json=db_query)

    
    # TODO more efficient way to filter out
    @app.get("/v1/public/user/calendar/event/index", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
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
            find_query = DocumentDB.find_one(target_collection="CalendarEventEntry", find_filter={"event_id": each_event_id})
            if find_query != None:
                if find_query["visibility"] == "public":
                    filtered_result["event_id_list"].append(each_event_id)
        return JSONResponse(status_code=200, content=filtered_result)

    
    # TODO check is the event_id already being used
    @app.post("/v1/add/user/calendar/event", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_add_user_calendar_event(request: Request, person_id: str, token: str=Header(None), req_body: json_body.AddUserCalendarEvent=None):
        print(dict(req_body))
        validate_token_result = match_token_with_person_id(person_id=person_id, auth_token=token)
        if validate_token_result != True: 
            return validate_token_result
        """add the event detail"""
        new_event_id = int(str(int(datetime.now().timestamp())) + str(random_content.get_int(length=6)))
        new_event_entry = {
            "structure_version": 2,
            "event_id": new_event_id,
            "owner_list": [],
            "visibility": req_body.visibility,
            "start_time": {
                "text": req_body.start_time.text,
                "timestamp": req_body.start_time.timestamp,
                "timezone_name": req_body.start_time.timezone_name,
                "timezone_offset": req_body.start_time.timezone_offset
            },
            "end_time": {
                "text": req_body.end_time.text,
                "timestamp": req_body.end_time.timestamp,
                "timezone_name": req_body.end_time.timezone_name,
                "timezone_offset": req_body.end_time.timezone_offset
            },
            "display_name": req_body.display_name,
            "description": req_body.description,
            "type_list": [],
            "tag_list": []
        }
        for each_type in req_body.type_list:
            new_event_entry["type_list"].append({"type_id": each_type.type_id, "name": each_type.name})
        for each_tag in req_body.tag_list:
            new_event_entry["tag_list"].append({"tag_id": each_tag.tag_id, "name": each_tag.name})
        for each_owner in req_body.owner_list:
            print(each_owner)
            if each_owner.person_id != None:
                new_event_entry["owner_list"].append({"person_id": each_owner.person_id})
            else:
                return JSONResponse(status_code=400, content={"status": "person_id in owner_list is required"})
        print(new_event_entry)
        insert_query = DocumentDB.insert_one(target_collection="CalendarEventEntry", document_body=new_event_entry)
        print(insert_query)
        """add record to the index"""
        event_id_index = DocumentDB.find_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id})
        if event_id_index is None: 
            return JSONResponse(status_code=404, content={"status": "user calander_event_index not found"})
        del event_id_index["_id"] # If not remove _id when replace will get error
        event_id_index["event_id_list"].append(new_event_id)
        update_query = DocumentDB.replace_one(target_collection="CalendarEventIndex", find_filter={"person_id": person_id}, document_body=event_id_index)
        print(update_query)
        if update_query["matchedCount"] == 1 and update_query["modifiedCount"] == 1:
            pass
        else:
            return JSONResponse(status_code=500, content={"status": "failed to insert index"})
        return JSONResponse(status_code=200, content={"status": "success", "event_id": new_event_id})


    @app.get("/v1/universal/user/calendar/event", tags=["V1"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def v1_add_user_calendar_event(request: Request, header_token: Optional[str]=Header(None), event_id: int = 1234567890123456):
        if len(str(event_id)) != 16:
            return JSONResponse(status_code=400, content={"status": "malformed event_id"})
        find_query = DocumentDB.find_one(target_collection="CalendarEventEntry", find_filter={"event_id": event_id})
        if find_query == None:
            return JSONResponse(status_code=404, content={"status": "calendar_event not found"})
        processed_find_query = JSONFilter.universal_user_calendar_event(input_json=find_query, person_id="1234567890")
        return JSONResponse(status_code=200, content=find_query)


if __name__ == "__main__":
    if sys.platform == "win32":
        uvicorn.run("server:app", debug=True, reload=True, port=ServerConfig.PORT, host=ServerConfig.HOST, limit_concurrency=ServerConfig.CONCURRENCY)
    else:
        uvicorn.run("server:app", debug=True, reload=False, port=ServerConfig.PORT, host=ServerConfig.HOST, limit_concurrency=ServerConfig.CONCURRENCY)
