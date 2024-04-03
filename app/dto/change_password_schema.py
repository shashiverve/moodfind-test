from pydantic import BaseModel

class ChangePasswordSchema(BaseModel):
    email:str
    password:str
    c_password:str

class VerifyForgotPasswordOTPSchema(BaseModel):
    email: str
    otp: int

class SentForgotPasswordOTPSchema(BaseModel):
    email: str