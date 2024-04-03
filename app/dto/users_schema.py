from pydantic import BaseModel
from typing import List, Optional


class UserSchema(BaseModel):
    name: str
    email: str
    contact_number: str
    address: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    country_id: Optional[int] = 0
    zip_code: Optional[str] = ""
    roles: List[str] = []

    class Config:
        orm_mode = True
