# app/schemas/dict.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# 1. Ortak Alanlar (Tüm modellerin miras alacağı temel yapı)
class DictionaryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["İspanyolca A1"])
    description: Optional[str] = Field(default=None, max_length=255, examples=["Temel başlangıç kelimeleri"])
    language: str = Field(default="TR to ENG", examples=["TR to ENG"])


# 2. Sözlük Oluşturma Şeması (POST isteğinde body'den beklenenler)
class DictionaryCreate(DictionaryBase):
    user_id: UUID = Field(..., examples=["a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"])


# 3. Yanıt Şeması (İstemciye geri dönerken kullanılacak format)
class DictionaryResponse(DictionaryBase):
    id: UUID
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True