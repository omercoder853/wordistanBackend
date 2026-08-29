from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from uuid import UUID

class WordBase(BaseModel):
    dictionary_id:int
    word:str
    meaning:str

class DailyWord(BaseModel):
    id:int
    word:str
    type:str
    meaning:str
    example_en:str
    example_tr:str
    target_date:date
    is_saved:bool
    saved_id:int | None