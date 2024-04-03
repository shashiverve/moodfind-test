import uvicorn
from fastapi import FastAPI, Request,HTTPException
from config.database import engine, Base, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi_route_logger_middleware import RouteLoggerMiddleware
from sqlalchemy.event import listen
from fastapi.staticfiles import StaticFiles
from starlette import status
from fastapi_pagination import add_pagination
from app.modules.questions import questions_route
from app.modules.user_sessions import user_sessions_route
from app.modules.user_responses import user_responses_route
from app.modules.general import general_route
from app.modules.login import login_route
from app.modules.users import users_route
from app.modules.forgot_password import forgot_password_route
from app.modules.admin_view import admin_view_route
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
import warnings



app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = ["*"]

warnings.filterwarnings("ignore")

# Exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 400 and "UUID not provided in Header" in exc.detail:
        return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.detail,
            "data": None
        }
    
    )
    else:
        return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.detail,
            "data": None
        })


@app.exception_handler(RequestValidationError)
async def http_exception_accept_handler(request: Request, exc: RequestValidationError):
    error_wrapper: ErrorWrapper = exc.raw_errors[0]
    validation_error: ValidationError = error_wrapper.exc
    overwritten_errors = validation_error.errors()
    errMsg = ""
    for err in overwritten_errors:
        errMsg = err['msg'] if err['msg'] != None else None
    customResponse = {
        "status": True,
        "message": errMsg,
        "data": None,
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=customResponse,
    )




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def welcome():
    return "Welcome to Mood Finder Service"

app.include_router(login_route.router)
app.include_router(user_sessions_route.router)
app.include_router(users_route.router)
app.include_router(admin_view_route.router)
app.include_router(forgot_password_route.router)
app.include_router(general_route.router)
app.include_router(questions_route.router)
app.include_router(user_responses_route.router)


add_pagination(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host='192.168.1.67', port=7000, log_level="info", reload=True)
    print("running")
