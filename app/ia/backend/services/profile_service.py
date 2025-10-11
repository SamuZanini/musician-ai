"""
Profile Service for #Dô application
Handles user profile management, avatar uploads, and user statistics
"""
import os
import base64
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import firebase_admin
from firebase_admin import firestore, storage
from ..models.user import User, UserUpdate, UserProfile, Instrument, SubscriptionPlan


class ProfileService:
    """Profile management service"""
    
    def __init__(self):
        self.db = firestore.client()
        self.bucket = storage.bucket()
    
    async def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile with statistics"""
        user_doc = self.db.collection('users').document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = user_doc.to_dict()
        
        # Get practice statistics
        practice_stats = await self._get_practice_stats(user_id)
        
        return UserProfile(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            avatar_url=user_data.get('avatar_url'),
            favorite_instrument=user_data.get('favorite_instrument'),
            subscription_plan=user_data.get('subscription_plan', SubscriptionPlan.COPPER),
            created_at=user_data['created_at'],
            practice_streak=practice_stats.get('current_streak', 0),
            total_practice_time=practice_stats.get('total_practice_time', 0)
        )
    
    async def update_user_profile(self, user_id: str, update_data: UserUpdate) -> User:
        """Update user profile"""
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = user_doc.to_dict()
        update_dict = {}
        
        # Update fields if provided
        if update_data.email is not None:
            # Check if email is already taken
            existing_user = self.db.collection('users').where('email', '==', update_data.email).get()
            if existing_user and existing_user[0].id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            update_dict['email'] = update_data.email
        
        if update_data.username is not None:
            update_dict['username'] = update_data.username
        
        if update_data.avatar_url is not None:
            update_dict['avatar_url'] = update_data.avatar_url
        
        if update_data.favorite_instrument is not None:
            update_dict['favorite_instrument'] = update_data.favorite_instrument
        
        if update_data.password is not None:
            # Hash new password
            from ..services.auth_service import AuthService
            auth_service = AuthService()
            update_dict['password_hash'] = auth_service.get_password_hash(update_data.password)
        
        if update_dict:
            update_dict['updated_at'] = datetime.utcnow()
            user_ref.update(update_dict)
        
        # Return updated user
        updated_doc = user_ref.get()
        return User(**updated_doc.to_dict())
    
    async def upload_avatar(self, user_id: str, avatar_data: str) -> str:
        """Upload user avatar and return URL"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(avatar_data.split(',')[1])
            
            # Validate image size (max 1MB)
            if len(image_data) > 1024 * 1024:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image too large. Maximum size is 1MB."
                )
            
            # Generate filename
            filename = f"avatars/{user_id}_{datetime.utcnow().timestamp()}.jpg"
            
            # Upload to Firebase Storage
            blob = self.bucket.blob(filename)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            
            # Make public and get URL
            blob.make_public()
            avatar_url = blob.public_url
            
            # Update user profile
            self.db.collection('users').document(user_id).update({
                'avatar_url': avatar_url,
                'updated_at': datetime.utcnow()
            })
            
            return avatar_url
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload avatar: {str(e)}"
            )
    
    async def delete_avatar(self, user_id: str) -> bool:
        """Delete user avatar"""
        user_doc = self.db.collection('users').document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = user_doc.to_dict()
        avatar_url = user_data.get('avatar_url')
        
        if avatar_url:
            try:
                # Extract filename from URL
                filename = avatar_url.split('/')[-1]
                blob_name = f"avatars/{filename}"
                
                # Delete from Firebase Storage
                blob = self.bucket.blob(blob_name)
                blob.delete()
                
                # Update user profile
                self.db.collection('users').document(user_id).update({
                    'avatar_url': None,
                    'updated_at': datetime.utcnow()
                })
                
                return True
            except Exception as e:
                # Log error but don't fail the request
                print(f"Error deleting avatar: {str(e)}")
                return False
        
        return True
    
    async def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get detailed user statistics"""
        practice_stats = await self._get_practice_stats(user_id)
        
        # Get recent practice sessions
        sessions_ref = self.db.collection('practice_sessions')
        recent_sessions = sessions_ref.where('user_id', '==', user_id)\
            .order_by('start_time', direction=firestore.Query.DESCENDING)\
            .limit(10).get()
        
        recent_sessions_data = []
        for session in recent_sessions:
            session_data = session.to_dict()
            recent_sessions_data.append({
                'id': session_data['id'],
                'start_time': session_data['start_time'],
                'duration_minutes': session_data.get('duration_minutes', 0),
                'accuracy_percentage': session_data.get('accuracy_percentage', 0),
                'instrument_type': session_data.get('instrument_type')
            })
        
        return {
            'practice_stats': practice_stats,
            'recent_sessions': recent_sessions_data,
            'achievements': await self._get_user_achievements(user_id)
        }
    
    async def _get_practice_stats(self, user_id: str) -> Dict[str, Any]:
        """Get practice statistics for user"""
        # Get all practice sessions for user
        sessions_ref = self.db.collection('practice_sessions')
        sessions = sessions_ref.where('user_id', '==', user_id).get()
        
        total_time = 0
        total_sessions = len(sessions)
        accuracy_sum = 0
        current_streak = 0
        longest_streak = 0
        temp_streak = 0
        
        # Calculate statistics
        for session in sessions:
            session_data = session.to_dict()
            total_time += session_data.get('duration_minutes', 0)
            accuracy_sum += session_data.get('accuracy_percentage', 0)
        
        average_accuracy = accuracy_sum / total_sessions if total_sessions > 0 else 0
        
        # Calculate streak (simplified - in real implementation, check consecutive days)
        if total_sessions > 0:
            current_streak = min(total_sessions, 30)  # Simplified streak calculation
            longest_streak = current_streak
        
        return {
            'total_practice_time': total_time,
            'total_sessions': total_sessions,
            'average_accuracy': round(average_accuracy, 2),
            'current_streak': current_streak,
            'longest_streak': longest_streak
        }
    
    async def _get_user_achievements(self, user_id: str) -> list:
        """Get user achievements"""
        # This would be implemented based on practice milestones
        # For now, return empty list
        return []
    
    async def update_practice_streak(self, user_id: str, increment: bool = True) -> int:
        """Update user practice streak"""
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return 0
        
        user_data = user_doc.to_dict()
        current_streak = user_data.get('practice_streak', 0)
        
        if increment:
            new_streak = current_streak + 1
        else:
            new_streak = 0  # Reset streak
        
        user_ref.update({
            'practice_streak': new_streak,
            'updated_at': datetime.utcnow()
        })
        
        return new_streak
