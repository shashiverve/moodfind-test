from fastapi import APIRouter, Depends, File, Form, UploadFile, Request
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from typing import Optional
from fastapi_pagination import Params
from app.helper.general_helper import Helper
from app.modules.questions.questions_service import QuestionsService


router = APIRouter(prefix="/api/questions", tags=["Questions"],dependencies=[Depends(Helper.user_session_header)])

# route for the get all Questions
@router.get("/list", summary="Get All Questions")
def getAllQuestions(db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
    questions = QuestionsService.list_questions(db=db,uuid=uuid)
    if questions is not False and questions !=[]:
        return ResponseSchema(response=msg['question_list_found'], data=questions)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])

# route for the get Questions by Id
@router.get("/{question_id}", summary="Get Questions By Id")
def getQuestionByID(question_id:int,db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
    question = QuestionsService.getQuestionByID(question_id=question_id,uuid=uuid,db=db)
    if question is not None:
        return ResponseSchema(response=msg['question_found'], data=question.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])
