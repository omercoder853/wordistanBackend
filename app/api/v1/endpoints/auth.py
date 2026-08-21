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
            
        return TokenResponse.model_validate({
                    **session.__dict__,
                    "user_id":user.id
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