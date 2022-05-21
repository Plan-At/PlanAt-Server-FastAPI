from typing import List, Optional
from pydantic import BaseModel


class TimeObject(BaseModel):
    text: str
    timestamp_int: int
    timezone_name: str
    timezone_offset: int


class TypeObject(BaseModel):
    type_id: str
    display_name: str


class TagObject(BaseModel):
    tag_id: str
    display_name: str


class ACObject(BaseModel):
    canonical_name: Optional[str]
    person_id: Optional[str]
    permission_list: List[str] = ["read_full", "edit_full", "delete"]


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
    access_control_list: List[ACObject]
    display_name: str = "my event"
    description: str = "my description"
    start_time: TimeObject
    end_time: TimeObject
    type_list: List[TypeObject]
    tag_list: List[TagObject]


class RegistrationUser(BaseModel):
    name: str


class UnsafeLoginBody(BaseModel):
    person_id: str
    password: str
    token_lifespan: int = 60 * 60 * 24 * 1


class PictureObject(BaseModel):
    image_id: str
    image_url: str


class EmailObject(BaseModel):
    domain_name: str
    full_address: str


class PhoneNumberObject(BaseModel):
    country_code: str
    regular_number: str


class PhysicalAddressObject(BaseModel):
    full_address: str
    street_address: str
    city: str
    province: str
    country: str
    continent: str
    post_code: str


class TwitterObject(BaseModel):
    user_name: str
    user_handle: str
    user_id: str


class NamingSection(BaseModel):
    unique_name: str
    display_name_partial: str
    display_name_full: str


class PictureSection(BaseModel):
    avatar: PictureObject
    background: PictureObject


class StatusSection(BaseModel):
    current_status: str
    until: TimeObject
    default_status: str


class AboutSection(BaseModel):
    short_description: str
    full_description: str
    company_name: str
    job_title: str


class ContactMethodSection(BaseModel):
    email_primary: EmailObject
    phone: PhoneNumberObject
    physical_address: PhysicalAddressObject
    twitter: TwitterObject


class UserProfileObject(BaseModel):
    naming: NamingSection
    picture: PictureSection
    about: AboutSection
    status: StatusSection
    contact_method_collection: ContactMethodSection
