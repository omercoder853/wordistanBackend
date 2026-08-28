from fastapi import APIRouter, HTTPException, status, Depends
from app.core.supabase import supabase,supabase_admin
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest, RegisterRequest , LoginResponse,ChangePasswordRequest
from app.core.dependencies import get_supabase_client,get_current_user
from app.api.v1.endpoints.stats import fetch_user_stats

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def auth_login(payload: LoginRequest):
    try:
        res = supabase.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        session = res.session
        user = res.user
        if not session or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login failed, user or session not found."
            )
        metadata = {**(user.user_metadata),"created_at":str(user.created_at)}
        return LoginResponse.model_validate({
                    **session.__dict__,
                    "user_id":user.id,
                    "email":user.email,
                    "metadata":metadata
                })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def refresh_token(payload: RefreshRequest):
    try:
        response = supabase.auth.refresh_session(payload.refresh_token)
        session = response.session
        user = response.user

        if not session or not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
            
        return TokenResponse.model_validate({
                    **session.__dict__,
                    "user_id":user.id
                })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Refreshing failed: {str(e)}"
        )

@router.get("/me", status_code=status.HTTP_200_OK)
def get_my_profile(client=Depends(get_supabase_client)):
    return {
        "message": "Token is valid, protected endpoint accessed successfully!",
        "user_id": client["user"].id,
        "email": client["user"].email,
        "user_metadata": client["user"].user_metadata,
        "user_stats":fetch_user_stats(client=client)
    }


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def auth_register(payload: RegisterRequest):
    try:
        response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": payload.model_dump(mode="json",exclude={"email","password"})
            }
        })
        session = response.session
        user = response.user
        
        if not session or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration succeeded, but session could not be established (Email confirmation may be required)."
            )
        
        return TokenResponse.model_validate({
            **session.__dict__,
            "user_id":user.id
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Registration failed: {str(e)}"
        )

@router.delete("/delete-user",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user=Depends(get_current_user)):
    user_id = user["user"].id
    try:
        res = supabase_admin.auth.admin.delete_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while deleting user : {str(e)}"
        )
    return

@router.post("/change-password",status_code=status.HTTP_204_NO_CONTENT)
def change_password(data: ChangePasswordRequest,client=Depends(get_supabase_client)):

    user = client["user"]
    try:
        supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": data.current_password
        })
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is wrong"
        )
    
    try:
        supabase_admin.auth.admin.update_user_by_id(user.id,{"password": data.new_password})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password can not be changed: {str(e)}"
        )
    return 