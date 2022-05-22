# Framework core library
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("", tags=["V2"])
async def v2_endpoint():
    return JSONResponse(status_code=200, content={"status": "implementing"})
