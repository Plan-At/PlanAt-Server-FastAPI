import sys
from datetime import datetime
import time
import traceback
import requests

import uvicorn
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from constant import ServerConfig, RateLimitConfig, MediaAssets, START_TIME, PROGRAM_HASH, APITag
from route import fake, v2_captcha, v2_auth, v2_user, v2_calendar, v2_hosting
from util import docs_page

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(v2_auth.router, prefix="/v2/auth", tags=APITag.AUTH)
app.include_router(v2_calendar.router, prefix="/v2/calendar", tags=APITag.CALENDAR)
app.include_router(v2_user.router, prefix="/v2/user", tags=APITag.USER)
app.include_router(v2_hosting.router, prefix="/v2/hosting", tags=APITag.HOSTING)
app.include_router(v2_captcha.router, prefix="/v2/captcha", tags=APITag.CAPTCHA)
app.include_router(fake.router, prefix="/fake", tags=APITag.EXAMPLE)

"""
enable this for local development or when it's not reverse proxied
"""
if ServerConfig.ADD_CORS_HEADER:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    print(exc)
    return Response(
        status_code=200,  # return 500 here might not show any text
        content="".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)  # Not compatible with Python3.10
        )
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=ServerConfig.TITLE,
        version=ServerConfig.SEMVER,
        description=ServerConfig.DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": MediaAssets.FAVICON
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def hello_world(request: Request):
    # return JSONResponse(status_code=200, content={"message": "hello, documentation available at /docs"})
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", tags=["General Methods"])
@limiter.limit(RateLimitConfig.NO_COMPUTE)
def get_favicon(request: Request):
    return RedirectResponse(url=MediaAssets.FAVICON)


@app.get("/doc", include_in_schema=False)
def overridden_swagger():
    return HTMLResponse(status_code=200, content=docs_page.HTML)


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Plan-At", swagger_favicon_url=MediaAssets.FAVICON)


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url="/openapi.json", title="Plan-At", redoc_favicon_url=MediaAssets.FAVICON)


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
    return JSONResponse(status_code=200, content={"status": "alive",
                                                  "uptime": f"{datetime.now() - START_TIME}",
                                                  "version": PROGRAM_HASH})


@app.get("/test/connection", tags=["General Methods"])
@limiter.limit(RateLimitConfig.SMALL_SIZE)
def api_test_connection(request: Request):
    print(requests.get("https://www.google.com/", timeout=5).status_code)
    return JSONResponse(status_code=200, content={})


@app.get("/tool/delay", tags=["Utility"])
def api_tool_delay(request: Request, sleep_time: int):
    time.sleep(sleep_time)
    return JSONResponse(status_code=200, content={"status": "finished"})


@app.get("/everything", tags=["General Methods"])
async def receive_everything_get(request: Request):
    print(request.headers)
    print(await request.body())
    return JSONResponse(status_code=200, content={"status": "finished"})


@app.post("/everything", tags=["General Methods"])
async def receive_everything_post(request: Request):
    print(request.headers)
    print(await request.body())
    return JSONResponse(status_code=200, content={"status": "finished"})


if __name__ == "__main__":
    if sys.platform == "win32":
        uvicorn.run("server:app", debug=True, reload=True, port=ServerConfig.PORT, host=ServerConfig.HOST,
                    limit_concurrency=ServerConfig.CONCURRENCY, log_level=ServerConfig.LOG_LEVEL)
    else:
        uvicorn.run("server:app", debug=True, reload=False, port=ServerConfig.PORT, host=ServerConfig.HOST,
                    limit_concurrency=ServerConfig.CONCURRENCY, log_level=ServerConfig.LOG_LEVEL)
