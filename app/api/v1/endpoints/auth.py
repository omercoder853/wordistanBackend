from fastapi import APIRouter, HTTPException, status, Depends
from app.core.supabase import supabase
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest, RegisterRequest
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
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
            
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": session.token_type,
            "expires_in": session.expires_in,
            "user_id": user.id
        }
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
            
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": session.token_type,
            "expires_in": session.expires_in,
            "user_id": user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Refreshing failed: {str(e)}"
        )

@router.get("/me", status_code=status.HTTP_200_OK)
def get_my_profile(current_user = Depends(get_current_user)):
    return {
        "message": "Token is valid, protected endpoint accessed successfully!",
        "user_id": current_user.id,
        "email": current_user.email,
        "user_metadata": current_user.user_metadata
    }

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def auth_register(payload: RegisterRequest):
    try:
        response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": {
                    "first_name": payload.first_name,
                    "last_name": payload.last_name,
                    "nick_name": payload.nick_name,
                    "birth_date": str(payload.birth_date),
                    "gender": payload.gender,
                    "avatar_url": payload.avatar_url
                }
            }
        })
        session = response.session
        user = response.user
        
        if not session or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration succeeded, but session could not be established (Email confirmation may be required)."
            )
        
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": session.token_type,
            "expires_in": session.expires_in,
            "user_id": user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Registration failed: {str(e)}"
        )