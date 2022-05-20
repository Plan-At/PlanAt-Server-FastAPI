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


@router.post("/create", tags=["V2"])
async def v2_create_user():
    pass


@router.get("/profile")
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
