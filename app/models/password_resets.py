from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BIGINT, BOOLEAN, text
from sqlalchemy.orm import relationship
from config.database import Base
import os


class PasswordReset(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"password_resets"
    id = Column(INTEGER, primary_key=True,index=True)
    email=Column(String(255),nullable=False)
    token=Column(String(255),nullable=True)
    otp=Column(INTEGER,nullable=False)
    is_verified=Column(BOOLEAN,nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    