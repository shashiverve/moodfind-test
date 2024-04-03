from ast import Str
from datetime import datetime
from fastapi import Depends, File, Form, UploadFile
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import desc, func, or_
from config.database import get_db, msg
from app.models.users import User
from app.models.roles import Role
from app.helper.general_helper import Helper
from app.models.user_has_roles import UserHasRole
from typing import Optional
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.hashing.pw_hashing import Hash
from dotenv import load_dotenv
from app.dto.response_schema import ResponseSchema
import os


load_dotenv(verbose=True)

class UserService:
    # Get all Users List using this  Function
    def list_user(params: Params,search_string: Str,sort_by: Optional[str], sort_direction: Optional[str] ,db: Session):
        try:
            all_user = db.query(User).options(load_only(User.id, User.name, User.city, User.state, User.email, User.contact_number, User.picture, User.address, User.zip_code,User.created_at),
                                            joinedload(User.roles).options(load_only(Role.id, Role.name)))

             # Sort_by and sort_direction both logic here
            if sort_direction == "desc":
                all_user = all_user.order_by(User.__dict__[sort_by].desc())
            elif sort_direction == "asc":
                all_user = all_user.order_by(User.__dict__[sort_by].asc())
            else:
                all_user = all_user.order_by(User.id.asc())

            if search_string:
                all_user = all_user.filter(or_(
                    User.name.like('%'+search_string+'%'),
                    User.email.like('%'+search_string+'%'),
                    User.contact_number.like('%' + search_string + '%'),
                    User.roles.any(Role.name.like('%' + search_string + '%'))
                ))

            users = paginate(all_user, params)
            for i in users.__dict__['items']:
                # Below code is add the image_url variable in user object
                if i.picture is not None and os.getenv('BASE_URL') not in i.picture:
                                i.picture = os.path.join(os.getenv('BASE_URL'), i.picture) if i.picture else None

            return users
        except Exception as e:
            print(str(e))
            return False
        
    # Get all Particuler Users  using this  Function
    def get_user(userid: int, db: Session = Depends(get_db)):
        try:
            user = db.query(User).options(
                joinedload(User.roles).options(load_only(Role.id, Role.name))
            ).filter(User.id == userid).first()

            if not user == None:
                # Below function is add the image_url variable in user object
                if user.picture is not None and os.getenv('BASE_URL') not in user.picture:
                        user.picture = os.path.join(os.getenv('BASE_URL'), user.picture) if user.picture else None    
                del user.__dict__['password'], user.__dict__['email_verified_at'], user.__dict__['remember_token'], user.__dict__['deleted_at']
                return user
            else:
                return False
        except Exception as e:
            return False

    # Create User using this Function
    def create_user(picture: UploadFile = File(None), name: str = Form(), email: str = Form(), password: str = Form(), contact_number: str = Form(), address: str = Form(None), city: str = Form(None), state: str = Form(None), zip_code: str = Form(), roles: str = Form(), db: Session = Depends(get_db)):
        try:
            file_location = None
            if picture:
                file_location = Helper.upload_file_image(image=picture,section="profile_image")
                if file_location == "upload_error":
                    return ResponseSchema(response=msg['failed_to_upload_image'])

            use_exist = db.query(User).filter(User.email == email).first()
            if use_exist is None:
                db_user = User(
                    name=name,
                    email=email,
                    password=Hash.bcrypt(password),
                    contact_number=contact_number,
                    address=address,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    picture=file_location,
                    created_at=datetime.now()
                )
                db.add(db_user)
                db.commit()
                updated_db_user = db.query(User).filter(User.email == email).order_by(User.email.desc()).first()
                user_roles = roles.split(',')
                for i in user_roles:
                    db_user_group = UserHasRole(
                        user_id=updated_db_user.__dict__['id'], role_id=i)
                    db.add(db_user_group)
                db.commit()
                updated_user_data = db.query(User).options(load_only(User.id, User.name, User.city, User.state, User.email, User.contact_number, User.picture)).filter(User.email == email).order_by(User.email.desc()).first()
                user_groups = db.query(UserHasRole.role_id).filter(UserHasRole.user_id == updated_user_data.__dict__['id']).all()
                user_groups_ids = []
                for value in user_groups:
                    user_groups_ids.append(value[0])
                group = db.query(Role.id, Role.name).filter(Role.id.in_(user_groups_ids)).all()

                # Below function is add the image_url variable in user object
                if updated_user_data.picture is not None and os.getenv('BASE_URL') not in updated_user_data.picture:
                        updated_user_data.picture = os.path.join(os.getenv('BASE_URL'), updated_user_data.picture) if updated_user_data.picture else None

                updated_user_data.__dict__['roles'] = group
                return updated_user_data
            else:
                return False
        except Exception as e:
            print(e)
            return False

        
    # Update Particuler User using this function
    def update_user(userid: int, picture: UploadFile = File(None), name: str = Form(None), email: str = Form(None), contact_number: str = Form(None), address: str = Form(None), city: str = Form(None), state: str = Form(None), zip_code: str = Form(None), roles: str = Form(None), is_remove: int = Form(None), password: str = Form(None), c_password: str = Form(None),project_ids:str=Form(None), db: Session = Depends(get_db)):
        try:
            user_exist = db.query(User).filter(User.email == email, User.id != userid).first()
            if user_exist is None:
                db_userid = db.query(User).filter(User.id == userid).first()
                # user save code
                if not db_userid == None:
                    db_userid.name = db_userid.name if name == None else name
                    db_userid.email = db_userid.email if email == None else email
                    db_userid.contact_number = contact_number
                    db_userid.address = address
                    db_userid.city = city
                    db_userid.state = state
                    db_userid.zip_code = zip_code
                    db_userid.updated_at = datetime.now()


                    # user image save
                    updated_image_path = ""
                    if picture:
                        if db_userid.picture == "" or db_userid.picture == None:
                            pass
                        else:
                            if os.path.exists(os.path.join(os.getcwd(), db_userid.picture)):
                                os.remove(os.path.join(os.getcwd(), db_userid.picture))

                        updated_image_path = Helper.upload_file_image(image=picture, section='profile_image')
                        db_userid.picture = updated_image_path
                        if updated_image_path == "":
                            return False

                    if is_remove == 1:
                        db_userid.picture = None

                    if password:
                        db_userid.password = Hash.bcrypt(c_password)

                    db.commit()

                    # user groups save agaist user

                    if roles is not None:
                        db_user_group = db.query(UserHasRole).filter(
                        UserHasRole.user_id == userid).delete()
                        db.commit()
                        update_user_roles = roles.split(',')
                        for i in update_user_roles:
                            db_user_group = UserHasRole(user_id=db_userid.id, role_id=i)
                            db.add(db_user_group)
                            db.commit()

                    updated_db_userid = db.query(User).options(
                joinedload(User.roles).options(load_only(Role.id, Role.name))
            ).filter(User.id == userid).first()

                    # Below function is add the image_url variable in user object
                    if updated_db_userid.picture is not None and os.getenv('BASE_URL') not in updated_db_userid.picture:
                                updated_db_userid.picture = os.path.join(os.getenv('BASE_URL'), updated_db_userid.picture) if updated_db_userid.picture else None

                    del updated_db_userid.password, updated_db_userid.email_verified_at, updated_db_userid.remember_token, updated_db_userid.deleted_at
                    return updated_db_userid
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(str(e))
            return False

    # Delete particuler User using This Function
    def delete_user(userid: int, db: Session):
        try:
            db_userid = db.query(User).options(load_only(
                User.id, User.name, User.city, User.state, User.email, User.contact_number, User.picture)).filter(User.id == userid).first()
            
            if db_userid is not None:
                if db_userid.picture is not None or db_userid.picture != "":
                    if os.path.exists(f"{os.getcwd()}/{db_userid.picture}") == True:
                        os.remove(f"{os.getcwd()}/{db_userid.picture}")

                db_delete_user_has_user_group = db.query(UserHasRole).filter(UserHasRole.user_id == db_userid.id).delete()
                db.commit()
                db.delete(db_userid)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            print('An exception occurred', str(e))
            return False