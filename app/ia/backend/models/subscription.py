"""
Subscription model for the #Dô application
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SubscriptionPlan(str, Enum):
    """Subscription plans"""
    COPPER = "copper"
    SILVER = "silver"
    GOLD = "gold"


class SubscriptionStatus(str, Enum):
    """Subscription status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"


class PlanFeatures(BaseModel):
    """Plan features model"""
    max_practice_sessions: int
    max_scores_per_day: int
    advanced_ml_features: bool
    premium_scores: bool
    priority_support: bool
    offline_mode: bool


class SubscriptionPlanDetails(BaseModel):
    """Subscription plan details"""
    id: str
    name: str
    plan_type: SubscriptionPlan
    price_monthly: float
    price_yearly: float
    features: PlanFeatures
    description: str
    is_popular: bool = False


class UserSubscription(BaseModel):
    """User subscription model"""
    id: str
    user_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    start_date: datetime
    end_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    auto_renew: bool = True


class PaymentIntent(BaseModel):
    """Payment intent model"""
    id: str
    user_id: str
    plan: SubscriptionPlan
    amount: float
    currency: str = "USD"
    stripe_payment_intent_id: str
    status: str
    created_at: datetime


class AboutUs(BaseModel):
    """About us content model"""
    title: str
    description: str
    mission: str
    team: List[dict]  # Team member info
    image_url: str
    contact_email: str
