from fastapi import APIRouter, HTTPException, status, Depends,Response
from app.core.dependencies import get_supabase_client

router = APIRouter(prefix="/stats", tags=["User Stats"])

def fetch_user_stats(client):
    user_id = client["user"].id
    try:
        response = (client["db"].table("user_stats").select("*").eq("user_id", user_id).execute())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching statistics: {str(e)}"
        )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User statistics not found."
        )

    return response.data[0]

@router.get("/", status_code=status.HTTP_200_OK)
def get_my_stats(client=Depends(get_supabase_client)):
    return fetch_user_stats(client=client)

@router.post("/increment-translation", status_code=status.HTTP_204_NO_CONTENT)
def increment_translation_stat(client=Depends(get_supabase_client)):
    try:
        client["db"].rpc("increment_translated_words", {"p_user_id": str(client["user"].id)}).execute()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Translation counter error: {str(e)}"
        )
