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
    canonical_name: Optional[str]
    person_id: Optional[str]
    

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


class CalendarEventObject(BaseModel):
    access_control_list: List[OwnerObject]
    display_name: str = "my event"
    description: str = "my description"
    start_time: TimeObject
    end_time: TimeObject
    type_list: List[TypeObject]
    tag_list: List[TagObject]

class RegistrationUser(BaseModel):
    name: str
