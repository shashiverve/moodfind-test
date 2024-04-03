from fastapi import Depends, File, Form, UploadFile, BackgroundTasks, Request, Header,HTTPException
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from sqlalchemy import Integer
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Annotated
from sqlalchemy.orm import Session, load_only, joinedload, class_mapper
from sqlalchemy import or_, func, and_
from app.auth.auth_handler import signJWT
from app.dto.login_schema import LoginSchema
from app.hashing.pw_hashing import Hash
from app.models.roles import Role
from app.models.users import User
from dotenv import load_dotenv
from config.database import get_db
from app.models.user_sessions import UserSessionsModel
from app.models.configurations import ConfigurationsModel
from moviepy.video.io.VideoFileClip import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import os
import subprocess
import traceback
import re
import random

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

load_dotenv(verbose=True)
class Helper:
    def user_login(request: LoginSchema, db: Session = Depends(get_db)):
        try:
            user = db.query(User).options(load_only(User.id, User.name, User.city, User.state, User.email, User.contact_number, User.picture, User.address, User.zip_code, User.created_at),
                                        joinedload(User.roles).options(load_only(Role.id, Role.name))
                                          ).filter(or_(User.name == request.user_name, User.email == request.user_name)).first()



            if user:
                if not Hash.verify(request.password, user.password):
                    return False

                # Generate token using below method
                token_data = signJWT(request.user_name)
                user.__dict__['token']= signJWT(request.user_name)['access_token']
                user.__dict__['picture_url'] = user.picture_url

                del user.password
            return user
        except Exception as e:
            print(str(e))
            return False

    def generate_otp():
        try:
            otp_genrate = random.randint(000000, 999999)
            if len(str(otp_genrate)) < 6:
                otp_genrate = random.randint(000000, 999999)
            return otp_genrate
        except Exception as e:
            print(str(e))
            return False

    def user_session_header(request: Request, Uuid: Annotated[str | None, Header()] = None, db: Session = Depends(get_db)):
        try:
            if Uuid is None:
                raise HTTPException(status_code=400, detail="UUID not provided in Header")
            
            user = db.query(UserSessionsModel).filter(UserSessionsModel.uuid == Uuid).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User Session not found")
            
            return user.uuid
            
        except HTTPException:
            raise 
       
                
    def upload_file_image(image: UploadFile, section: Optional[str] = None):
        file_location =""
        try:
            upload_path = os.path.join(os.getcwd(), 'uploads', section) if section is not None else os.path.join(os.getcwd(), 'uploads')
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            timestamp = datetime.timestamp(datetime.now())
            final_timestamp = str(timestamp).split('.')
            change_filename = image.filename.split('.')
            final_filename = change_filename[0]
            if change_filename[-1] == "jpeg" or change_filename[-1] == "jpg" or change_filename[-1] == "png" or change_filename[-1] == "JPEG" or change_filename[-1] == "JPG" or change_filename[-1] == "PNG":
                final_filename = f"{os.path.basename(section)}_{final_timestamp[0]}.{change_filename[-1]}" if section is not None else f"{final_timestamp[0]}.{change_filename[-1]}"
                file_location = f"uploads/{section}/{final_filename}"
                with open(file_location, "wb+") as file_object:
                    file_object.write(image.file.read())
                return file_location
        except Exception as e:
            print(str(e))
            return file_location
    
    #Question_id wise Save Videos logic is here
    
    # def upload_file(video: UploadFile, section: Optional[str] = None,question_id: Optional[str] = None):
    #     file_location =""
    #     try:
    #         upload_path = os.path.join(os.getcwd(), 'uploads', f"{section}") if section is not None else os.path.join(os.getcwd(), 'uploads')
    #         if not os.path.exists(upload_path):
    #             os.mkdir(upload_path)
    #             os.chmod(upload_path, 0o777)
    #         video_dir = os.path.join(upload_path,"videos")
    #         if not os.path.exists(video_dir):
    #             os.makedirs(video_dir)
    #             os.chmod(video_dir, 0o777)
            

    #         timestamp = datetime.timestamp(datetime.now())
    #         final_timestamp = str(timestamp).split('.')
    #         change_filename = video.filename.split('.')
    #         final_filename = change_filename[0]
    #         if change_filename[-1] == "mp4" or change_filename[-1] == "MP4":
    #             final_filename = f"{os.path.basename(section)}_{question_id}.{change_filename[-1]}" if section is not None else f"{final_timestamp[0]}.{change_filename[-1]}"
    #             file_location = f"uploads/{section}/videos/{final_filename}"
    #             with open(file_location, "wb+") as file_object:
    #                 file_object.write(video.file.read())
    #             return file_location
    #     except Exception as e:
    #         # Get the traceback as a string
    #         traceback_str = traceback.format_exc()
    #         print(traceback_str)

    #         # Get the line number of the exception
    #         line_no = traceback.extract_tb(e.__traceback__)[-1][1]
    #         print(f"Exception occurred on line {line_no}")
    #         return str(e)
    
    def upload_file(video: UploadFile, section: Optional[str] = None):
        file_location =""
        try:
            upload_path = os.path.join(os.getcwd(), 'uploads', f"{section}") if section is not None else os.path.join(os.getcwd(), 'uploads')
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
                os.chmod(upload_path, 0o777)

            timestamp = datetime.timestamp(datetime.now())
            final_timestamp = str(timestamp).split('.')
            change_filename = video.filename.split('.')
            final_filename = change_filename[0]
            if change_filename[-1] == "mp4" or change_filename[-1] == "MP4":
                final_filename = f"{os.path.basename(section)}_{final_timestamp[0]}.{change_filename[-1]}" if section is not None else f"{final_timestamp[0]}.{change_filename[-1]}"
                file_location = f"uploads/{section}/{final_filename}"
                with open(file_location, "wb+") as file_object:
                    file_object.write(video.file.read())
                return file_location
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    
    #Extract Audio using moviepy package

    # def extractAudio(input_video_path):          using moviepy package
    #     output_audio_path=os.path.join(os.getcwd(), "uploads/1/extrect_output.mp3")
    #     video_clip = VideoFileClip(input_video_path)
    #     audio_clip = video_clip.audio
    #     # Save the audio to a new file
    #     audio_clip.write_audiofile(output_audio_path, codec='libmp3lame')

    #     # Close the video clip
    #     video_clip.close()
    #     file_location="uploads/1/extrect_output.mp3"
    #     return file_location
    
   
    #For extrect Audio File Logic is Here.
   
   
    # def extractAudioFfmpeg(input_video_path,section: Optional[str] = None):
    #     try:
    #         file_location =""
    #         upload_path = os.path.join(os.getcwd(), 'uploads', f"{section}") if section is not None else os.path.join(os.getcwd(), 'uploads')
    #         if not os.path.exists(upload_path):
    #             os.mkdir(upload_path)
    #             os.chmod(audio_dir, 0o777)
    #         audio_dir = os.path.join(upload_path,"audios")
    #         if not os.path.exists(audio_dir):
    #             os.mkdir(audio_dir)
    #             os.chmod(audio_dir, 0o777)

    #         timestamp = datetime.timestamp(datetime.now())
    #         final_timestamp = str(timestamp).split('.')
    #         change_filename = input_video_path.split('.')
    #         final_filename = change_filename[0]
    #         if change_filename[-1] == "mp4" or change_filename[-1] == "MP4":
    #             change_filename[-1]="mp3"
    #             final_filename = f"{os.path.basename(section)}_{final_timestamp[0]}.{change_filename[-1]}" if section is not None else f"{final_timestamp[0]}.{change_filename[-1]}"
    #             file_location =f"uploads/{section}/audios/{final_filename}"
    #             ffmpeg_command = 'ffmpeg -i {} -vn {}'.format(input_video_path, file_location)
    #             subprocess.run(ffmpeg_command, shell=True)

    #         return file_location
    #     except Exception as e:
    #         # Get the traceback as a string
    #         traceback_str = traceback.format_exc()
    #         print(traceback_str)

    #         # Get the line number of the exception
    #         line_no = traceback.extract_tb(e.__traceback__)[-1][1]
    #         print(f"Exception occurred on line {line_no}")
    #         return str(e)
    
    def video_merging(user_session_id):
        try:
            # Directory containing the video files
            directory = os.path.join(os.getcwd(), f"uploads/{str(user_session_id)}/videos")

            # Get a list of all .mp4 files in the directory
            video_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.mp4')]

            # Sort video paths based on question_id
            video_paths.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

            output_file_path = os.path.join(os.getcwd(), f"uploads/{str(user_session_id)}/output.mp4")
            #text file
            temp_file_path = os.path.join(os.getcwd(), "temp_file.txt")
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write('\n'.join(["file '{}'".format(video_path) for video_path in video_paths]))
            
            #video merging
            ffmpeg_command = '/usr/bin/ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(temp_file_path, output_file_path)
            subprocess.run(ffmpeg_command, shell=True)

            os.remove(temp_file_path)
            
            file_location=f"uploads/{str(user_session_id)}/output.mp4"
            return file_location
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    
    def send_mail(email_subject: str, receipient_email: str, email_body, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
        try:
            configurations_data=db.query(ConfigurationsModel).filter(ConfigurationsModel.config_type==1).all()
            configurations = {configuration.__dict__['config_key']: configuration.__dict__['config_value'] for
                           configuration in
                           configurations_data}
            conf = ConnectionConfig(
                MAIL_USERNAME=configurations['mail_username'],
                MAIL_PASSWORD=configurations['mail_password'],
                MAIL_FROM=configurations['mail_from'],
                MAIL_PORT=int(configurations['mail_port']),
                MAIL_SERVER=configurations['mail_server'],
                MAIL_FROM_NAME=configurations['mail_from_name'],
                MAIL_STARTTLS=False,
                MAIL_SSL_TLS=True,
                # MAIL_TLS=True,
                # MAIL_SSL=False,
                USE_CREDENTIALS=True
            )
                
            
            message = MessageSchema(
                    subject=email_subject,
                    recipients=[receipient_email],
                    body=email_body,
                    subtype=MessageType.html
                    # html=email_body,
                    # subtype="html"
                )
            fm = FastMail(conf)
            background_tasks.add_task(fm.send_message,message)
            return True
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    
    def email_validation_helper(emailVal: str):
        if (re.fullmatch(emailRegex, emailVal)):
            return True
        else:
            return False


    # def convert_to_wav(input_audio_path, output_wav_path):
    #     audio = AudioSegment.from_file(input_audio_path)
    #     audio.export(output_wav_path, format="wav")

    # def audio_to_text(input_audio_path):
    
        # output_text_path = os.path.join(os.getcwd(), "uploads/1/sample_check.txt")

        # # Convert to WAV using pydub and ffmpeg
        # audio = AudioSegment.from_file(input_audio_path)
        # audio_data = audio.raw_data
        # audio_sr = audio.frame_rate
        # audio_channels = audio.channels

        # # Use ffmpeg to convert raw audio data to WAV
        # converted_audio = AudioSegment(
        #     audio_data,
        #     frame_rate=audio_sr,
        #     sample_width=audio.sample_width,
        #     channels=audio_channels
        # )

        # # Save the converted audio to a temporary WAV file
        # temp_wav_path = os.path.join(os.getcwd(), "uploads/1/temp.wav")
        # converted_audio.export(temp_wav_path, format="wav")

        # recognizer = sr.Recognizer()

        # try:
        #     # Use the temporary WAV file for speech recognition
        #     audio_file = sr.AudioFile(temp_wav_path)

        #     with audio_file as source:
        #         recognizer.adjust_for_ambient_noise(source)
        #         audio_data = recognizer.record(source)

        #     # Recognize speech using Google Web Speech API
        #     text = recognizer.recognize_sphinx(audio_data)

        #     # Save the text to a file
        #     with open(output_text_path, 'w') as text_file:
        #         text_file.write(text)

        #     print("Audio to text conversion successful. Text saved to", output_text_path)

        # except sr.UnknownValueError:
        #     print("Speech Recognition could not understand audio")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error during ffmpeg execution: {e}")
        # finally:
        #     # Clean up: Remove the temporary WAV file
        #     os.remove(temp_wav_path)

        # return None
