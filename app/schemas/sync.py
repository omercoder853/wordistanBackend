from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.schemas.games import NewGameSession

class DictionaryPushItem(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    language: str
    created_at: Optional[datetime] = None

class WordPushItem(BaseModel):
    id: UUID
    dictionary_id: UUID
    word: str
    meaning: str
    added_at: Optional[datetime] = None

class XpLogItem(BaseModel):
    id: UUID
    action_type: str
    amount: int
    created_at: datetime

class SyncPushRequest(BaseModel):
    deleted_words_ids: Optional[List[UUID]] = []
    deleted_dictionary_ids: Optional[List[UUID]] = []
    dictionaries: Optional[List[DictionaryPushItem]] = []
    words: Optional[List[WordPushItem]] = []        
    xp_logs: Optional[List[XpLogItem]] = []
    game_sessions: Optional[List[NewGameSession]] = [] 

class SyncPushResponse(BaseModel):
    success: bool
    synced_dictionary_ids: List[UUID]
    synced_word_ids: List[UUID]
    synced_xp_logs_ids: List[UUID]
    synced_game_sessions: List[UUID]  