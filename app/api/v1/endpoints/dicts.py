from fastapi import APIRouter,HTTPException,status,Depends
from app.schemas.dicts import DictionaryBase,DictionaryResponse
from app.core.dependencies import get_supabase_client

router = APIRouter(prefix="/dictionaries",tags=["Dictionaries"])

@router.get("/")
def dictionaries_list(client=Depends(get_supabase_client)):
    response = client["db"].table("dictionaries").select("* , words(count)").execute()
    return response.data

@router.post("/new",status_code=status.HTTP_201_CREATED)
def add_dictionary(payload : DictionaryBase,client=Depends(get_supabase_client)):
    user_id = str(client["user"].id)

    new_dict = {
        **payload.model_dump(mode="json"),
        "user_id":user_id
    }
    try:
        response = client["db"].table("dictionaries").insert(new_dict).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/delete/{dict_id}")
def delete_dictionary(dict_id,client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("dictionaries").delete().eq("id",dict_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dictionary is not found or you are not allowed for this."
            )
        return {"message": "Dictionary deleted successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )