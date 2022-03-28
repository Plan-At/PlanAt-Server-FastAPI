from typing import Dict, List, Optional
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

class OwnerObject(BaseModel):
    person_id: Optional[str] = "1234567890"


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
    owner_list: List[OwnerObject]
    visibility: str = "private"
    display_name: str = "my event"
    description: str = "my description"
    start_time: TimeObject
    end_time: TimeObject
    type_list: List[TypeObject]
    tag_list: List[TagObject]
    