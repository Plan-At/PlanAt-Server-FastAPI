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
import util.pymongo_wrapper as DocumentDB

router = APIRouter()


@router.post("/create", tags=["V2"])
async def v2_create_user(request: Request, user_profile: json_body.UserProfileObject, password: str = Header(None)):
    person_id = random_content.get_int(length=10)
    return JSONResponse(status_code=200, content={"status": "created",
                                                  "person_id": person_id,
                                                  "password": password})


@router.post("/delete", tags=["V2"])
async def v2_delete_user(request: Request, name_and_password: json_body.UnsafeLoginBody):
    mongoSession = DocumentDB.get_client()
    credential_verify_query = DocumentDB.find_one(collection="LoginV1",
                                                  find_filter={"person_id": name_and_password.person_id},
                                                  db_client=mongoSession)
    print(credential_verify_query)
    # the hash string generated using hashlib is lowercase
    if hashlib.sha512(name_and_password.password.encode("utf-8")).hexdigest() != credential_verify_query["password_hash"]:
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": name_and_password.person_id,
                                     "password": name_and_password.password})


@router.get("/profile", tags=["V2"])
async def v2_get_user_profile():
    pass


@router.post("/profile/name/display_name", tags=["V2"])
async def v2_update_user_profile_name_displayname():
    pass


@router.post("/profile/about/description", tags=["V2"])
async def v2_update_user_profile_about_description():
    pass


@router.post("/profile/status", tags=["V2"])
async def v2_update_user_profile_status():
    pass


@router.post("/profile/picture", tags=["V2"])
async def v2_update_user_profile_picture():
    pass
