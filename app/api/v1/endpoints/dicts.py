from fastapi import APIRouter,HTTPException,status
from app.core.supabase import supabase
from app.schemas.dicts import DictionaryCreate,DictionaryResponse

router = APIRouter(prefix="/dictionaries",tags=["Dictionaries"])

@router.get("/")
def dictionaries_list():
    response = supabase.table("dictionaries").select("*").execute()
    return response.data

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_dictionary(payload : DictionaryCreate):
    new_dict = {
        "name":payload.name,
        "description":payload.description,
        "language":payload.language,
        "user_id":str(payload.user_id)
    }
    try:
        response = supabase.table("dictionaries").insert(new_dict).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )