from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase import supabase

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
        ):
    token = credentials.credentials

    try:
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        return {"user":user_response.user,"token":token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_supabase_client(current_user=Depends(get_current_user)):
    token = current_user["token"]
    supabase.postgrest.session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return {"db":supabase , "user":current_user["user"]}
    
    