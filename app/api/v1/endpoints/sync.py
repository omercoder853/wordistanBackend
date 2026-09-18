from fastapi import APIRouter, Depends, HTTPException
from app.schemas.sync import SyncPushRequest, SyncPushResponse
from app.core.dependencies import get_supabase_client

router = APIRouter(prefix="/sync", tags=["Sync"])

@router.post("/push", response_model=SyncPushResponse)
async def push_sync_data(payload: SyncPushRequest, client: dict = Depends(get_supabase_client)):
    synced_dict_ids = []
    synced_word_ids = []
    user_id = client["user"].id
    db = client["db"]

    # 1. ÖNCE SİLİNEN KELİMELERİ SİL
    if payload.deleted_words_ids:
        db.table("words").delete().in_("id", payload.deleted_words_ids).execute()

    # 2. SİLİNEN SÖZLÜKLERİ SİL
    if payload.deleted_dictionary_ids:
        db.table("dictionaries").delete().eq("user_id", user_id).in_("id", payload.deleted_dictionary_ids).execute()

    # 3. SÖZLÜKLERİ UPSERT ET
    if payload.dictionaries:
        dict_records = [
            {
                "id": str(d.id),
                "user_id": user_id,  
                "name": d.name,
                "description": d.description,
                "language": d.language,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in payload.dictionaries
        ]
        
        res_dict = db.table("dictionaries").upsert(dict_records, on_conflict="id").execute()
        if res_dict.data:
            synced_dict_ids = [d["id"] for d in res_dict.data]

    # 4. KELİMELERİ UPSERT ET
    if payload.words:
        word_records = [
            {
                "id": str(w.id),
                "dictionary_id": str(w.dictionary_id),
                "word": w.word,
                "meaning": w.meaning,
                "added_at": w.added_at.isoformat() if w.added_at else None
            }
            for w in payload.words
        ]
        
        res_words = db.table("words").upsert(word_records, on_conflict="id").execute()
        if res_words.data:
            synced_word_ids = [w["id"] for w in res_words.data]

    return {
        "success": True,
        "synced_dictionary_ids": synced_dict_ids,
        "synced_word_ids": synced_word_ids
    }