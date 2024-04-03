from pydantic import BaseModel
from typing import List, Optional


class UserSessionsSchema(BaseModel):
    model_id:int
    ethnicity_id:int
    other_ethnicity:Optional[str] = ""
    gender:int
    other_gender:Optional[str] = ""
    age:int
    user_agent:Optional[str] = ""
    device_type:Optional[str] = ""

    class Config:
        orm_mode = True