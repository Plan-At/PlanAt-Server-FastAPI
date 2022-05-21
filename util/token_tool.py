from fastapi.responses import JSONResponse
import util.mongodb_data_api as DocumentDBRelay
import util.pymongo_wrapper as DocumentDB
from pymongo.database import Database
from constant import AuthConfig
import requests
from datetime import datetime

from util.custom_exception import TokenExpiredException


def check_token_exist_http(auth_token: str):
    if len(auth_token) != AuthConfig.TOKEN_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed token"})
    db_query = DocumentDBRelay.find_one(target_collection="TokenV1", find_filter={"token_value": auth_token})
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "token not found", "pa-token": auth_token})
    return True


def match_token_with_person_id_http(person_id: str, auth_token: str, requests_session=requests.Session()):
    """
    All the check to the token is done here
    Will validate person_id
    """
    print(auth_token)
    if auth_token == None:
        return ""
    if len(auth_token) != AuthConfig.TOKEN_LENGTH:
        return JSONResponse(status_code=403, content={"status": "malformed token"})
    db_query = DocumentDBRelay.find_one(target_collection="TokenV3", find_filter={"token_value": auth_token}, requests_session=requests_session)
    print(db_query)
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "token not found"})
    if db_query["person_id"] != person_id:
        return JSONResponse(status_code=403, content={"status": "invalid token for this person_id"})
    return True


def find_person_id_with_token_http(auth_token: str, requests_session=requests.Session()):
    """
    All the check to the token is done here
    Will validate person_id
    """
    print(auth_token)
    if auth_token == None:
        return ""
    if len(auth_token) != AuthConfig.TOKEN_LENGTH:
        return ""
    db_query = DocumentDBRelay.find_one(target_collection="TokenV1", find_filter={"token_value": auth_token}, requests_session=requests_session)
    print(db_query)
    if db_query is None:
        return ""
    else:
        return db_query["person_id"]


def get_person_id_with_token(pa_token: str, db_client: Database):
    """
    All the check to the token is done here
    Will validate person_id
    """
    print(pa_token)
    if pa_token == None:
        return ""
    if len(pa_token) != AuthConfig.TOKEN_LENGTH:
        return ""
    db_query = DocumentDB.find_one(collection="TokenV3", find_filter={"token_value": pa_token}, db_client=db_client)
    print(db_query)
    if db_query is None:
        return ""
    if db_query["expiration_timestamp_int"] <= datetime.now().timestamp():
        deletion_query = DocumentDB.delete_one(collection="TokenV3", find_filter={"token_value": pa_token}, db_client=db_client)
        print(deletion_query)
        raise TokenExpiredException(db_query["token_value"], db_query["expiration_timestamp_int"])
    return db_query["person_id"]
