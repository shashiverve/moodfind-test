from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,SMALLINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
from app.models.ethnicity_list import EthnicityListModel
import os


class UserSessionsModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"user_sessions"
    id = Column(INTEGER, primary_key=True,index=True)
    uuid=Column(String(255), nullable=True)
    model_id=Column(INTEGER,nullable=True)
    ethnicity_id=Column(INTEGER,nullable=True)
    other_ethnicity=Column(String(255),nullable=True)
    gender=Column(INTEGER,nullable=True)
    other_gender=Column(String(255),nullable=True)
    age=Column(INTEGER,nullable=True)
    email=Column(String(255),nullable=True)
    session_video=Column(String(255),nullable=True)
    user_agent=Column(String(255),nullable=True)
    device_type=Column(String(255),nullable=True)
    ip_address=Column(String(255),nullable=True)
    is_active=Column(SMALLINT,nullable=True)
    is_completed=Column(SMALLINT,nullable=True)
    created_at=Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    
    ethnicity = relationship(EthnicityListModel, backref=os.getenv("DB_PREFIX") + "user_sessions", primaryjoin='foreign(UserSessionsModel.ethnicity_id) == remote(EthnicityListModel.id)', lazy="select")

