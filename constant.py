import hashlib
from datetime import datetime

START_TIME = datetime.now()
PROGRAM_HASH = hashlib.md5(open(__file__, mode="rb").read()).hexdigest()


class ServerConfig:
    PORT = 8000
    HOST = "127.0.0.1"
    CONCURRENCY = 8
    CURRENT_VERSION = "v1"
    API_SERVER_LIST = [
        {"priority": 0, "load": 0, "name": "Primary", "URL": "https://api-0.752628.xyz/", "provider": "Official", "location": "US-West"}]
    IMAGEBED_FOLDER = "/Plan-At/usercontent"
    LOG_LEVEL = "debug"


class AuthConfig:
    PERSON_ID_LENGTH = 10
    TOKEN_LENGTH = 8


class ContentLimit:
    DISPLAY_NAME_LENGTH = 20
    SHORT_DESCRIPTION = 100
    LONG_DESCRIPTION = 500
    USER_STATUS = 15
    PUBLIC_EVENT_ID_INDEX = 50
    IMAGE_SIZE = 1024 * 1024 * 4


class RateLimitConfig:
    ENABLE_RL = False
    if ENABLE_RL:
        NO_COMPUTE = "2/second"
        LESS_COMPUTE = "1/second"
        SOME_COMPUTE = "1/3second"
        MORE_COMPUTE = "1/5second"
        INTENSE_COMPUTE = "1/10second"
        MIN_DB = "2/3second"
        SOME_DB = "2/5second"
        MAX_DB = "2/15second"
        MICRO_SIZE = "1/second"
        SMALL_SIZE = "1/5second"
        MID_SIZE = "1/30second"
        BIG_SIZE = "1/minute"
        LOW_SENSITIVITY = "1/10second"
        MID_SENSITIVITY = "1/30second"
        HIGH_SENSITIVITY = "1/minute"
        BURST = "20/minute"
    else:
        NO_COMPUTE = "100/second"
        LESS_COMPUTE = "100/second"
        SOME_COMPUTE = "100/second"
        MORE_COMPUTE = "100/second"
        INTENSE_COMPUTE = "100/second"
        MIN_DB = "100/second"
        SOME_DB = "100/second"
        MAX_DB = "100/second"
        MICRO_SIZE = "100/second"
        SMALL_SIZE = "100/second"
        MID_SIZE = "10/second"
        BIG_SIZE = "10/second"
        LOW_SENSITIVITY = "100/second"
        MID_SENSITIVITY = "100/second"
        HIGH_SENSITIVITY = "100/second"
        BURST = "1000/second"


class MediaAssets:
    FAVICON = "https://cdn.jsdelivr.net/gh/Plan-At/static-image/2022/02/17/favicon.ico"
