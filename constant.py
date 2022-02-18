class ServerConfig:
    PORT = 8000
    HOST = "127.0.0.1"
    CONCURRENCY = 8
    CURRENT_VERSION = "v1"
    API_SERVER_LIST = [{"priority": 0, "load": 0, "name": "Primary", "URL": "https://api-0.752628.xyz/", "provider": "Official", "location": "US-West"}]

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

class DummyData:
    USER_PROFILE = {"id":"","profile_url":"","unique_name":"","display_name":"","picture":{"avatar":{"regular":"","full":""},"background":{"regular":"","full":""}},"status":{"current_status":"","until":"","default_status":""},"about":{"short_description":"","full_description":""},"contact":{"email":"","phone":""},"public_tags":[{"id":"","name":""}],"public_friends":[{"id":"","name":""}],"public_teams":[{"id":"","name":""}]}
    USER_CALENDAR = {"id":"","username":"","calendar_entry":[{"object_id":"1","event_id":"1","owner":"me","visibility":"public","start":"Monday 9AM","end":"Monday 9PM","name":"work","description":"endless work","type":"work","tags":["work","mandatory","not fun"]},{"object_id":"2","event_id":"2","owner":"me","visibility":"private","start":"Monday 9PM","end":"Monday 11PM","name":"rest","description":"having fun","type":"work","tags":["gaming","fun"]},{"object_id":"3","event_id":"3","owner":"me","visibility":"public","start":"Tuesday 9AM","end":"Tuesday 9PM","name":"work","description":"endless work","type":"work","tags":["work","mandatory","not fun"]}]}