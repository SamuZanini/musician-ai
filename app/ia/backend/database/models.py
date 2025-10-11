"""
SQLAlchemy database models for #Dô application
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .connection import Base


class UserRole(str, enum.Enum):
    """User roles enum"""
    ANONYMOUS = "anonymous"
    REGISTERED = "registered"
    PREMIUM = "premium"
    ADMIN = "admin"


class SubscriptionPlan(str, enum.Enum):
    """Subscription plans enum"""
    COPPER = "copper"
    SILVER = "silver"
    GOLD = "gold"


class InstrumentType(str, enum.Enum):
    """Instrument types enum"""
    VIOLIN = "violin"
    FLUTE = "flute"
    TRUMPET = "trumpet"
    PIANO = "piano"
    CELLO = "cello"


class PracticeSessionStatus(str, enum.Enum):
    """Practice session status enum"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class NoteAccuracy(str, enum.Enum):
    """Note accuracy enum"""
    PERFECT = "perfect"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class SubscriptionStatus(str, enum.Enum):
    """Subscription status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    favorite_instrument = Column(Enum(InstrumentType), nullable=True)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.COPPER)
    role = Column(Enum(UserRole), default=UserRole.REGISTERED)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    practice_streak = Column(Integer, default=0)
    total_practice_time = Column(Integer, default=0)  # in minutes
    
    # Relationships
    practice_sessions = relationship("PracticeSession", back_populates="user")
    play_along_sessions = relationship("PlayAlongSession", back_populates="user")
    subscriptions = relationship("UserSubscription", back_populates="user")
    payment_intents = relationship("PaymentIntent", back_populates="user")


class Instrument(Base):
    """Instrument model"""
    __tablename__ = "instruments"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(InstrumentType), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    tuning_notes = Column(Text, nullable=True)  # JSON string
    difficulty_level = Column(Integer, default=1)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class FAQItem(Base):
    """FAQ item model"""
    __tablename__ = "faq_items"
    
    id = Column(String, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    instrument_type = Column(Enum(InstrumentType), nullable=False)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())


class PracticeSession(Base):
    """Practice session model"""
    __tablename__ = "practice_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    instrument_type = Column(String, nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    status = Column(Enum(PracticeSessionStatus), default=PracticeSessionStatus.ACTIVE)
    notes_played = Column(Integer, default=0)
    correct_notes = Column(Integer, default=0)
    accuracy_percentage = Column(Float, default=0.0)
    streak_days = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="practice_sessions")


class NoteDetection(Base):
    """Note detection model"""
    __tablename__ = "note_detections"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("practice_sessions.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    note = Column(String, nullable=False)
    frequency = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    accuracy = Column(Enum(NoteAccuracy), nullable=False)
    timestamp = Column(DateTime, default=func.now())


class Composer(Base):
    """Composer model"""
    __tablename__ = "composers"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    period = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    scores = relationship("Score", back_populates="composer")


class Score(Base):
    """Musical score model"""
    __tablename__ = "scores"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    composer_id = Column(String, ForeignKey("composers.id"), nullable=False)
    instrument_type = Column(String, nullable=False)
    difficulty_level = Column(Integer, default=1)
    file_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    duration_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    composer = relationship("Composer", back_populates="scores")


class PlayAlongSession(Base):
    """Play-along session model"""
    __tablename__ = "play_along_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    score_id = Column(String, ForeignKey("scores.id"), nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    accuracy_score = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="play_along_sessions")
    score = relationship("Score")


class SubscriptionPlanDetails(Base):
    """Subscription plan details model"""
    __tablename__ = "subscription_plans"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    plan_type = Column(Enum(SubscriptionPlan), nullable=False)
    price_monthly = Column(Float, nullable=False)
    price_yearly = Column(Float, nullable=False)
    max_practice_sessions = Column(Integer, nullable=False)
    max_scores_per_day = Column(Integer, nullable=False)
    advanced_ml_features = Column(Boolean, default=False)
    premium_scores = Column(Boolean, default=False)
    priority_support = Column(Boolean, default=False)
    offline_mode = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class UserSubscription(Base):
    """User subscription model"""
    __tablename__ = "user_subscriptions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    status = Column(Enum(SubscriptionStatus), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    trial_end_date = Column(DateTime, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")


class PaymentIntent(Base):
    """Payment intent model"""
    __tablename__ = "payment_intents"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    stripe_payment_intent_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payment_intents")


class AboutUs(Base):
    """About us content model"""
    __tablename__ = "about_us"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    mission = Column(Text, nullable=False)
    team = Column(Text, nullable=True)  # JSON string
    image_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
