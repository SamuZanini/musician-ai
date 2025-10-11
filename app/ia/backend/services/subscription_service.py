"""
Subscription Service for #Dô application
Handles subscription plans, payments, and user access management
"""
import os
import stripe
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import firebase_admin
from firebase_admin import firestore
from ..models.subscription import (
    SubscriptionPlan, SubscriptionStatus, PlanFeatures, 
    SubscriptionPlanDetails, UserSubscription, PaymentIntent, AboutUs
)


class SubscriptionService:
    """Subscription and payment management service"""
    
    def __init__(self):
        self.db = firestore.client()
        
        # Initialize Stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        self.stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
        
        self._initialize_subscription_plans()
        self._initialize_about_us()
    
    def _initialize_subscription_plans(self):
        """Initialize subscription plans"""
        plans_data = [
            {
                'id': 'copper_plan',
                'name': 'Copper Plan',
                'plan_type': SubscriptionPlan.COPPER,
                'price_monthly': 5.00,
                'price_yearly': 50.00,
                'features': {
                    'max_practice_sessions': 10,
                    'max_scores_per_day': 3,
                    'advanced_ml_features': False,
                    'premium_scores': False,
                    'priority_support': False,
                    'offline_mode': False
                },
                'description': 'Perfect for beginners - Basic practice features',
                'is_popular': False
            },
            {
                'id': 'silver_plan',
                'name': 'Silver Plan',
                'plan_type': SubscriptionPlan.SILVER,
                'price_monthly': 15.00,
                'price_yearly': 150.00,
                'features': {
                    'max_practice_sessions': 50,
                    'max_scores_per_day': 10,
                    'advanced_ml_features': True,
                    'premium_scores': True,
                    'priority_support': True,
                    'offline_mode': False
                },
                'description': 'For serious musicians - Advanced features included',
                'is_popular': True
            },
            {
                'id': 'gold_plan',
                'name': 'Gold Plan',
                'plan_type': SubscriptionPlan.GOLD,
                'price_monthly': 25.00,
                'price_yearly': 250.00,
                'features': {
                    'max_practice_sessions': -1,  # Unlimited
                    'max_scores_per_day': -1,     # Unlimited
                    'advanced_ml_features': True,
                    'premium_scores': True,
                    'priority_support': True,
                    'offline_mode': True
                },
                'description': 'For professionals - Everything unlimited',
                'is_popular': False
            }
        ]
        
        # Check if plans already exist
        plans_ref = self.db.collection('subscription_plans')
        existing = plans_ref.get()
        
        if not existing:
            for plan_data in plans_data:
                plans_ref.document(plan_data['id']).set(plan_data)
    
    def _initialize_about_us(self):
        """Initialize about us content"""
        about_data = {
            'title': 'Sobre o #Dô',
            'description': 'O #Dô é uma plataforma inovadora que combina tecnologia de machine learning com educação musical para ajudar músicos de todos os níveis a melhorar sua prática.',
            'mission': 'Democratizar o acesso à educação musical de qualidade através da tecnologia, oferecendo feedback em tempo real e ferramentas avançadas de prática.',
            'team': [
                {
                    'name': 'Equipe de Desenvolvimento',
                    'role': 'Desenvolvedores',
                    'description': 'Estudantes de Análise e Desenvolvimento de Sistemas'
                }
            ],
            'image_url': '/images/about/orchestra.jpg',
            'contact_email': 'contato@dô.com'
        }
        
        # Store about us content
        self.db.collection('about_us').document('main').set(about_data)
    
    async def get_all_plans(self) -> List[SubscriptionPlanDetails]:
        """Get all subscription plans"""
        plans_ref = self.db.collection('subscription_plans')
        plans = plans_ref.get()
        
        return [SubscriptionPlanDetails(**doc.to_dict()) for doc in plans]
    
    async def get_plan_by_type(self, plan_type: SubscriptionPlan) -> Optional[SubscriptionPlanDetails]:
        """Get subscription plan by type"""
        plans_ref = self.db.collection('subscription_plans')
        plan_query = plans_ref.where('plan_type', '==', plan_type).get()
        
        if plan_query:
            return SubscriptionPlanDetails(**plan_query[0].to_dict())
        return None
    
    async def get_user_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """Get user's current subscription"""
        subscription_ref = self.db.collection('user_subscriptions')
        subscription_query = subscription_ref.where('user_id', '==', user_id).get()
        
        if subscription_query:
            subscription_data = subscription_query[0].to_dict()
            return UserSubscription(**subscription_data)
        return None
    
    async def create_subscription(self, user_id: str, plan_type: SubscriptionPlan, 
                                is_yearly: bool = False) -> Dict[str, Any]:
        """Create new subscription for user"""
        # Get plan details
        plan = await self.get_plan_by_type(plan_type)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription plan not found"
            )
        
        # Calculate price
        price = plan.price_yearly if is_yearly else plan.price_monthly
        currency = "USD"
        
        try:
            # Create Stripe payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(price * 100),  # Convert to cents
                currency=currency,
                metadata={
                    'user_id': user_id,
                    'plan_type': plan_type,
                    'is_yearly': str(is_yearly)
                }
            )
            
            # Store payment intent
            payment_intent_id = f"pi_{user_id}_{datetime.utcnow().timestamp()}"
            self.db.collection('payment_intents').document(payment_intent_id).set({
                'id': payment_intent_id,
                'user_id': user_id,
                'plan': plan_type,
                'amount': price,
                'currency': currency,
                'stripe_payment_intent_id': payment_intent.id,
                'status': payment_intent.status,
                'created_at': datetime.utcnow()
            })
            
            return {
                'payment_intent_id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'amount': price,
                'currency': currency,
                'plan': plan_type
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment processing error: {str(e)}"
            )
    
    async def confirm_subscription(self, payment_intent_id: str) -> UserSubscription:
        """Confirm subscription after successful payment"""
        # Get payment intent from database
        payment_ref = self.db.collection('payment_intents')
        payment_query = payment_ref.where('stripe_payment_intent_id', '==', payment_intent_id).get()
        
        if not payment_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment intent not found"
            )
        
        payment_data = payment_query[0].to_dict()
        user_id = payment_data['user_id']
        plan_type = payment_data['plan']
        
        # Verify payment with Stripe
        try:
            stripe_payment = stripe.PaymentIntent.retrieve(payment_intent_id)
            if stripe_payment.status != 'succeeded':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Payment not completed"
                )
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment verification error: {str(e)}"
            )
        
        # Calculate subscription dates
        start_date = datetime.utcnow()
        if payment_data.get('is_yearly', False):
            end_date = start_date + timedelta(days=365)
        else:
            end_date = start_date + timedelta(days=30)
        
        # Create subscription
        subscription_id = f"sub_{user_id}_{datetime.utcnow().timestamp()}"
        subscription = UserSubscription(
            id=subscription_id,
            user_id=user_id,
            plan=plan_type,
            status=SubscriptionStatus.ACTIVE,
            start_date=start_date,
            end_date=end_date,
            stripe_subscription_id=payment_intent_id,
            auto_renew=True
        )
        
        # Store subscription
        self.db.collection('user_subscriptions').document(subscription_id).set({
            'id': subscription_id,
            'user_id': user_id,
            'plan': plan_type,
            'status': subscription.status.value,
            'start_date': start_date,
            'end_date': end_date,
            'stripe_subscription_id': payment_intent_id,
            'auto_renew': True
        })
        
        # Update user's subscription plan
        self.db.collection('users').document(user_id).update({
            'subscription_plan': plan_type,
            'updated_at': datetime.utcnow()
        })
        
        return subscription
    
    async def cancel_subscription(self, user_id: str) -> bool:
        """Cancel user subscription"""
        subscription = await self.get_user_subscription(user_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found"
            )
        
        # Update subscription status
        subscription_ref = self.db.collection('user_subscriptions').document(subscription.id)
        subscription_ref.update({
            'status': SubscriptionStatus.CANCELLED.value,
            'auto_renew': False,
            'updated_at': datetime.utcnow()
        })
        
        # Update user's subscription plan to copper
        self.db.collection('users').document(user_id).update({
            'subscription_plan': SubscriptionPlan.COPPER,
            'updated_at': datetime.utcnow()
        })
        
        return True
    
    async def start_trial(self, user_id: str, plan_type: SubscriptionPlan) -> UserSubscription:
        """Start free trial for user"""
        # Check if user already has a subscription
        existing_subscription = await self.get_user_subscription(user_id)
        if existing_subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a subscription"
            )
        
        # Calculate trial dates
        start_date = datetime.utcnow()
        trial_end_date = start_date + timedelta(days=7)
        
        # Create trial subscription
        subscription_id = f"trial_{user_id}_{datetime.utcnow().timestamp()}"
        subscription = UserSubscription(
            id=subscription_id,
            user_id=user_id,
            plan=plan_type,
            status=SubscriptionStatus.TRIAL,
            start_date=start_date,
            trial_end_date=trial_end_date,
            auto_renew=False
        )
        
        # Store subscription
        self.db.collection('user_subscriptions').document(subscription_id).set({
            'id': subscription_id,
            'user_id': user_id,
            'plan': plan_type,
            'status': subscription.status.value,
            'start_date': start_date,
            'trial_end_date': trial_end_date,
            'auto_renew': False
        })
        
        # Update user's subscription plan
        self.db.collection('users').document(user_id).update({
            'subscription_plan': plan_type,
            'updated_at': datetime.utcnow()
        })
        
        return subscription
    
    async def check_subscription_access(self, user_id: str, feature: str) -> bool:
        """Check if user has access to a specific feature"""
        subscription = await self.get_user_subscription(user_id)
        if not subscription:
            return False
        
        # Check if subscription is active
        if subscription.status not in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]:
            return False
        
        # Check trial expiration
        if subscription.status == SubscriptionStatus.TRIAL:
            if subscription.trial_end_date and datetime.utcnow() > subscription.trial_end_date:
                return False
        
        # Check subscription expiration
        if subscription.end_date and datetime.utcnow() > subscription.end_date:
            return False
        
        # Get plan features
        plan = await self.get_plan_by_type(subscription.plan)
        if not plan:
            return False
        
        # Check specific feature access
        if feature == 'premium_scores':
            return plan.features.premium_scores
        elif feature == 'advanced_ml':
            return plan.features.advanced_ml_features
        elif feature == 'offline_mode':
            return plan.features.offline_mode
        elif feature == 'unlimited_sessions':
            return plan.features.max_practice_sessions == -1
        elif feature == 'unlimited_scores':
            return plan.features.max_scores_per_day == -1
        
        return True
    
    async def get_about_us(self) -> AboutUs:
        """Get about us content"""
        about_doc = self.db.collection('about_us').document('main').get()
        
        if about_doc.exists:
            about_data = about_doc.to_dict()
            return AboutUs(**about_data)
        else:
            # Return default content
            return AboutUs(
                title="Sobre o #Dô",
                description="Plataforma de prática musical com IA",
                mission="Democratizar a educação musical",
                team=[],
                image_url="/images/about/default.jpg",
                contact_email="contato@dô.com"
            )
    
    async def update_about_us(self, about_data: AboutUs) -> AboutUs:
        """Update about us content (admin function)"""
        self.db.collection('about_us').document('main').set(about_data.dict())
        return about_data
    
    async def get_payment_history(self, user_id: str) -> List[PaymentIntent]:
        """Get user's payment history"""
        payments_ref = self.db.collection('payment_intents')
        payments = payments_ref.where('user_id', '==', user_id)\
            .order_by('created_at', direction=firestore.Query.DESCENDING).get()
        
        return [PaymentIntent(**doc.to_dict()) for doc in payments]
    
    async def get_subscription_analytics(self) -> Dict[str, Any]:
        """Get subscription analytics (admin function)"""
        # Get all subscriptions
        subscriptions_ref = self.db.collection('user_subscriptions')
        subscriptions = subscriptions_ref.get()
        
        total_subscriptions = len(subscriptions)
        active_subscriptions = 0
        trial_subscriptions = 0
        plan_counts = {}
        
        for subscription in subscriptions:
            subscription_data = subscription.to_dict()
            status = subscription_data.get('status')
            plan = subscription_data.get('plan')
            
            if status == SubscriptionStatus.ACTIVE.value:
                active_subscriptions += 1
            elif status == SubscriptionStatus.TRIAL.value:
                trial_subscriptions += 1
            
            plan_counts[plan] = plan_counts.get(plan, 0) + 1
        
        return {
            'total_subscriptions': total_subscriptions,
            'active_subscriptions': active_subscriptions,
            'trial_subscriptions': trial_subscriptions,
            'plan_distribution': plan_counts,
            'conversion_rate': (active_subscriptions / total_subscriptions * 100) if total_subscriptions > 0 else 0
        }
