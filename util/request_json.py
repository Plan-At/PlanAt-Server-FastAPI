from pydantic import BaseModel


class RequestUserProfile(BaseModel):
    person_id: str

class UpdateUserProfileName_DisplayName(BaseModel):
    display_name: str
