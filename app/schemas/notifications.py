from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime
from uuid import UUID

class Notification(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    title_tr: str = Field(..., min_length=1, max_length=100)
    title_en: str = Field(..., min_length=1, max_length=100)
    description_tr: str = Field(..., min_length=1, max_length=200)
    description_en: str = Field(..., min_length=1, max_length=200)
    data : Dict[str, Any] = Field(...) 
    is_read: bool = Field(...)

class NotificationResponse(Notification):
    id: UUID = Field(...)
    user_id: UUID = Field(...)
    created_at : datetime = Field(...)