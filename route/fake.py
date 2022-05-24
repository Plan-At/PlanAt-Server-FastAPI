import hashlib

from starlette.requests import Request
from fastapi import APIRouter
from starlette.responses import JSONResponse

from constant import AuthConfig
import example_data

router = APIRouter()


@router.get("", tags=["Fake Data"])
def dummy(request: Request):
    return JSONResponse(status_code=200, content={"status": "deprecated    data might not reflect v2"})


@router.get("/user/profile", tags=["Fake Data"])
def dummy_user_profile(request: Request):
    return example_data.USER_PROFILE_7


@router.get("/user/calendar", tags=["Fake Data"])
def dummy_user_calendar(request: Request):
    return example_data.USER_CALENDAR


@router.get("/auth/decrypt", tags=["Fake Data"])
def dummy_auth_decrypt(request: Request, encrypted_sha512_string: str, auth_token: str, timestamp: str):
    if len(auth_token) == AuthConfig.TOKEN_LENGTH:
        if hashlib.sha512((auth_token + timestamp).encode("utf-8")).hexdigest() == encrypted_sha512_string:
            return {"auth_status": "ok"}
        else:
            return {"auth_status": "failed", "error": "auth_token not match"}
    else:
        return {"auth_status": "failed", "error": "invalid auth_token format"}


@router.get("/error/internal", tags=["Fake Data"])
async def fake_internal_error(request: Request):
    raise Exception
