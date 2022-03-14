from pydantic import BaseModel


class RequestUserProfile(BaseModel):
    person_id: str

class UpdateUserProfileName_DisplayName(BaseModel):
    display_name: str

class UpdateUserProfileAbout_Description(BaseModel):
    short_description: str
    full_description: str

class UpdateUserProfileStatus(BaseModel):
    current_status: str
