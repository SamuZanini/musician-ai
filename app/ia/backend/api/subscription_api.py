"""
Subscription API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any
from ..models.subscription import (
    SubscriptionPlanDetails, UserSubscription, PaymentIntent, AboutUs
)
from ..models.user import User
from ..services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscription", tags=["Subscription"])
subscription_service = SubscriptionService()


async def get_current_user() -> User:
    """Get current authenticated user"""
    # This would be implemented with proper JWT validation
    pass


@router.get("/plans", response_model=List[SubscriptionPlanDetails])
async def get_all_plans():
    """Get all subscription plans"""
    try:
        plans = await subscription_service.get_all_plans()
        return plans
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/plans/{plan_type}", response_model=SubscriptionPlanDetails)
async def get_plan_by_type(plan_type: str):
    """Get subscription plan by type"""
    try:
        plan = await subscription_service.get_plan_by_type(plan_type)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )
        return plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/current", response_model=UserSubscription)
async def get_current_subscription(current_user: User = Depends(get_current_user)):
    """Get user's current subscription"""
    try:
        subscription = await subscription_service.get_user_subscription(current_user.id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No subscription found"
            )
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/create")
async def create_subscription(
    plan_type: str,
    is_yearly: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Create new subscription for user"""
    try:
        result = await subscription_service.create_subscription(
            current_user.id, plan_type, is_yearly
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/confirm")
async def confirm_subscription(payment_intent_id: str):
    """Confirm subscription after successful payment"""
    try:
        subscription = await subscription_service.confirm_subscription(payment_intent_id)
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/cancel")
async def cancel_subscription(current_user: User = Depends(get_current_user)):
    """Cancel user subscription"""
    try:
        success = await subscription_service.cancel_subscription(current_user.id)
        return {"message": "Subscription cancelled successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/trial")
async def start_trial(
    plan_type: str,
    current_user: User = Depends(get_current_user)
):
    """Start free trial for user"""
    try:
        subscription = await subscription_service.start_trial(current_user.id, plan_type)
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/access/{feature}")
async def check_access(
    feature: str,
    current_user: User = Depends(get_current_user)
):
    """Check if user has access to a specific feature"""
    try:
        has_access = await subscription_service.check_subscription_access(
            current_user.id, feature
        )
        return {"feature": feature, "has_access": has_access}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/about", response_model=AboutUs)
async def get_about_us():
    """Get about us content"""
    try:
        about = await subscription_service.get_about_us()
        return about
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/payments", response_model=List[PaymentIntent])
async def get_payment_history(current_user: User = Depends(get_current_user)):
    """Get user's payment history"""
    try:
        payments = await subscription_service.get_payment_history(current_user.id)
        return payments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
