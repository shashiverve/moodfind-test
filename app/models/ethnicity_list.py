from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
import os

class EthnicityListModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"ethnicity_master"
    id = Column(INTEGER, primary_key=True,index=True)
    ethnicity_name=Column(String(255),nullable=True)