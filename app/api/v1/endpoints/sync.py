from fastapi import APIRouter, Depends, HTTPException
from app.schemas.sync import SyncPushRequest, SyncPushResponse
from app.core.dependencies import get_supabase_client

router = APIRouter(prefix="/sync", tags=["Sync"])

@router.post("/push", response_model=SyncPushResponse)
async def push_sync_data(payload: SyncPushRequest, client: dict = Depends(get_supabase_client)):
    synced_dict_ids = []
    synced_word_ids = []
    synced_logs_ids = []
    synced_session_ids = []
    user_id = client["user"].id
    db = client["db"]

    # 1. DELETE LOCALLY DELETED WORDS
    if payload.deleted_words_ids:
        db.table("words").delete().in_("id", payload.deleted_words_ids).execute()

    # 2. DELETE LOCALLY DELETED DICTIONARIES
    if payload.deleted_dictionary_ids:
        db.table("dictionaries").delete().eq("user_id", user_id).in_("id", payload.deleted_dictionary_ids).execute()

    # 3. UPSERT DICTIONARIES
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

    # 4. UPSERT WORDS
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

    # 5. UPSERT XP LOGS
    if payload.xp_logs:
        xp_records = [
            {
                "id": str(log.id),
                "user_id": user_id,
                "action_type": log.action_type,
                "amount": log.amount,
                "created_at": (
                    log.created_at.isoformat()
                    if hasattr(log.created_at, "isoformat")
                    else str(log.created_at)
                ),
            }
            for log in sorted(payload.xp_logs, key=lambda x: x.created_at)
        ]

        res_logs = (
            db.table("xp_logs")
            .upsert(xp_records, on_conflict="id", ignore_duplicates=True)
            .execute()
        )

        synced_logs_ids = [str(log.id) for log in payload.xp_logs]

    # 6. UPSERT GAME SESSIONS
    if payload.game_sessions:
        game_sessions_record = [
            {
                "id": str(session.id),
                "user_id": user_id,
                "game_mode": session.game_mode,
                "total_count": session.total_count,
                "correct_count": session.correct_count,
                "wrong_count": session.wrong_count,
                "passed_count": session.passed_count,
                "duration_secs": session.duration_secs,
                "score": session.score,
                "performance_score": session.performance_score,
                "played_at": (
                    session.played_at.isoformat()
                    if hasattr(session.played_at,"isoformat")
                    else str(session.played_at)
                ),
            }
            for session in sorted(payload.game_sessions, key=lambda x: x.played_at)
        ]

        res_sessions = (
            db.table("game_sessions")
            .upsert(game_sessions_record, on_conflict="id", ignore_duplicates=True)
            .execute()
        )

        synced_session_ids = [str(session.id) for session in payload.game_sessions]

    return {
        "success": True,
        "synced_dictionary_ids": synced_dict_ids,
        "synced_word_ids": synced_word_ids,
        "synced_xp_logs_ids" : synced_logs_ids,
        "synced_game_sessions" : synced_session_ids,
    }