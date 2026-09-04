from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from datetime import date,datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

class WordRequest(BaseModel):
    dictionary_id: int
    word: str
    meaning: str

    @field_validator("word")
    @classmethod
    def clean_word(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if not cleaned:
            raise ValueError("Word field can not be empty.")
        return cleaned

    @field_validator("meaning")
    @classmethod
    def clean_meaning(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if not cleaned:
            raise ValueError("Meaning field can not be empty.")
        return cleaned

class WordResponse(BaseModel):
    id : int
    dictionary_id : int
    word : str
    meaning : str
    added_at : datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("word")
    @classmethod
    def capitalize_word(cls,v:str) -> str:
        return v.strip().capitalize()
    
    @field_validator("meaning")
    @classmethod
    def capitalize_meaning(cls,v:str) -> str:
        return v.strip().capitalize()


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