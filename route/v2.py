from typing import Optional, List
import sys
import json
from datetime import datetime
import time
import hashlib
import requests

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, StreamingResponse
from fastapi import APIRouter, Header, File, Query
from fastapi.responses import JSONResponse

from captcha.image import ImageCaptcha

from util import random_content

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


@router.post("/calendar/event", tags=["V2"])
async def v2_create_calendar_event():
    pass


@router.get("/calendar/event", tags=["V2"])
async def v2_get_calendar_event():
    pass


@router.get("/captcha/image", tags=["V2"])
async def v2_generate_captcha_image():
    return StreamingResponse(ImageCaptcha().generate(str(random_content.get_int(4))), media_type="image/png")
