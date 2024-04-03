import json
import subprocess
from fastapi import APIRouter, Depends, Form,Request,Header
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from app.auth.auth_bearer import JWTBearer
from app.dto.configurations_schema import ConfigurationRequest
from app.models.roles import Role
from config.database import get_db, msg
from app.helper.general_helper import Helper
from app.modules.general.general_service import GeneralService
from app.dto.response_schema import ResponseSchema
import httpx

EXTERNAL_API_URL = "http://192.168.1.157:5000/"


router = APIRouter(prefix="/api", tags=["General"])

@router.get("/ethnicity_list",summary="Get Ethnicity List")
def ethnicityList(request:Request,db: Session = Depends(get_db)):
    ethnicity_list=GeneralService.ethnicityList(request=request,db=db)
    if ethnicity_list is not None and ethnicity_list!=[]:
        return ResponseSchema(response=msg['ethnicity_list'], data=ethnicity_list)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])
    
@router.get("/configurations",summary="Get Configurations")
def configurations(request:Request,db: Session = Depends(get_db)):
    configurations_data=GeneralService.configurations(request=request,db=db)
    if configurations_data is not None and configurations_data!={}:
        return ResponseSchema(response=msg['configuration_found'], data=configurations_data)
    else:
        return ResponseSchema(status=False,response=msg['something_went_wrong'])

@router.post("/update_configurations", summary="Update Configuration",dependencies=[Depends(JWTBearer())])
def updateConfigurations(configuration: ConfigurationRequest, db: Session = Depends(get_db)):
    update_configuration = GeneralService.update_configuration(configurations=configuration, db=db)
    if update_configuration is not False:
        return ResponseSchema(response=msg['configuration_updated'], data=update_configuration)
    else:
        return ResponseSchema(status= False,response=msg['no_record_found'], data=[])
    
@router.get("/roles",summary="Roles List Api", response_model=ResponseSchema)
def roles_list(db: Session = Depends(get_db)):
    roles = GeneralService.roles_list(db=db)
    if roles is not False:
        return ResponseSchema(response=msg['role_found'], data=roles)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'], data=[])
    

@router.get("/test_ext")
def get_my_data():
    curl_command = [
        "curl",
        "-X", "GET",
        f"{EXTERNAL_API_URL}"
    ]
     # Execute the curl command and capture the output
    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE)
    output= process.communicate()
    
    # Parse the JSON response
    # response_data = json.loads(output)
    return output
    
