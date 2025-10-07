from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    full_name: str
    phone_number: str
    email: Optional[EmailStr] = None
    source_form: str


class LeadRead(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: Optional[EmailStr] = None
    source_form: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
