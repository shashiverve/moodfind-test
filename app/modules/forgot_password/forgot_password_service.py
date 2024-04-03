from fastapi import Depends,BackgroundTasks,Request
from config.database import get_db, response, msg
from app.dto.response_schema import ResponseSchema
from app.models.password_resets import PasswordReset
from app.models.configurations import ConfigurationsModel
from app.dto.change_password_schema import VerifyForgotPasswordOTPSchema, ChangePasswordSchema, SentForgotPasswordOTPSchema
from sqlalchemy.orm import Session, load_only, joinedload
from app.models.users import User
from datetime import datetime
from app.helper.general_helper import Helper
from app.hashing.pw_hashing import Hash
from jinja2 import Template
from jinja2 import Template
from jinja2 import Template
# from app.helper.audit_helper import AuditHelper

class ForgotPasswordService():
    
    # Services for the SEND OTP to the user
    def send_forgot_password_otp(request:Request,background_tasks: BackgroundTasks, otp_sent: SentForgotPasswordOTPSchema, db: Session = Depends(get_db)):
        if(Helper.email_validation_helper(emailVal=otp_sent.email)):
            user = db.query(User).options(load_only(User.email)).filter(User.email == otp_sent.email).first()
            if user is None:
                return 3
  

            get_email_obj = db.query(ConfigurationsModel).options(load_only(ConfigurationsModel.id, ConfigurationsModel.config_key, ConfigurationsModel.config_value)).all()
            
            email_subject = None
            email_body = None
            for key in get_email_obj:
                if key.__dict__['config_key'] == "sent_otp_to_user_subject":
                    email_subject = key.__dict__['config_value']
                elif key.__dict__['config_key'] == "sent_otp_to_user_body":
                    email_body = key.__dict__['config_value']
            
            # Generate the random OTP
            OTP_Generate = Helper.generate_otp()

            # Below code to add a add into password reset table
            add_todb = PasswordReset(
                email=user.email,
                otp=OTP_Generate,
                is_verified=0,
                created_at=datetime.now()
            )
            db.add(add_todb)
            db.commit()

            #  below code to send a email to recipient
            tm = Template(f"{email_body}")
            message = tm.render(user_name=user.name, OTP=OTP_Generate, app_name="Mood Find Inc.")
            Helper.send_mail(email_subject=email_subject, receipient_email=user.email, email_body=message, background_tasks=background_tasks, db=db)

            if add_todb is not False:
                return 1
            return 2
        return False


    # Services for the Verify forget Password OTP
    def verify_forgot_password_otp(verifyOtp: VerifyForgotPasswordOTPSchema, db: Session = Depends(get_db)):
        try:
            check_otp=0
            if(Helper.email_validation_helper(emailVal=verifyOtp.email)):
                check_otp = db.query(PasswordReset).filter(PasswordReset.email == verifyOtp.email).order_by(PasswordReset.id.desc()).first()
                if check_otp:
                    if check_otp.__dict__['is_verified'] == False:
                        if check_otp.__dict__['otp'] == verifyOtp.otp:
                            check_otp.is_verified = True
                            db.commit()
                        else:
                            check_otp = 1
                else:
                    check_otp = 2
            else:
                check_otp = 3
            return check_otp
        except Exception as e:
            return False

    # After verify OTP user can change the New Password 
    def user_change_password(passwordVal: ChangePasswordSchema, db: Session = Depends(get_db)):
        if(Helper.email_validation_helper(emailVal=passwordVal.email)):
            get_db_user = db.query(User).filter(User.email == passwordVal.email).first()
            if get_db_user:
                get_db_user.password = Hash.bcrypt(passwordVal.password)
                db.commit()
                db.refresh(get_db_user)
                return ResponseSchema(response=msg['password_changed'])
            return ResponseSchema(response=msg['user_with_email_invalid'])
        return ResponseSchema(response=msg['email_invalid'])
