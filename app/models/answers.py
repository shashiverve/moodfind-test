from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
import os

class AnswersModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"answers"
    id = Column(INTEGER, primary_key=True,index=True)
    question_id=Column(INTEGER,nullable=True)
    model_id=Column(INTEGER,nullable=True)
    answer_text=Column(TEXT,nullable=True)