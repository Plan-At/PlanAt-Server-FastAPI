import logging
import sys
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger = open(file="fast_demo.log", mode="a", encoding="utf-8")
    logger.write(f"time={str(datetime.now())} ip={request.client.host} method={request.method} path=\"{request.url.path}\" ")
    response = await call_next(request)
    logger.write(f"completed_in={(datetime.now()-start_time).microseconds/1000}ms status_code={response.status_code}\n")
    return response

@app.get("/")
def hello_world():
    return {"message": "hello, documentation available at /docs"}

@app.get("/favicon.ico")
def get_favicon():
    return FileResponse(path="./favicon.ico", filename="favicon.ico")

@app.get("/ip", tags=["General Methods"])
def client_ip(request: Request):
    return {"ip": get_remote_address(request=request)}


@app.get("/version", tags=["General Methods"])
def api_version():
    return {"version": "v1"}

@app.get("/status", tags=["General Methods"])
@limiter.limit("5/10second")
def api_status(request: Request):
    return {"status": "ok"}

@app.get("/server/list", tags=["General Methods"])
@limiter.limit("1/minute")
def api_server_list(request: Request):
    return {"server_list": [{"priority": 0, "load": 0, "name": "", "URL": "", "provider": "", "location": ""}]}

@app.get("/server/assignment", tags=["General Methods"])
@limiter.limit("1/minute")
def api_server_assignment(request: Request):
    return {"recommended_servers": [{"priority": 0, "load": 0, "name": "", "URL": "", "provider": "", "location": ""}]}


@app.get("/dummy", tags=["Dummy Data"])
def dummy():
    return {"status": "ok"}

@app.get("/dummy/user/profile", tags=["Dummy Data"])
def dummy_user_profile():
    return {"id":"","profile_url":"","unique_name":"","display_name":"","picture":{"avatar":{"regular":"","full":""},"background":{"regular":"","full":""}},"status":{"current_status":"","until":"","default_status":""},"about":{"short_decription":"","full_decription":""},"contact":{"email":"","phone":""},"public_tags":[{"id":"","name":""}],"public_friends":[{"id":"","name":""}],"public_teams":[{"id":"","name":""}]}

@app.get("/dummy/user/calendar", tags=["Dummy Data"])
def dummy_user_calendar():
    return {"status": "ok"}


@app.get("/v1", tags=["V1"])
def v1():
    return {"status": "ok"}

@app.get("/v1/public/stats", tags=["V1"])
@limiter.limit("5/minute")
def v1_public_stats(request: Request):
    return {"status": "ok"}

@app.get("/v1/restricted/stats", tags=["V1"])
@limiter.limit("5/minute")
def v1_restricted_stats(request: Request):
    return {"status": "ok"}

@app.get("/v1/public/user/profile", tags=["V1"])
@limiter.limit("5/minute")
def v1_public_user_profile(request: Request, user_id: str):
    return {"status": "ok", "display_name": user_id}

@app.get("/v1/private/user/profile", tags=["V1"])
def v1_private_user_profile():
    return {"status": "empty"}

if __name__ == "__main__":
    if sys.platform == "win32":
        uvicorn.run("fast_demo:app", debug=True, reload=True, port=8000, host="127.0.0.1", limit_concurrency=8)
    else:
        uvicorn.run("fast_demo:app", debug=True, reload=False, port=80, host="0.0.0.0", limit_concurrency=8)