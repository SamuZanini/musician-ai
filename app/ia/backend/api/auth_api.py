"""
Authentication API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.user import User, UserCreate, UserLogin
from ..services.auth_service import AuthService
from ..database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    return await auth_service.get_current_user(credentials.credentials, db)


@router.post("/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        user = await auth_service.register_user(user_data, db)
        return {
            "message": "User registered successfully",
            "user": user.dict()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Dict[str, Any])
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return token"""
    try:
        result = await auth_service.authenticate_user(login_data, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    try:
        success = await auth_service.change_password(
            current_user.id, old_password, new_password, db
        )
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    """Initiate password reset process"""
    try:
        success = await auth_service.forgot_password(email, db)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """Reset password with token"""
    try:
        success = await auth_service.reset_password(token, new_password, db)
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
