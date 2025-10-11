"""
Authentication Service for #Dô application
Handles user authentication, JWT tokens, and password management
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..database.models import User as DBUser, UserRole, SubscriptionPlan
from ..models.user import User, UserCreate, UserLogin


class AuthService:
    """Authentication service using JWT and bcrypt"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    async def register_user(self, user_data: UserCreate, db: Session) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        import uuid
        user_id = str(uuid.uuid4())
        hashed_password = self.get_password_hash(user_data.password)
        
        db_user = DBUser(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password,
            avatar_url=user_data.avatar_url,
            favorite_instrument=user_data.favorite_instrument,
            subscription_plan=user_data.subscription_plan,
            role=user_data.role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            avatar_url=db_user.avatar_url,
            favorite_instrument=db_user.favorite_instrument,
            subscription_plan=db_user.subscription_plan,
            role=db_user.role,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
            is_active=db_user.is_active
        )
    
    async def authenticate_user(self, login_data: UserLogin, db: Session) -> Dict[str, Any]:
        """Authenticate user and return token"""
        # Get user from database
        db_user = db.query(DBUser).filter(DBUser.email == login_data.email).first()
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not self.verify_password(login_data.password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is active
        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account deactivated"
            )
        
        # Update last login
        db_user.last_login = datetime.utcnow()
        db.commit()
        
        # Create access token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": db_user.id, "email": db_user.email},
            expires_delta=access_token_expires
        )
        
        user = User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            avatar_url=db_user.avatar_url,
            favorite_instrument=db_user.favorite_instrument,
            subscription_plan=db_user.subscription_plan,
            role=db_user.role,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
            is_active=db_user.is_active
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    async def get_current_user(self, token: str, db: Session) -> User:
        """Get current user from token"""
        payload = self.verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            avatar_url=db_user.avatar_url,
            favorite_instrument=db_user.favorite_instrument,
            subscription_plan=db_user.subscription_plan,
            role=db_user.role,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
            is_active=db_user.is_active
        )
    
    async def change_password(self, user_id: str, old_password: str, new_password: str, db: Session) -> bool:
        """Change user password"""
        db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify old password
        if not self.verify_password(old_password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid old password"
            )
        
        # Update password
        db_user.password_hash = self.get_password_hash(new_password)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        
        return True
    
    async def forgot_password(self, email: str, db: Session) -> bool:
        """Initiate password reset process"""
        db_user = db.query(DBUser).filter(DBUser.email == email).first()
        
        if not db_user:
            # Don't reveal if email exists
            return True
        
        # In a real implementation, you would:
        # 1. Generate a reset token
        # 2. Send email with reset link
        # 3. Store reset token with expiration
        
        return True
    
    async def reset_password(self, token: str, new_password: str, db: Session) -> bool:
        """Reset password with token"""
        # In a real implementation, you would:
        # 1. Verify reset token
        # 2. Check expiration
        # 3. Update password
        # 4. Invalidate token
        
        return True
