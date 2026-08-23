from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.core.dependencies import get_supabase_client
from app.schemas.words import WordBase

router = APIRouter(prefix="/words",tags=["Words"])

@router.get("/{dict_id}",status_code=status.HTTP_200_OK)
def words_list(dict_id:int,client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("words").select("*").eq("dictionary_id",dict_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/add",status_code=status.HTTP_201_CREATED)
def add_word(payload:WordBase,client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("words").insert(payload.model_dump(mode="json")).execute()
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Word is not added. You are not allowed for this operation or dictionary is not found"
        )
    return response.data

    

@router.delete("/delete/{word_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_word(word_id:int,client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("words").delete().eq("id",word_id).execute()
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word is not found or you are not allowed for this operation"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    