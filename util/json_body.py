from crypt import methods
from typing import List
from pydantic import BaseModel

class TimeObject(BaseModel):
    text: str
    timestamp: int
    timezone_name: str
    timezone_offset: int


class TypeObject(BaseModel):
    type_id: str
    name: str


class TagObject(BaseModel):
    tag_id: str
    name: str


"""
Is possible to stack multiple BaseModel class into one
"""

class RequestUserProfile(BaseModel):
    person_id: str


class UpdateUserProfileName_DisplayName(BaseModel):
    display_name: str


class UpdateUserProfileAbout_Description(BaseModel):
    short_description: str
    full_description: str


class UpdateUserProfileStatus(BaseModel):
    current_status: str


class AddUserCalendarEvent(BaseModel):
    visibility: str
    display_name: str
    description: str
    start_time: TimeObject
    end_time: TimeObject
    type_list: List[TypeObject]
    tag_list: List[TagObject]
    