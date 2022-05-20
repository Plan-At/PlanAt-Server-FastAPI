import hashlib

from starlette.requests import Request
from fastapi import APIRouter

from constant import DummyData, AuthConfig

router = APIRouter()


@router.get("", tags=["Dummy Data"])
def dummy(request: Request):
    return {"status": "ok"}


@router.get("/user/profile", tags=["Dummy Data"])
def dummy_user_profile(request: Request):
    return DummyData.USER_PROFILE_5


@router.get("/user/calendar", tags=["Dummy Data"])
def dummy_user_calendar(request: Request):
    return DummyData.USER_CALENDAR


@router.get("/auth/decrypt", tags=["Dummy Data"])
def dummy_auth_decrypt(request: Request, encrypted_sha512_string: str, auth_token: str, timestamp: str):
    if len(auth_token) == AuthConfig.TOKEN_LENGTH:
        if hashlib.sha512((auth_token + timestamp).encode("utf-8")).hexdigest() == encrypted_sha512_string:
            return {"auth_status": "ok"}
        else:
            return {"auth_status": "failed", "error": "auth_token not match"}
    else:
        return {"auth_status": "failed", "error": "invalid auth_token format"}


@router.get("/error/internal", tags=["Dummy Data"])
async def fake_internal_error(request: Request):
    raise Exception
