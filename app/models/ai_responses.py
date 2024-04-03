from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
import os

class AiResponsesModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"ai_responses"
    id = Column(INTEGER, primary_key=True,index=True)
    model_id=Column(INTEGER,nullable=True)
    user_session_id=Column(INTEGER,nullable=True)
    response_data=Column(String(255),nullable=True)

    created_at=Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))