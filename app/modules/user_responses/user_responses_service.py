import os
import subprocess
import traceback
from fastapi import APIRouter, Depends, File, Form, UploadFile, Request
from fastapi import Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session, load_only, joinedload, selectinload
from sqlalchemy import or_, func, and_
from config.database import get_db, msg
from app.helper.general_helper import Helper
from typing import Optional
from app.models.user_response import UserResponseModel
from app.models.user_sessions import UserSessionsModel
from app.models.ai_responses import AiResponsesModel
from app.models.questions import QuestionsModel
from fastapi_pagination import Params
from dotenv import load_dotenv
from datetime import datetime
from app.helper.general_helper import Helper
from jinja2 import Template
import random
import time

load_dotenv(verbose=True)


class UserResponseService:

    def add_user_response(request: Request, model_id: int = Form(), user_session_id: int = Form(), question_id: int = Form(), answer_id: int = Form(), response_video: UploadFile = File(None), db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
        try:
            response_video_path = None
            # response_audio_path = None
            # video_merging_file_path = None

            if response_video is not None:
                response_video_path = Helper.upload_file(
                    video=response_video, section=str(user_session_id),question_id=str(question_id))

            #For extrect Audio File Logic is Here.

            # if response_video is not None:
            #     response_audio_path = Helper.extractAudioFfmpeg(
            #         response_video_path, section=str(user_session_id))

            add_response = UserResponseModel(
                model_id=model_id,
                user_session_id=user_session_id,
                question_id=question_id,
                answer_id=answer_id,
                response_video=response_video_path,
                # response_audio=response_audio_path,
                created_at=datetime.now()
            )
            db.add(add_response)
            db.commit()
            return True
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def getAllResponses(request: Request, user_session_id: int, db: Session = Depends(get_db), uuid: str = Depends(Helper.user_session_header)):
        try:
            get_all_response = db.query(UserResponseModel).options(load_only(UserResponseModel.user_session_id, UserResponseModel.question_id, UserResponseModel.response_video),
                                                                   joinedload(UserResponseModel.question).options(load_only(QuestionsModel.id, QuestionsModel.question_text))).filter(UserResponseModel.user_session_id == user_session_id).order_by(UserResponseModel.question_id.asc()).all()

            get_ai_response=db.query(AiResponsesModel).filter(AiResponsesModel.user_session_id==user_session_id).first()

            for response in get_all_response:
                if response.response_video is not None:
                    response.response_video = os.path.join(
                        os.getenv('BASE_URL'), response.response_video)
            if get_ai_response is not None:
                get_all_response.append({"ai_response":get_ai_response.response_data})
            return get_all_response
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def sendToAI(request: Request, model_id: int = Form(), user_session_id: int = Form(), db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
        try:
            user=db.query(AiResponsesModel).filter(AiResponsesModel.user_session_id==user_session_id).first()
            if user is None:
                static_ai_response = ["You Are Very Depressed",
                                    "You Are Moderately Depressed",
                                    "Your Mental Health is Fit & Fine"]
                video_merging_file_path = Helper.video_merging(user_session_id)
                user_session = db.query(UserSessionsModel).filter(UserSessionsModel.id == user_session_id).first()
                user_session.session_video = video_merging_file_path
                user_session.is_completed = 1
                random_response = random.choice(static_ai_response)

                add_ai_response = AiResponsesModel(
                    model_id=model_id,
                    user_session_id=user_session_id,
                    response_data=random_response
                )
                db.add(add_ai_response)
                db.commit()
                db.refresh(add_ai_response)
                time.sleep(15)
                return add_ai_response
            return None

        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def sendMail(request: Request, background_tasks: BackgroundTasks, user_session_id: int = Form(), email: str = Form(), db: Session = Depends(get_db), uuid: int = Depends(Helper.user_session_header)):
        try:
            image_path=os.path.join(os.getenv('BASE_URL'), "uploads/email_image_1.png")
            print(image_path)
            questions_and_answers = []
            user_email = db.query(UserSessionsModel).filter(
                UserSessionsModel.id == user_session_id).first()
            user_responses = db.query(UserResponseModel).options(joinedload(UserResponseModel.user_answer)).options(
                joinedload(UserResponseModel.question)).filter(UserResponseModel.user_session_id == user_session_id).order_by(UserResponseModel.question_id.asc()).all()
            ai_response = db.query(AiResponsesModel).filter(
                AiResponsesModel.user_session_id == user_session_id).first()

            if user_email is not None:
                user_email.email = email
                db.commit()
            email_subject = "Mood Find Report"

            def generate_question_html(question_id, question, answer_video_link):
                download_icon_path = os.path.join(
                    os.getenv('BASE_URL'), "uploads/download_icn.png")
                question_html = f"""
                    <div>
                        
                        <p><b>{question_id}. </b>{question}</p>
                        <a href="{answer_video_link}" download>
                            &#x2B07; Download
                        </a>
                    </div>
                """
                return question_html

            # Initialize an empty list to store HTML for each question
            question_html_list = []

            # Loop through each user response and generate HTML for each question
            for user_response in user_responses:
                question = user_response.question.question_text
                # answer = user_response.user_answer.answer_text
                answer_video_link = os.path.join(
                    os.getenv('BASE_URL'), user_response.response_video)
                question_html = generate_question_html(
                    user_response.question_id,question, answer_video_link)
                question_html_list.append(question_html)

            # Construct the email body HTML
            email_body = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                        }}
                        .question-body{{
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            padding:10px
                        }}
                        .question-container {{
                            margin-bottom: 20px;
                            border: 1px solid #ccc;
                            padding: 10px;
                            border-radius: 5px;
                            background:#f7f7f7;
                        }}
                        .download-icon {{
                            width: 20px;
                            height: auto;
                        }}
                    </style>
                </head>
                <body class="question-body">
                    <h1>Mood Find Report</h1>
                    <p>Dear {email},</p>
                    <p>Based on the response we have received from you our findings suggest that {ai_response.response_data}</p>
                    <p>Please Find Below Mood Find Report:</p>
                    <img style="width: -webkit-fill-available; !important" src={image_path} alt="image">
                    <p>Your Responses:</p>
            """

            # Add generated HTML for each question to the email body
            for question_html in question_html_list:
                email_body += f"""
                    <div class="question-container">
                        <b>{question_html}</b>
                    </div>
                """
            # Close the email body HTML
            email_body += """
                <p>Thank You!<br><br>Mood Find Inc. </p>
                </body>
                </html>
            """
            tm = Template(f"{email_body}")
            message = tm.render(user_name="Human",
                                app_name="Mood Find Inc")
            Helper.send_mail(email_subject=email_subject, receipient_email=email,
                             email_body=message, background_tasks=background_tasks, db=db)
            return True
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
