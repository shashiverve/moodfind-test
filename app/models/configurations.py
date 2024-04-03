from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey,TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from config.database import Base
import os

class ConfigurationsModel(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"configurations"
    id = Column(INTEGER, primary_key=True,index=True)
    config_key=Column(String(555),nullable=False)
    config_value=Column(TEXT,nullable=False)
    config_type=Column(INTEGER,nullable=False)	