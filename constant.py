class ServerConfig:
    PORT = 8000
    HOST = "127.0.0.1"
    CONCURRENCY = 8
    CURRENT_VERSION = "v1"
    API_SERVER_LIST = [
        {"priority": 0, "load": 0, "name": "Primary", "URL": "https://api-0.752628.xyz/", "provider": "Official", "location": "US-West"}]


class AuthConfig:
    PERSON_ID_LENGTH = 10
    TOKEN_LENGTH = 8

class ContentLimit:
    DISPLAY_NAME_LENGTH = 20
    SHORT_DESCRIPTION = 100
    LONG_DESCRIPTION = 500
    USER_STATUS = 15
    PUBLIC_EVENT_ID_INDEX = 50


class RateLimitConfig:
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


class MediaAssets:
    FAVICON = "https://cdn.jsdelivr.net/gh/Plan-At/static-image/2022/02/17/favicon.ico"


class DummyData:
    USER_PROFILE = {
        "structure_version": 1,
        "person_id": "1234567890",
        "metadata": {
            "uuid": "6cb63b46-00ce-4433-a7e1-c839e94c1315",
            "seed": "56467484686",
            "registration_timestamp": "1646081914"
        },
        "name": {
            "unique_name": "abced",
            "display_name": "HelloWorld",
            "localization": [],
            "historical_name": [],
            "searchable": True
        },
        "picture": {
            "avatar": {
                "regular": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/avatar/s=64/HW",
                },
                "full": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/avatar/s=128/HW",
                }
            },
            "background": {
                "regular": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
                },
                "full": {
                    "image_id": "",
                    "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
                }
            }
        },
        "status": {
            "current_status": "Developing",
            "until": {
                "text": "Extraday 13AM",
                "timestamp": 0,
                "timezone_name": "Mars",
                "timezone_offset": 0
            },
            "default_status": "Alive"
        },
        "about": {
            "short_description": "I",
            "full_description": "I'm here"
        },
        "contact": [
            {
                "method": "email",
                "value": {
                    "domain": "example.com",
                    "full": "example@example.com",
                },
                "visibility": {
                    "system_contact": True,
                    "public": True,
                    "searchable": True,
                    "organization_default": True,
                    "organization_visible": [],
                    "organization_invisible": [],
                    "friend_default": True,
                    "friend_visible": [],
                    "friend_invisible": []
                }
            },
            {
                "method": "phone",
                "value": {
                    "country_code": "",
                    "full": "1234567890",
                },
                "visibility": {
                    "system_contact": True,
                    "public": True,
                    "searchable": True,
                    "organization_default": True,
                    "organization_visible": [],
                    "organization_invisible": [],
                    "friend_default": True,
                    "friend_visible": [],
                    "friend_invisible": []
                }
            }
        ],
        "usergroup": [],
        "public_tag_list": [{"tag_id": "123", "name": "OP"}],
        "public_friend_list": [{"person_id": "", "name": ""}],
        "public_team_list": [{"org_id": "", "name": ""}]
    }
    USER_CALENDAR = {
        "structure_version": 1,
        "person_id": "",
        "calendar_event":
            [
                {
                    "structure_version": 2,
                    "event_id": 1234567890123456,
                    "owner_list": [{"person_id": "1234567890"}],
                    "visibility": "public",
                    "start_time": {
                        "text": "Monday 9AM",
                        "timestamp": 0,
                        "timezone_name": "America/Los_Angeles",
                        "timezone_offset": 0
                    },
                    "end_time": {
                        "text": "Monday 10AM",
                        "timestamp": 0,
                        "timezone_name": "",
                        "timezone_offset": 0
                    },
                    "display_name": "work",
                    "description": "endless work",
                    "type_list": [{"type_id": "","name": "work"}],
                    "tag_list": [{"tag_id": "", "name": "mandatory"}, {"tag_id": "", "name": "not fun"}]
                }
            ]
        }
    
    USER_CALENDAR_EVENT_INDEX = {
        "structure_version": 1,
        "person_id": "1234567890",
        "event_id_list": [
            123456789001,
            123456789002,
            123456789003
        ]
    }
