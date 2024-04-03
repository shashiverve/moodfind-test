from sqlalchemy import Column, INTEGER
from config.database import Base
import os

class UserHasRole(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"user_has_roles"
    id = Column(INTEGER, primary_key=True,index=True)
    user_id = Column(INTEGER, nullable=False)
    role_id=Column(INTEGER, nullable=False)
