from datetime import datetime
import traceback
from fastapi import Depends, File, Form, UploadFile, Request,Header
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import desc, func, or_
from app.dto.user_sessions import UserSessionsSchema
from app.models.user_response import UserResponseModel
from config.database import get_db, msg
from dotenv import load_dotenv
from app.dto.response_schema import ResponseSchema
from app.models.user_sessions import UserSessionsModel
from app.helper.general_helper import Helper
from typing import Annotated
import os
import uuid

load_dotenv(verbose=True)

class UserSessionsService:

    def createUserSessions(request:Request,user_session:UserSessionsSchema, db: Session = Depends(get_db)):
    
        try:
            add_user_session=UserSessionsModel(
                uuid=uuid.uuid4(),
                model_id=1,
                ethnicity_id=user_session.ethnicity_id,
                other_ethnicity=user_session.other_ethnicity,
                gender=user_session.gender,
                other_gender=user_session.other_gender,
                age=user_session.age,
                user_agent=request.headers.get("user-agent"),
                device_type=user_session.device_type,
                ip_address=request.client.host,
                is_active=1,
                is_completed=0,
                created_at =datetime.now()
            )
            db.add(add_user_session)
            db.commit()
            db.refresh(add_user_session)

            return add_user_session
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def checkSession(request:Request,Uuid: Annotated[str | None, Header()],db: Session = Depends(get_db)):
        try:
            check_session=db.query(UserSessionsModel).filter(UserSessionsModel.uuid==Uuid).first()
            if check_session is not None:
                is_answer_given=db.query(UserResponseModel).filter(UserResponseModel.user_session_id==check_session.id).first()
                if is_answer_given is not None:
                    add_new_session=UserSessionsModel(
                        uuid=uuid.uuid4(),
                        model_id=check_session.model_id,
                        ethnicity_id=check_session.ethnicity_id,
                        gender=check_session.gender,
                        age=check_session.age,
                        user_agent=request.headers.get("user-agent"),
                        device_type=check_session.device_type,
                        ip_address=request.client.host,
                        is_active=1,
                        is_completed=0,
                        created_at =datetime.now()
                    )
                    db.add(add_new_session)
                    check_session.is_active=0
                    db.commit()
                    db.refresh(add_new_session)
                    return add_new_session.__dict__
                return 1
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    def SaveUserSessionVideo(request:Request,user_session_id:int=Form(),session_video: UploadFile = File(None),db: Session = Depends(get_db),uuid: str = Depends(Helper.user_session_header)):
        try:
            get_user_session=db.query(UserSessionsModel).filter(UserSessionsModel.id==user_session_id).first()
            video_path=""
            video_path=Helper.upload_file(video=session_video,section=str(user_session_id))
            if session_video is not None:
                get_user_session.session_video=video_path
                db.commit()
                get_user_session.session_video=os.path.join(os.getenv('BASE_URL'), get_user_session.session_video)

            return get_user_session
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)