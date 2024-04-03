import traceback
from fastapi import APIRouter, Depends, File, Form, UploadFile, Request
from sqlalchemy.orm import Session, load_only, joinedload
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from typing import Optional
from fastapi_pagination import Params
from app.helper.general_helper import Helper
from app.models.questions import QuestionsModel
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

class QuestionsService:

    def list_questions(db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
        try:
            list_questions=db.query(QuestionsModel).options(joinedload(QuestionsModel.answer)).all()
            for question in list_questions:
                if question.question_audio is not None:
                    question.question_audio=os.path.join(os.getenv('BASE_URL'), question.question_audio)
            return list_questions
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def getQuestionByID(question_id:int,db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
        try:
            question=db.query(QuestionsModel).options(joinedload(QuestionsModel.answer)).filter(QuestionsModel.id==question_id).first()
            if question is not None:
                question.question_audio=os.path.join(os.getenv('BASE_URL'), question.question_audio)
            return question
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)