from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text
from config.database import Base
import os

class Role(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"roles"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # users = relationship("UserHasUserGroup", back_populates="user_group")