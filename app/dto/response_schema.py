from pydantic import BaseModel, validator, root_validator
from typing import Union,Optional

class ResponseSchema(BaseModel):
    status: bool = True
    response: str
    data: Union[Optional[dict], Optional[list], None] = None
