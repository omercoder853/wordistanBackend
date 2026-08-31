from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_supabase_client

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/sessions", status_code=status.HTTP_200_OK)
def get_game_sessions(client=Depends(get_supabase_client)):
    try:
        # Sıralama doğrudan DB seviyesinde yapılıyor
        response = (
            client["db"]
            .table("game_sessions")
            .select("*")
            .order("played_at", desc=True)
            .execute()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch game sessions: {str(e)}"
        )
    
    sessions = response.data or []
    
    if not sessions:
        return {
            "sessions": [],
            "totals": {"total": 0, "correct": 0, "wrong": 0, "passed": 0, "duration": 0},
            "average_score": 0.0,
            "game_mode_counts": {"mp": 0, "wc": 0, "mcq": 0},
            "best_performance": {"id": None, "score": 0.0}
        }

    sum_total = 0
    sum_correct = 0
    sum_wrong = 0
    sum_passed = 0
    sum_score = 0
    sum_duration = 0
    sum_performance_score = 0
    game_mode_counts = {"mp": 0, "wc": 0, "mcq": 0}

    first_perf = sessions[0].get("performance_score") or 0.0
    best_performance_id = sessions[0].get("id")
    best_performance_score = float(first_perf)

    for data in sessions:
        perf_score = float(data.get("performance_score") or 0.0)
        if perf_score > best_performance_score:
            best_performance_score = perf_score
            best_performance_id = data.get("id")

        sum_total += data.get("total_count", 0)
        sum_correct += data.get("correct_count", 0)
        sum_wrong += data.get("wrong_count", 0)
        sum_passed += data.get("passed_count", 0)
        sum_score += float(data.get("score", 0.0))
        sum_duration += data.get("duration_secs", 0)
        sum_performance_score += float(data.get("performance_score") or 0.0)

        mode = data.get("game_mode")
        if mode in game_mode_counts:
            game_mode_counts[mode] += 1

    return {
        "sessions": sessions,
        "totals": {
            "total": sum_total,
            "correct": sum_correct,
            "wrong": sum_wrong,
            "passed": sum_passed,
            "duration": sum_duration
        },
        "average_score": round(sum_score / len(sessions), 3),
        "average_performance_score": round(sum_performance_score / len(sessions), 3),
        "game_mode_counts": game_mode_counts,
        "best_performance": {
            "id": best_performance_id,
            "score": round(best_performance_score, 2)
        }
    }