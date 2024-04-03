from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.login_schema import LoginSchema
from app.modules.login.login_service import LoginService
from app.dto.response_schema import ResponseSchema

router = APIRouter(prefix="/api", tags=["Admin login"])

@router.post("/login",summary="Login with email and password", response_model=ResponseSchema)
def loginUser(request: LoginSchema, db: Session = Depends(get_db)):
    logged_user = LoginService.user_authentication(db=db, request=request)
    if logged_user is not False and type(logged_user)!= str:
        return ResponseSchema(response=msg['user_logged_in'], data=logged_user.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['invalid_password_email'], data=[])