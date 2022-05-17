import sys
from datetime import datetime
import time
import hashlib
import requests

import uvicorn
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from constant import DummyData, ServerConfig, AuthConfig, RateLimitConfig, MediaAssets, ContentLimit, START_TIME, PROGRAM_HASH
from route import v1, v2

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(v1.router)
app.include_router(v2.router, prefix="/v2")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger = open(file=f"{int(START_TIME.timestamp())}.FastAPI.log", mode="a", encoding="utf-8")
    logger.write(f"time={str(datetime.now())} ip={request.client.host} method={request.method} path=\"{request.url.path}\" ")
    response: Response = await call_next(request)
    process_time = f"{(datetime.now() - start_time).microseconds / 1000}ms"
    response.headers["X-Process-Time"] = process_time
    logger.write(f"completed_in={process_time} status_code={response.status_code}\n")
    return response


@app.get("/")
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def hello_world(request: Request):
    return JSONResponse(status_code=200, content={"message": "hello, documentation available at /docs"})


@app.get("/favicon.ico")
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def get_favicon(request: Request):
    return RedirectResponse(url=MediaAssets.FAVICON)


@app.get("/ip", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def request_ip(request: Request):
    return JSONResponse(status_code=200, content={"ip": get_remote_address(request=request)})


@app.get("/header", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def request_header(request: Request):
    return JSONResponse(status_code=200, content=dict(request.headers))


@app.get("/version", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def api_version(request: Request):
    return JSONResponse(status_code=200, content={"version": ServerConfig.CURRENT_VERSION})


@app.get("/timestamp", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def request_timestamp(request: Request):
    return JSONResponse(status_code=200, content={"timestamp": str((int(datetime.now().timestamp())))})


@app.get("/status", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def api_status(request: Request):
    return JSONResponse(status_code=200, content={"status": f"alive", "uptime": f"{datetime.now() - START_TIME}", "version": PROGRAM_HASH})


@app.get("/server/list", tags=["General Methods"])
@limiter.limit(RateLimitConfig.HIGH_SENSITIVITY)
def api_server_list(request: Request):
    return JSONResponse(status_code=200, content={"server_list": ServerConfig.API_SERVER_LIST})


@app.get("/server/assignment", tags=["General Methods"])
@limiter.limit(RateLimitConfig.LOW_SENSITIVITY)
def api_server_assignment(request: Request):
    return JSONResponse(status_code=200, content={"recommended_servers": [{"priority": 0, "load": 0, "display_name": "", "URL": "", "provider": "", "location": ""}]})


@app.get("/test/connection", tags=["General Methods"])
@limiter.limit(RateLimitConfig.SMALL_SIZE)
def api_test_connection(request: Request):
    print(requests.get("https://www.google.com/", timeout=5).status_code)
    return JSONResponse(status_code=200, content={})


@app.get("/tool/delay", tags=["Utility"])
def api_tool_delay(request: Request, sleep_time: int):
    time.sleep(sleep_time)
    return JSONResponse(status_code=200, content={"status": "finished"})


class DummyMethod:
    @app.get("/dummy", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.NO_COMPUTE)
    def dummy(request: Request):
        return {"status": "ok"}

    @app.get("/dummy/user/profile", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.MIN_DB)
    def dummy_user_profile(request: Request):
        return DummyData.USER_PROFILE_5

    @app.get("/dummy/user/calendar", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.SOME_DB)
    def dummy_user_calendar(request: Request):
        return DummyData.USER_CALENDAR

    @app.get("/dummy/auth/decrypt", tags=["Dummy Data"])
    @limiter.limit(RateLimitConfig.LESS_COMPUTE)
    def dummy_auth_decrypt(request: Request, encrypted_sha512_string: str, auth_token: str, timestamp: str):
        if len(auth_token) == AuthConfig.TOKEN_LENGTH:
            if hashlib.sha512((auth_token + timestamp).encode("utf-8")).hexdigest() == encrypted_sha512_string:
                return {"auth_status": "ok"}
            else:
                return {"auth_status": "failed", "error": "auth_token not match"}
        else:
            return {"auth_status": "failed", "error": "invalid auth_token format"}



if __name__ == "__main__":
    if sys.platform == "win32":
        uvicorn.run("server:app", debug=True, reload=True, port=ServerConfig.PORT, host=ServerConfig.HOST, limit_concurrency=ServerConfig.CONCURRENCY, log_level=ServerConfig.LOG_LEVEL)
    else:
        uvicorn.run("server:app", debug=True, reload=False, port=ServerConfig.PORT, host=ServerConfig.HOST, limit_concurrency=ServerConfig.CONCURRENCY, log_level=ServerConfig.LOG_LEVEL)
