from pydantic import BaseModel, Field , EmailStr
from typing import Optional,Dict,Any
from datetime import datetime,date
from uuid import UUID

class UserStats(BaseModel):
    user_id : UUID
    level : int
    total_xp : int
    max_streak : int
    updated_at : datetime
    saved_words : int
    translated_words : int
    dict_created : int
    xp_for_next : int
    required_xp_for_level : int
    current_streak : int
    last_activity_date : Optional[date]
    