from pydantic import BaseModel


class RequestUserProfile(BaseModel):
    person_id: str
