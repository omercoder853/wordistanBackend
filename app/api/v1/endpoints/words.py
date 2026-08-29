from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.core.dependencies import get_supabase_client
from app.schemas.words import WordBase,DailyWord
from datetime import date

router = APIRouter(prefix="/words",tags=["Words"])

@router.get("/daily-word",status_code=status.HTTP_200_OK,response_model=DailyWord)
def get_daily_word(client = Depends(get_supabase_client)):
    TOTAL_WORDS = 400
    today = date.today()
    EPOCH_DATE = date(2026,8,29)

    day_diff = (today - EPOCH_DATE).days
    target_id = (abs(day_diff) % TOTAL_WORDS)+1

    try:
        res = client["db"].table("daily_words").select("id,word,type,meaning,example_en,example_tr").eq("id",target_id).single().execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word is not found or you are not allowed for this operation"
        )
    word = res.data["word"]
    try:
        response = client["db"].table("words").select("id").or_(f"word.eq.{word},meaning.eq.{word}").execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if response.data:
        id = response.data[0]["id"]
        return DailyWord.model_validate({**res.data,"target_date":today,"is_saved":True,"saved_id":id})
    else:
        return DailyWord.model_validate({**res.data,"target_date":today,"is_saved":False,"saved_id":None})

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
    return
    