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


class AccessControl(BaseModel):
    canonical_name: Optional[str]
    person_id: Optional[str]
    permission_list: List[str] = ["read_full", "edit_full", "delete"]


"""
Is possible to stack multiple BaseModel class into one
"""


class CalendarEvent(BaseModel):
    display_name: str = "my event"
    description: str = "my description"
    start_time: TimeObject
    end_time: TimeObject
    access_control_list: List[AccessControl]
    type_list: List[TypeObject]
    tag_list: List[TagObject]


class RegistrationUser(BaseModel):
    name: str


class PasswordLoginBody(BaseModel):
    person_id: str
    password: str
    token_lifespan: int = 60 * 60 * 24 * 1


class PictureLink(BaseModel):
    image_id: str
    image_url: str


class EmailAddress(BaseModel):
    domain_name: str
    full_address: str


class PhoneNumber(BaseModel):
    country_code: str
    regular_number: str


class PhysicalAddress(BaseModel):
    full_address: str
    street_address: str
    city: str
    province: str
    country: str
    continent: str
    post_code: str


class TwitterUser(BaseModel):
    user_name: str
    user_handle: str
    user_id: str


class GithubUser(BaseModel):
    user_name: str
    user_handle: str


class NamingSection(BaseModel):
    unique_name: str
    display_name_partial: str
    display_name_full: str


class PictureSection(BaseModel):
    avatar: PictureLink
    background: PictureLink


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
    email_primary: EmailAddress
    phone: PhoneNumber
    physical_address: PhysicalAddress
    twitter: TwitterUser
    github: GithubUser


class UserProfileObject(BaseModel):
    naming: NamingSection
    picture: PictureSection
    about: AboutSection
    status: StatusSection
    contact_method_collection: ContactMethodSection


class GitHubOAuthCode(BaseModel):
    code: str
