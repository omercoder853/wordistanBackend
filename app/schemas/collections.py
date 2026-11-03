from pydantic import BaseModel,Field,field_validator
from datetime import datetime
from uuid import UUID
from typing import Any,List

class Collection(BaseModel):
    id : UUID = Field(...)
    title_tr : str = Field(...)
    title_en : str = Field(...)
    description_tr : str = Field(...)
    description_en : str = Field(...)
    owner : str = "Wordistan"
    level : str = Field(...)
    collection_words : int = 0
    tags_tr : list
    tags_en : list
    created_at : datetime

    @field_validator('collection_words',mode="before")
    @classmethod
    def extract_word_count(cls,value:Any) -> int:
        if isinstance(value,list) and len(value)>0:
            return value[0].get('count',0)

    @field_validator('tags_tr', 'tags_en', mode='before')
    @classmethod
    def parse_comma_separated_tags(cls, value: Any) -> List[str]:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [tag.strip() for tag in value.split(',') if tag.strip()]
        return []

class CollectionWord(BaseModel):
    id : UUID
    word : str
    meaning : str
    level : str
    type : str
    created_at : datetime
