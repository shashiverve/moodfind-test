from pydantic import BaseModel
from typing import Optional


class ConfigurationRequest(BaseModel):
    video_seconds: Optional[str] = None
    is_question_read_out: Optional[str] = None
    instruction_content: Optional[str] = None
    terms_and_condition: Optional[str] = None
    privacy_and_policy:Optional[str] = None
    demo_video_url:Optional[str] = None
 