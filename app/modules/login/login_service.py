from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session,load_only
from config.database import get_db, response,msg
from app.dto.response_schema import ResponseSchema
from app.dto.login_schema import LoginSchema
from app.helper.general_helper import Helper

class LoginService:
    def user_authentication(request: LoginSchema, db: Session = Depends(get_db)):
        try:
            user_authentication = Helper.user_login(db=db, request=request)
            if user_authentication is not None:
                return user_authentication
            else:
                return False
        except Exception as e:
            return False


        