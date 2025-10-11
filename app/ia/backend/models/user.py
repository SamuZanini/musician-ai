"""
User model for the #Dô application
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system"""
    ANONYMOUS = "anonymous"
    REGISTERED = "registered"
    PREMIUM = "premium"
    ADMIN = "admin"


class SubscriptionPlan(str, Enum):
    """Subscription plans"""
    COPPER = "copper"
    SILVER = "silver"
    GOLD = "gold"


class Instrument(str, Enum):
    """Supported instruments"""
    VIOLIN = "violin"
    FLUTE = "flute"
    TRUMPET = "trumpet"
    PIANO = "piano"
    CELLO = "cello"


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    username: str
    avatar_url: Optional[str] = None
    favorite_instrument: Optional[Instrument] = None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.COPPER
    role: UserRole = UserRole.REGISTERED


class UserCreate(UserBase):
    """User creation model"""
    password: str


class UserUpdate(BaseModel):
    """User update model"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    favorite_instrument: Optional[Instrument] = None
    password: Optional[str] = None


class User(UserBase):
    """Complete user model"""
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str
    remember_me: bool = False


class UserProfile(BaseModel):
    """User profile for display"""
    id: str
    username: str
    email: EmailStr
    avatar_url: Optional[str]
    favorite_instrument: Optional[Instrument]
    subscription_plan: SubscriptionPlan
    created_at: datetime
    practice_streak: int = 0
    total_practice_time: int = 0  # in minutes
