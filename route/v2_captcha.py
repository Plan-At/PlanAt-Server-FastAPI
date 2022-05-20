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
from util import random_content

router = APIRouter()

# TODO return both image body and the captcha id
@router.get("/image", tags=["V2"])
async def v2_generate_captcha_image():
    image_content = random_content.get_int(4)
    image_data = ImageCaptcha().generate(str(image_content))
    return StreamingResponse(content=image_data, media_type="image/png", headers={"captcha_id": str(uuid.uuid4())})


@router.get("/verify", tags=["V2"])
async def v2_verify_captcha():
    pass
