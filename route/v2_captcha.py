# Builtin library
import uuid

# Framework core library
from starlette.responses import StreamingResponse
from fastapi import APIRouter

# External library
from captcha.image import ImageCaptcha

# Local file
from util import random_content

router = APIRouter()


# TODO return both image body and the captcha id
@router.get("/image")
async def v2_generate_captcha_image():
    image_content = random_content.get_int(4)
    image_data = ImageCaptcha().generate(str(image_content))
    return StreamingResponse(content=image_data, media_type="image/png", headers={"captcha_id": str(uuid.uuid4())})


# TODO remove this if don't have time to work on
@router.get("/verify")
async def v2_verify_captcha():
    pass
