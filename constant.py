class AuthConfig:
    TOKEN_LENGTH = 8

class RateLimitConfig:
    NO_COMPUTE = "2/second"
    LESS_COMPUTE = "1/second"
    SOME_COMPUTE = "1/3second"
    MORE_COMPUTE = "1/5second"
    INTENSE_COMPUTE = "1/10second"

    MIN_DB = "1/3second"
    SOME_DB = "1/5second"
    MAX_DB = "1/15second"

    MICRO_SIZE = "1/second"
    SMALL_SIZE = "1/5second"
    MID_SIZE = "1/30second"
    BIG_SIZE = "1/minute"

    LOW_SENSITIVITY = "1/10second"
    MID_SENSITIVITY = "1/30second"
    HIGH_SENSITIVITY = "1/minute"

class MediaAssets:
    FAVICON = "https://cdn.jsdelivr.net/gh/Plan-At/static-image/2022/02/17/favicon.ico"