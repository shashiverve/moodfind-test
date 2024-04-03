from fastapi import APIRouter, Depends, File, Form, UploadFile,Request
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from typing import Optional
from app.modules.admin_view.admin_view_service import AdminViewService
from app.modules.user_responses.user_responses_service import UserResponseService
from fastapi_pagination import Params
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/api/admin", tags=["Admin View"],dependencies=[Depends(JWTBearer())])

# route for the get all users response for admin view
@router.get("/list_user_responses", summary="Get All Users Response Data")
def getAllUserResponseData(params: Params = Depends(),search_string:Optional[str]=None,sort_by: Optional[str] = None,sort_direction: Optional[str] = None,db: Session = Depends(get_db)):
    users_response_data = AdminViewService.getAllUserResponseData(params=params, search_string=search_string, sort_by=sort_by, sort_direction=sort_direction, db=db)
    if users_response_data is not False:
        return ResponseSchema(response=msg['all_users_response_found'], data=users_response_data)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])

#route for the get single user details response 
@router.get("/single_user_response", summary="Get Single Users Response")
def UserResponseData(request:Request,user_session_id:int,db: Session = Depends(get_db)):
    user_response_data = UserResponseService.getAllResponses(request=request,user_session_id=user_session_id,db=db)
    if user_response_data is not False:
        return ResponseSchema(response=msg['user_responses_found'], data=user_response_data)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])
