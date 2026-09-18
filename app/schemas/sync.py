from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DictionaryPushItem(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    language: str
    created_at: Optional[datetime] = None

class WordPushItem(BaseModel):
    id: str
    dictionary_id: str
    word: str
    meaning: str
    added_at: Optional[datetime] = None

class SyncPushRequest(BaseModel):
    dictionaries: List[DictionaryPushItem] = []
    words: List[WordPushItem] = []
    deleted_dictionary_ids: List = []
    deleted_words_ids: List = []

class SyncPushResponse(BaseModel):
    success: bool
    synced_dictionary_ids: List[str]
    synced_word_ids: List[str]