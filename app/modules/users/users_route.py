from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.response_schema import ResponseSchema
from app.modules.users.users_service import UserService
from typing import Optional
from fastapi_pagination import Params
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/api/admin/users", tags=["Admin"],dependencies=[Depends(JWTBearer())])

# route for the get all users
@router.get("/list", summary="Get All Users")
def getAllUser(params: Params = Depends(),search_string:Optional[str]=None,sort_by: Optional[str] = None,sort_direction: Optional[str] = None,db: Session = Depends(get_db)):
    users = UserService.list_user(params=params, search_string=search_string, sort_by=sort_by, sort_direction=sort_direction, db=db)
    if users is not False:
        return ResponseSchema(response=msg['user_list_generate'], data=users)
    else:
        return ResponseSchema(status=False,response=msg['no_record_found'])


# route for the get particuler user by Id
@router.get("/view/{userid}", summary="Get User By ID")
def getUser(userid: int, db: Session = Depends(get_db)):
    particular_user = UserService.get_user(userid=userid, db=db)
    if particular_user is not False:
        return ResponseSchema(response=msg['user_found'], data=particular_user.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['user_not_found'], data=[])

# route for the createing New User
@router.post("/add", summary="Create User")
def createUser(picture: UploadFile = File(None), name: str = Form(), email: str = Form(), password: str = Form(), contact_number: str = Form(None), address: str = Form(None), city: str = Form(None), state: str = Form(None), zip_code: str = Form(None), roles: str = Form(),db: Session = Depends(get_db)):
    create_user = UserService.create_user(picture=picture, name=name, email=email, password=password, contact_number=contact_number, address=address, city=city, state=state, zip_code=zip_code,roles=roles, db=db)
    if create_user is not False:
        return ResponseSchema(response=msg['user_created'], data=create_user.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['user_already_exists'])

# route for the Updating User
@router.put("/{userid}", summary="Update User")
def updateUser(userid: int, picture: UploadFile = File(None), name: str = Form(None), email: str = Form(None), contact_number: str = Form(None), address: str = Form(None), city: str = Form(None), state: str = Form(None), zip_code: str = Form(None), roles: str = Form(None), is_remove: int = Form(None), password: str = Form(None), c_password: str = Form(None),db: Session = Depends(get_db)):
    update_user = UserService.update_user(userid=userid, name=name, email=email, contact_number=contact_number, address=address, city=city, state=state, zip_code=zip_code, picture=picture,  roles=roles, is_remove=is_remove, password=password, c_password=c_password, db=db)
    if update_user is not False:
        return ResponseSchema(response=msg['user_updated'], data=update_user.__dict__)
    else:
        return ResponseSchema(status=False,response=msg['user_already_exists'])

# route for the Deleting User
@router.delete("/{userid}", summary="Delete User")
def deleteUser(userid: int, db: Session = Depends(get_db)):
    delete_user = UserService.delete_user(userid=userid, db=db)
    if delete_user is not False:
        return ResponseSchema(response=msg['user_deleted'])
    else:
        return ResponseSchema(status=False,response=msg['user_not_found'])