from ast import Str
from datetime import datetime
from fastapi import Depends, File, Form, UploadFile
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import desc, func, or_
from config.database import get_db, msg
from app.models.user_sessions import UserSessionsModel
from app.models.ethnicity_list import EthnicityListModel
from typing import Optional
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.hashing.pw_hashing import Hash
from dotenv import load_dotenv
import os
import httpx




load_dotenv(verbose=True)

class AdminViewService:
    # Get all Users List using this  Function
    def getAllUserResponseData(params: Params,search_string: Str,sort_by: Optional[str], sort_direction: Optional[str] ,db: Session):
        try:
            all_users_response = db.query(UserSessionsModel).options(load_only(UserSessionsModel.id, UserSessionsModel.age, UserSessionsModel.device_type, UserSessionsModel.ethnicity_id, UserSessionsModel.email, UserSessionsModel.gender,UserSessionsModel.is_completed),
                                            joinedload(UserSessionsModel.ethnicity).options(load_only(EthnicityListModel.id, EthnicityListModel.ethnicity_name)))

             # Sort_by and sort_direction both logic here
            if sort_direction == "desc":
                all_users_response = all_users_response.order_by(UserSessionsModel.__dict__[sort_by].desc())
            elif sort_direction == "asc":
                all_users_response = all_users_response.order_by(UserSessionsModel.__dict__[sort_by].asc())
            else:
                all_users_response = all_users_response.order_by(UserSessionsModel.id.asc())

            if search_string:
                all_users_response = all_users_response.filter(or_(
                    UserSessionsModel.age==(search_string),
                    UserSessionsModel.email.like('%'+search_string+'%'),
                    UserSessionsModel.device_type.like('%'+search_string+'%'),
                    UserSessionsModel.gender==(search_string),
                    UserSessionsModel.ethnicity.has(EthnicityListModel.ethnicity_name.like('%' + search_string + '%')),
                
                ))

            users_response = paginate(all_users_response, params)

            return users_response
        except Exception as e:
            print(str(e))
            return False