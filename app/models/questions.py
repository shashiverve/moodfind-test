from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
from app.models.answers import AnswersModel
import os

class QuestionsModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"questions"
    id = Column(INTEGER, primary_key=True,index=True)
    model_id=Column(INTEGER,nullable=True)
    question_text=Column(TEXT,nullable=True)
    question_audio=Column(String(255),nullable=True)

    answer=relationship(AnswersModel, backref=os.getenv("DB_PREFIX")+"questions",primaryjoin='foreign(QuestionsModel.id) == remote(AnswersModel.question_id)', lazy="select",uselist=True)
    
    