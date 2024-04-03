from pydantic import BaseModel

class LoginSchema(BaseModel):
    user_name: str
    password: str