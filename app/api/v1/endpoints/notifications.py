from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.core.dependencies import get_supabase_client
from app.schemas.notifications import Notification,NotificationResponse
from typing import List

router = APIRouter(prefix="/notifications",tags=["Notifications"])

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[NotificationResponse])
def notifications_list(client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("notifications").select("*").eq("user_id", str(client["user"].id)).order("created_at", desc=True).execute()
    except Exception as e:
         raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
         )
    return response.data


@router.post("/new",status_code=status.HTTP_201_CREATED)
def create_notification(payload: Notification,client=Depends(get_supabase_client)):
    try:
        newNotification = payload.model_dump()
        newNotification["user_id"] = client["user"].id
        response = client["db"].table("notifications").insert(newNotification).execute()
    except Exception as e:
         raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
         )
    return response.data

@router.patch("/{notification_id}/read",status_code=status.HTTP_200_OK)
def mark_notification_as_read(notification_id:str,client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("notifications").update({"is_read": True}).eq("id", notification_id).eq("user_id", str(client["user"].id)).execute()
    except Exception as e:
         raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
         )
    return response.data

@router.patch("/read-all",status_code=status.HTTP_200_OK)
def mark_all_notifications_as_read(client=Depends(get_supabase_client)):
    try:
        response = client["db"].table("notifications").update({"is_read": True}).eq("user_id", str(client["user"].id)).execute()
    except Exception as e:
         raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
         )
    return response.data