from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.schemas.collections import Collection,CollectionWord
from app.core.dependencies import get_supabase_client
from app.core.supabase import supabase
from typing import List

router = APIRouter(prefix="/collections",tags=["Collections"])

@router.get("/" , status_code=status.HTTP_200_OK,response_model=List[Collection])
def collections_list():
    try:
        response = supabase.table("collections").select("* , collection_words(count)").execute()
        data = response.data
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{collection_id}",status_code=status.HTTP_200_OK,response_model=List[CollectionWord])
def collection_words(collection_id:str):
    try:
        response = supabase.table("collection_words").select("*").eq("collection_id",collection_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )