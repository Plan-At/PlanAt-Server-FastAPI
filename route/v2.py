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

# External library
from captcha.image import ImageCaptcha

# Local file
from constant import AuthConfig
from util import random_content, json_body
import util.mongodb_data_api as DocumentDB

router = APIRouter()


@router.get("", tags=["V2"])
async def v2_endpoint():
    return JSONResponse(status_code=200, content={"status": "implementing"})


@router.post("/user/create", tags=["V2"])
async def v2_create_user():
    pass


@router.get("/user/profile")
async def v2_get_user_profile():
    pass


@router.post("/user/profile/name/display_name", tags=["V2"])
async def v2_update_user_profile_name_displayname():
    pass


@router.post("/user/profile/about/description", tags=["V2"])
async def v2_update_user_profile_about_description():
    pass


@router.post("/user/profile/status", tags=["V2"])
async def v2_update_user_profile_status():
    pass


@router.post("/user/profile/picture", tags=["V2"])
async def v2_update_user_profile_picture():
    pass


@router.post("/calendar/event/create", tags=["V2"])
async def v2_create_calendar_event():
    pass


@router.post("/calendar/event/edit", tags=["V2"])
async def v2_edit_calendar_event():
    pass


@router.get("/calendar/event/get", tags=["V2"])
async def v2_get_calendar_event():
    pass


@router.post("/auth/token/generate", tags=["V2"])
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


# TODO return both image body and the captcha id
@router.get("/captcha/image", tags=["V2"])
async def v2_generate_captcha_image():
    image_content = random_content.get_int(4)
    image_data = ImageCaptcha().generate(str(image_content))
    return StreamingResponse(content=image_data, media_type="image/png", headers={"captcha_id": str(uuid.uuid4())})


@router.get("/captcha/verify", tags=["V2"])
async def v2_verify_captcha():
    pass
