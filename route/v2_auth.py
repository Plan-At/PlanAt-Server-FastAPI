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
from constant import AuthConfig
from util import random_content, json_body
import util.mongodb_data_api as DocumentDB

router = APIRouter()

@router.post("/token/generate", tags=["V2"])
async def v2_auth_unsafe_login(request: Request, name_and_password: json_body.UnsafeLoginBody):
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
    while True:
        # Checking if the same token already being use
        # There is no do-while loop in Python
        generated_token = random_content.generator_access_token(length=AuthConfig.TOKEN_LENGTH)
        current_checking_query = DocumentDB.find_one("TokenV1", find_filter={"token_value": generated_token},
                                                     requests_session=mongoSession)
        if current_checking_query is None:
            break
    create_at = int(datetime.now().timestamp())
    expire_at = create_at + name_and_password.lifespan
    token_record_query = DocumentDB.insert_one(
        "TokenV3",
        document_body={
            "structure_version": 3,
            "person_id": name_and_password.person_id,
            "token_value": generated_token,
            "token_hash": hashlib.sha512(generated_token.encode("utf-8")).hexdigest(),
            "creation_timestamp_int": create_at,
            "expiration_timestamp_int": expire_at
        },
        requests_session=mongoSession)
    print(token_record_query)
    if (token_record_query is not None) and ("insertedId" in token_record_query):
        return JSONResponse(status_code=200,
                            content={"status": "success", "pa_token": generated_token, "expiration_timestamp": expire_at})
    else:
        return JSONResponse(status_code=500,
                            content={"status": "token generated but failed to insert that token to database"})


@router.post("/token/revoke", tags=["V2"])
async def v2_auth_token_revoke(request: Request, pa_token: str = Header(None)):
    mongoSession = requests.Session()
    # Lack of extra verification
    # But just assuming the token not leaking to hecker or any bad actors
    token_deletion_query = DocumentDB.delete_one(
        "TokenV3",
        find_filter={"token_value": pa_token},
        requests_session=mongoSession)
    print(token_deletion_query)
    if token_deletion_query is None:
        return JSONResponse(status_code=500, content={"status": "failed to remove the old token to database", "pa_token": pa_token})
    elif token_deletion_query["deletedCount"] == 0:
        return JSONResponse(status_code=404, content={"status": "token not found", "pa_token": pa_token})
    elif token_deletion_query["deletedCount"] == 1:
        return JSONResponse(status_code=200, content={"status": "deleted", "pa_token": pa_token})


# TODO: revoke existing session/token
@router.post("/password/update", tags=["V2"])
async def v2_update_auth_password(request: Request, old_password: json_body.UnsafeLoginBody, new_password: json_body.UnsafeLoginBody):
    mongoSession = requests.Session()
    credential_verify_query = DocumentDB.find_one("LoginV1", 
                                                  find_filter={"person_id": old_password.person_id},
                                                  requests_session=mongoSession)
    print(credential_verify_query)
    # verify the old password
    if (credential_verify_query is None) or not (
            hashlib.sha512(old_password.password.encode("utf-8")).hexdigest() == credential_verify_query["password_hash"]):
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match", 
                                     "person_id": old_password.person_id,
                                     "password": old_password.password})
    new_credential_entry = {
        "structure_version": 1,
        "person_id": old_password.person_id,
        "password_hash": hashlib.sha512(new_password.password.encode("utf-8")).hexdigest(),
        "password_length": len(new_password.password),
    }
    credential_update_query = DocumentDB.replace_one("LoginV1", 
                                                     find_filter={"person_id": old_password.person_id},
                                                     document_body=new_credential_entry, requests_session=mongoSession)
    print(credential_update_query)
    if credential_update_query["matchedCount"] != 1 and credential_update_query[
        "modifiedCount"] != 1:  # trying to make the break in the first place, if no error might proceed to other steps
        return JSONResponse(status_code=500, content={"status": "failed to update", 
                                                      "person_id": old_password.person_id,
                                                      "password": old_password.password})
    else:
        return JSONResponse(status_code=200, content={"status": "success", "voided": old_password.password})
