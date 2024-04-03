from fastapi import APIRouter, Depends, File, Form, UploadFile, Request,Header
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from app.modules.user_sessions.user_sessions_service import UserSessionsService
from app.helper.general_helper import Helper
from app.dto.user_sessions import UserSessionsSchema
from typing import Optional,Annotated
from fastapi_pagination import Params


router = APIRouter(prefix="/api/user_sessions", tags=["Users Sessions"])

# route for the createing New User Sessions
@router.post("/add", summary="Create User Sessions")
def createUserSessions(request:Request,user_session:UserSessionsSchema, db: Session = Depends(get_db)):
    create_user_sessions=UserSessionsService.createUserSessions(request=request,user_session=user_session,db=db)
    if create_user_sessions is not None:
        return ResponseSchema(response=msg['user_created'], data=create_user_sessions.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])

# route for the User Sessions Video Save
@router.post("/save_video", summary="Save Sessions Video")
def UserSessionsSaveVideo(request:Request,user_session_id:int=Form(),session_video: UploadFile = File(None), db: Session = Depends(get_db),uuid: str = Depends(Helper.user_session_header)):
    save_user_session_video=UserSessionsService.SaveUserSessionVideo(request=request,user_session_id=user_session_id,session_video=session_video,db=db,uuid=uuid)
    if save_user_session_video is not None:
        return ResponseSchema(response=msg['session_video_saved'], data=save_user_session_video.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])

@router.post("/check_session",summary="Check User Session")
def checkSession(request:Request,Uuid: Annotated[str | None, Header()],db: Session = Depends(get_db)):
    check_session=UserSessionsService.checkSession(request=request,Uuid=Uuid,db=db)
    if type(check_session)==int and check_session is not 0 and check_session is not None:
        check_session={"old_uuid":Uuid}
        return ResponseSchema(status=False,response=msg['old_session'], data=check_session)
    if type(check_session)==dict and  check_session is not None:
        return ResponseSchema(response=msg['new_session'], data=check_session)

