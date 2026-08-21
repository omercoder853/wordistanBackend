from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# 1. Ortak Alanlar (Tüm modellerin miras alacağı temel yapı)
class DictionaryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["İspanyolca A1"])
    description: str | None = Field(default=None, max_length=255, examples=["Temel başlangıç kelimeleri"])
    language: str = Field(default="TR to ENG", examples=["TR to ENG","ENG to TR"])


# 3. Yanıt Şeması (İstemciye geri dönerken kullanılacak format)
class DictionaryResponse(DictionaryBase):
    id: UUID
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True