from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.core.dependencies import get_supabase_client
from app.core.supabase import supabase

router = APIRouter(prefix="/achievements",tags=["Achievements"])

@router.get("/earned",status_code=status.HTTP_200_OK)
def fetch_earned_achievements(client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("user_achievements").select("earned_at,achievement_detail:achievements(*)").eq("user_id",client["user"].id).execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return response.data

@router.get("/all",status_code=status.HTTP_200_OK)
def fetch_all_achievements():
    try:
        reponse = supabase.table("achievements").select("*").execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return reponse.data