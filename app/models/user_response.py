from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from app.models.questions import QuestionsModel
from app.models.answers import AnswersModel

from config.database import Base
import os

class UserResponseModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"user_responses"
    id = Column(INTEGER, primary_key=True,index=True)
    model_id=Column(INTEGER,nullable=True)
    user_session_id=Column(INTEGER,nullable=True)
    question_id=Column(INTEGER,nullable=True)
    answer_id=Column(INTEGER,nullable=True)
    response_video=Column(String(255),nullable=True)
    response_audio=Column(String(255),nullable=True)
    response_text=Column(String(255),nullable=True)
    created_at=Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    
    question=relationship(QuestionsModel, backref=os.getenv("DB_PREFIX")+"user_responses",primaryjoin='foreign(UserResponseModel.question_id) == remote(QuestionsModel.id)', lazy="select")
    
    user_answer=relationship(AnswersModel, backref=os.getenv("DB_PREFIX")+"user_responses",primaryjoin='foreign(UserResponseModel.answer_id) == remote(AnswersModel.id)', lazy="select")
