from fastapi import APIRouter, Depends, BackgroundTasks,Request
from sqlalchemy.orm import Session
from config.database import get_db, msg
from app.dto.change_password_schema import ChangePasswordSchema, VerifyForgotPasswordOTPSchema, SentForgotPasswordOTPSchema
from app.modules.forgot_password.forgot_password_service import ForgotPasswordService
from app.dto.response_schema import ResponseSchema

router = APIRouter(prefix="/api/forgot_password", tags=["Forgot PassWord"])

# Router for SEND OTP via Email
@router.post("/otp_sent",summary="Send forgot password OTP")
def sendForgotPasswordOTP(request:Request,otp_sent: SentForgotPasswordOTPSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db), ):
    send_otp=ForgotPasswordService.send_forgot_password_otp(request=request,otp_sent=otp_sent, background_tasks=background_tasks,db=db)
    if send_otp ==1:
        return ResponseSchema(response=msg['otp_sent'])
    elif send_otp == 2:
        return ResponseSchema(status=False,response=msg['email_invalid'])
    elif send_otp == 3:
        return ResponseSchema(status=False, response=msg['user_with_email_invalid'])

# Router for verify OTP
@router.post("/otp_verify",summary="Verify forgot password OTP")
def VerifyForgotPasswordOTP(verifyOtp: VerifyForgotPasswordOTPSchema, db: Session = Depends(get_db)):
    verify_otp = ForgotPasswordService.verify_forgot_password_otp(verifyOtp=verifyOtp, db=db)
    if type(verify_otp) != int:
        return ResponseSchema(response=msg['otp_verified'], data=verify_otp.__dict__)
    else:
        if verify_otp == 1:
            return ResponseSchema(status=False, response=msg['invalid_otp'])
        elif verify_otp == 2:
            return ResponseSchema(status=False, response=msg['user_with_email_invalid'])
        elif verify_otp == 3:
            return ResponseSchema(status=False, response=msg['email_invalid'])

# Router for the Change Password
@router.post("/change_password", summary="Change user password")
def UserChangePassword(passwordVal: ChangePasswordSchema, db: Session = Depends(get_db)):
    change_password = ForgotPasswordService.user_change_password(passwordVal=passwordVal, db=db)
    return change_password
