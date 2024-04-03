import os
from fastapi import APIRouter, Depends,Request,Header
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import desc, func, or_, and_
from app.dto.configurations_schema import ConfigurationRequest
from app.models.roles import Role
from config.database import get_db
from app.helper.general_helper import Helper
from typing import Annotated, Optional
from app.models.user_sessions import UserSessionsModel
from app.models.user_response import UserResponseModel
from app.models.ethnicity_list import EthnicityListModel
from app.models.configurations import ConfigurationsModel
import traceback
import json
from uuid import uuid4
from datetime import datetime



class GeneralService:

    def ethnicityList(request:Request,db: Session = Depends(get_db)):
        try:
            ethnicity_list=db.query(EthnicityListModel).all()
            return ethnicity_list
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    def configurations(request:Request,db: Session = Depends(get_db)):
        try:
            configurations_data=db.query(ConfigurationsModel).filter(ConfigurationsModel.config_type==2).all()
            general_configurations = {configuration.__dict__['config_key']: configuration.__dict__['config_value'] for
                           configuration in
                           configurations_data}
            general_configurations['is_question_read_out']=int(general_configurations['is_question_read_out'])
            general_configurations['demo_video_url']= os.path.join(os.getenv('BASE_URL'), general_configurations['demo_video_url'])
            return general_configurations
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    
    def roles_list(db: Session = Depends(get_db)):
        try:
            roles = db.query(Role).options(load_only(Role.id, Role.name)).all()

            if roles is not False:
                return roles
            else:
                return False
        except Exception as e:
            return False


    def update_configuration(configurations: ConfigurationRequest, db: Session = Depends(get_db)):
            try:
                for (key, value) in configurations.__dict__.items():
                    db_configuration = db.query(ConfigurationsModel).filter(ConfigurationsModel.config_key == key,ConfigurationsModel.config_type==2).first()
                    if db_configuration.config_value != value:
                        db_configuration.config_value = value
                        db_configuration.updated_at = datetime.now()
                        db.commit()
                configurations_datas = db.query(ConfigurationsModel).options(load_only(ConfigurationsModel.id, ConfigurationsModel.config_key, ConfigurationsModel.config_value)).filter(ConfigurationsModel.config_type==2).all()
                result = {configurations_data.__dict__['config_key']: configurations_data.__dict__['config_value'] for configurations_data in configurations_datas}
                return result
            except Exception as e:
                print(str(e))
                return False
