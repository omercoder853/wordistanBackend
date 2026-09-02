from pydantic import BaseModel
from uuid import UUID

class NewGameSession(BaseModel):
    game_mode: str
    score : int
    correct_count : int
    wrong_count : int
    total_count : int
    passed_count : int
    duration_secs : int