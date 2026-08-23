from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class WordBase(BaseModel):
    dictionary_id:int
    word:str
    meaning:str