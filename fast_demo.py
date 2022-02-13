import logging
import sys
from datetime import datetime
import uvicorn
from fastapi import FastAPI
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
    return {"message": "hello, documentation available at \"/docs\""}

@app.get("/server-list")
def api_servers():
    return {"primary_servers": [{"priority": 0, "name": "", "URL": "", "provider": "", "location": ""}]}

@app.get("/version", tags=["General Methods"])
def api_version():
    return {"version": "v1"}

@app.get("/status", tags=["General Methods"])
@limiter.limit("5/10second")
def api_status(request: Request):
    return {"status": "ok"}

@app.get("/ip", tags=["General Methods"])
def client_ip(request: Request):
    return {"ip": get_remote_address(request=request)}

@app.get("/v1", tags=["V1"])
def v1_endpoint():
    return {"status": "ok"}

@app.get("/v1/private/user/profile", tags=["V1"])
def v1_private_user_profile():
    return {"status": "empty"}

@app.get("/v1/public/user/profile", tags=["V1"])
@limiter.limit("5/minute")
def v1_public_user_profile(request: Request, user_id: str):
    return {"status": "ok", "display_name": user_id}

if __name__ == "__main__":
    if sys.platform == "win32":
        uvicorn.run("fast_demo:app", debug=True, reload=True, port=8000)
    else:
        uvicorn.run("fast_demo:app", debug=True, reload=False, port=80, host="0.0.0.0")