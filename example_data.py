USER_PROFILE_5 = {
    "structure_version": 5,
    "person_id": "1234567890",
    "metadata": {
        "uuid": "6cb63b46-00ce-4433-a7e1-c839e94c1315",
        "seed": "56467484686",
        "registration_timestamp_int": "1646081914"
    },
    "naming": {
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
            "original": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/avatar/s=128/HW",
            }
        },
        "background": {
            "regular": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
            },
            "original": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/og/Hello%20World.jpg",
            }
        }
    },
    "status": {
        "current_status": "Developing",
        "until": {
            "text": "Extraday 13AM",
            "timestamp_int": 0,
            "timezone_name": "Mars",
            "timezone_offset": 0
        },
        "default_status": "Alive"
    },
    "about": {
        "short_description": "I",
        "full_description": "I'm here"
    },
    "contact_method_list": [
        {
            "method_name": "email",
            "domain_name": "example.com",
            "full_address": "example@example.com",
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
            "method_name": "phone",
            "country_code": "",
            "regular_number": "1234567890",
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
                "structure_version": 5,
                "event_id": 1234567890123456,
                "access_control_list": [
                    {
                        "person_id": "1234567890",
                        "premission": ["read", "edit", "delete"]
                    }
                ],
                "visibility": "public",
                "start_time": {
                    "text": "Monday 9AM",
                    "timestamp_int": 0,
                    "timezone_name": "America/Los_Angeles",
                    "timezone_offset": 0
                },
                "end_time": {
                    "text": "Monday 10AM",
                    "timestamp_int": 0,
                    "timezone_name": "",
                    "timezone_offset": 0
                },
                "display_name": "work",
                "description": "endless work",
                "type_list": [{"type_id": "", "name": "work"}],
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

TOKEN_INFO_2 = {
    "structure_version": 2,
    "person_id": "1234567890",
    "token_value": "aaaaaaaa",
    "token_hash": ""
}

TOKEN_INFO_3 = {
    "structure_version": 3,
    "person_id": "1234567890",
    "token_value": "aaaaaaaa",
    "token_hash": "f74f2603939a53656948480ce71f1ce466685b6654fd22c61c1f2ce4e2c96d1cd02d162b560c4beaf1ae45f3471dc5cbc1ce040701c0b5c38457988aa00fe97f",
    "creation_timestamp_int": 1653022969,
    "expiration_timestamp_int": 1658293369
}

PASSWORD_INFO = {
    "structure_version": 1,
    "person_id": "1234567890",
    "password_hash": "12B03226A6D8BE9C6E8CD5E55DC6C7920CAAA39DF14AAB92D5E3EA9340D1C8A4D3D0B8E4314F1F6EF131BA4BF1CEB9186AB87C801AF0D5C95B1BEFB8CEDAE2B9",
    "password_length": 8,
}

# For directly compatible with vanilla JSON, do not add comma after each last item
# Abandoned some not very essential item, but possible to add back later
USER_PROFILE_6 = {
    "structure_version": 6,
    "person_id": "1234567890",
    "metadata": {
        "uuid": "6cb63b46-00ce-4433-a7e1-c839e94c1315",
        "seed": "56467484686",
        "registration_timestamp_int": "1646081914"
    },
    "naming": {
        "unique_name": "abced",
        "display_name_partial": "Hello",
        "display_name_full": "HelloWorld",
        "localization": [],
        "historical_name": []
    },
    "picture": {
        "avatar": {
            "regular": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/avatar/s=64/HW"
            },
            "original": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/avatar/s=128/HW"
            }
        },
        "background": {
            "regular": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/og/Hello%20World.jpg"
            },
            "original": {
                "image_id": "",
                "image_url": "https://cdn.statically.io/og/Hello%20World.jpg"
            }
        }
    },
    "status": {
        "current_status": "Developing",
        "until": {
            "text": "Extraday 13AM",
            "timestamp_int": 0,
            "timezone_name": "Mars",
            "timezone_offset": 0
        },
        "default_status": "Alive"
    },
    "about": {
        "short_description": "I",
        "full_description": "I'm here",
        "company_name": "",
        "job_title": ""
    },
    "contact_method_collection": {
        "email_primary": {
            "domain_name": "example.com",
            "full_address": "example@example.com"
        },
        "phone": {
            "country_code": "",
            "regular_number": "1234567890"
        },
        "physical_address": {
            "street_address": "",
            "city": "",
            "province": "",
            "country": "",
            "continent": "",
            "post_code": ""
        },
        "github": {
            "user_name": "",
            "user_handle": ""
        },
        "twitter": {
            "user_name": "",
            "user_handle": "",
            "user_id": ""
        }
    }
}


USER_PROFILE_7 = {
    "structure_version": 7,
    "person_id": "1234567890",
    "metadata": {
        "uuid": "6cb63b46-00ce-4433-a7e1-c839e94c1315",
        "seed": "56467484686",
        "registration_timestamp_int": "1646081914"
    },
    "naming": {
        "unique_name": "abced",
        "display_name_partial": "Hello",
        "display_name_full": "HelloWorld",
        "localization": [],
        "historical_name": []
    },
    "picture": {
        "avatar": {
            "image_id": "",
            "image_url": "https://cdn.statically.io/avatar/s=128/HW"
        },
        "background": {
            "image_id": "",
            "image_url": "https://cdn.statically.io/og/Hello%20World.jpg"
        }
    },
    "about": {
        "short_description": "I",
        "full_description": "I'm here",
        "company_name": "",
        "job_title": ""
    },
    "status": {
        "current_status": "Developing",
        "until": {
            "text": "Extraday 13AM",
            "timestamp_int": 0,
            "timezone_name": "Mars",
            "timezone_offset": 0
        },
        "default_status": "Alive"
    },
    "contact_method_collection": {
        "email_primary": {
            "domain_name": "example.com",
            "full_address": "example@example.com"
        },
        "phone": {
            "country_code": "",
            "regular_number": "1234567890"
        },
        "physical_address": {
            "full_address": "",
            "street_address": "",
            "city": "",
            "province": "",
            "country": "",
            "continent": "",
            "post_code": ""
        },
        "github": {
            "user_name": "",
            "user_handle": ""
        },
        "twitter": {
            "user_name": "",
            "user_handle": "",
            "user_id": ""
        }
    }
}

HOSTING_IMAGE = {
    "structure_version": 1,
    "image_url": "https://cdn.image4.io/as-an-imagebed/f_auto/Plan-At/usercontent/16490351977f8394ebab084c34406531918337c425.png",
    "image_id": "16490351977f8394ebab084c34406531918337c425",
    "image_file_name": "16490351977f8394ebab084c34406531918337c425.png",
    "image_file_path": "/Plan-At/usercontent/16490351977f8394ebab084c34406531918337c425.png",
    "image_size": 0,
    "image_width": 0,
    "image_hright": 0,
    "hosting_provider": "image4io"
}
