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

@app.get("/")
def hello_world():
    return {"message": "hello"}

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

@app.get("/v1/user", tags=["V1"])
def v1_user():
    return {"status": "ok"}

@app.get("/v1/user/profile", tags=["V1"])
def v1_user_profile(display_name: str):
    return {"status": "ok", "display_name": display_name}

if __name__ == "__main__":
    print(__file__)
    uvicorn.run("fast_demo:app", debug=True, reload=True)