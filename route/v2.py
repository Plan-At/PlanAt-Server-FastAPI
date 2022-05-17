from typing import Optional, List
import sys
import json
from datetime import datetime
import time
import hashlib
import requests

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from fastapi import APIRouter, Header, File, Query
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

router = APIRouter()

@router.get("", tags=["V2"])
async def v2_endpoint():
    return JSONResponse(status_code=200, content={"status": "implementing"})
    