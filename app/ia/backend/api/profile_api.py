"""
Profile API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Dict, Any
from ..models.user import User, UserUpdate, UserProfile
from ..services.auth_service import AuthService
from ..services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["Profile"])
auth_service = AuthService()
profile_service = ProfileService()


async def get_current_user() -> User:
    """Get current authenticated user"""
    # This would be implemented with proper JWT validation
    # For now, returning a mock user
    pass


@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile with statistics"""
    try:
        profile = await profile_service.get_user_profile(current_user.id)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/me", response_model=User)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    try:
        updated_user = await profile_service.update_user_profile(
            current_user.id, update_data
        )
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/avatar")
async def upload_avatar(
    avatar_data: str,  # Base64 encoded image
    current_user: User = Depends(get_current_user)
):
    """Upload user avatar"""
    try:
        avatar_url = await profile_service.upload_avatar(
            current_user.id, avatar_data
        )
        return {"avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/avatar")
async def delete_avatar(current_user: User = Depends(get_current_user)):
    """Delete user avatar"""
    try:
        success = await profile_service.delete_avatar(current_user.id)
        return {"message": "Avatar deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/statistics")
async def get_statistics(current_user: User = Depends(get_current_user)):
    """Get detailed user statistics"""
    try:
        stats = await profile_service.get_user_statistics(current_user.id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
