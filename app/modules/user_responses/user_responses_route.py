from fastapi import APIRouter, Depends, File, Form, UploadFile, Request
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from app.helper.general_helper import Helper
from typing import Optional
from fastapi_pagination import Params
from app.modules.user_responses.user_responses_service import UserResponseService


router = APIRouter(prefix="/api/user_response", tags=["User Responses"])

#get All Response  of user
@router.get("/list/{user_session_id}",summary="Get all Response")
def getAllResponses(request:Request,user_session_id:int,db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
    all_responses=UserResponseService.getAllResponses(request=request,user_session_id=user_session_id,db=db,uuid=uuid)
    if all_responses is not False and all_responses !=[]:
        return ResponseSchema(response=msg['user_responses_found'], data=all_responses)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])

# route for the Add User Response
@router.post("/add", summary="Add User Response")
def addUserResponse(request:Request,model_id:int= Form(),user_session_id:int= Form(),question_id:int= Form(),answer_id:int= Form(None),response_video: UploadFile = File(None), db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
    add_user_response=UserResponseService.add_user_response(request=request,model_id=model_id,user_session_id=user_session_id,question_id=question_id,answer_id=answer_id,response_video=response_video,db=db,uuid=uuid)
    if add_user_response is True:
        return ResponseSchema(response=msg['user_response_saved'], data=None)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])

#user response send to AI
@router.post("/send_to_ai", summary="User Response Send To AI")
def sendToAI(request:Request,model_id:int= Form(),user_session_id:int= Form(),db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
    send_to_ai=UserResponseService.sendToAI(request=request,model_id=model_id,user_session_id=user_session_id,db=db,uuid=uuid)
    if send_to_ai is not None:
        return ResponseSchema(response=msg['user_response_sent'], data=send_to_ai.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])





# route for the Add User Response
@router.post("/send_mail", summary="Send User Response Email")
def sendMail(request:Request,background_tasks: BackgroundTasks,user_session_id:int=Form(),email:str=Form(),db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
    verify_mail=Helper.email_validation_helper(email)
    if verify_mail is True:
        send_details_email=UserResponseService.sendMail(request=request,background_tasks=background_tasks,user_session_id=user_session_id,email=email,db=db,uuid=uuid)
        if send_details_email is True:
            return ResponseSchema(response=msg['email_sent'], data=None)
        else:
            return ResponseSchema(status=False,response=msg['something_went_wrong'])
    else:
        return ResponseSchema(status=False,response=msg['invalid_email'])



