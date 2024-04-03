from sqlalchemy import Column, INTEGER, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from app.models.roles import Role
from config.database import Base
import os

class User(Base):
    __tablename__ = os.getenv("DB_PREFIX")+"users"
    id = Column(INTEGER, primary_key=True,index=True)
    name = Column(String(50), nullable=False)
    email= Column(String(255), nullable=False)
    email_verified_at =  Column(TIMESTAMP,nullable=True)
    password = Column(String(255), nullable=True)
    contact_number = Column(String(50), nullable=True)
    address = Column(String(555), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(50), nullable=False)
    remember_token = Column(String(100), nullable=True)
    picture = Column(String(555), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True,server_default=text("NULL"))
    created_at = Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Accessor for picture_url
    @hybrid_property
    def picture_url(self):
        if self.picture:
            return f"{os.getenv('BASE_URL')}{self.picture}"
        else:
            return None


    roles = relationship(Role, secondary=os.getenv("DB_PREFIX") + "user_has_roles",
                              backref=os.getenv("DB_PREFIX") + "users",
                                  primaryjoin='foreign(User.id) == remote(UserHasRole.user_id)',
                              secondaryjoin='foreign(Role.id) == remote(UserHasRole.role_id)',
                              lazy="select")