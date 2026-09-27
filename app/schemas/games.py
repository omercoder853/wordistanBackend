from pydantic import BaseModel,Field
from uuid import UUID
from datetime import datetime

class NewGameSession(BaseModel):
    id:UUID = Field(...)
    game_mode: str = Field(...)
    score : float = Field(...)
    correct_count : int = Field(...)
    wrong_count : int = Field(...)
    total_count : int = Field(...)
    passed_count : int = Field(...)
    duration_secs : int = Field(...)
    performance_score : float = Field(...)
    played_at : datetime = Field(...)