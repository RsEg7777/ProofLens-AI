"""
Razorpay Payment Integration for ProofLens AI
Handles subscription payments, order creation, and verification
"""

import razorpay
from datetime import datetime, timedelta
from config import Config
from models import db, UserSubscription, SubscriptionPlan, CreditTransaction, User
import logging

logger = logging.getLogger(__name__)


class RazorpayHandler:
    """Handle Razorpay payment operations"""
    
    def __init__(self):
        """Initialize Razorpay client"""
        self.client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))
        self.client.set_app_details({"title": "ProofLens AI", "version": "1.0"})
    
    def create_order(self, amount, currency='INR', receipt=None, notes=None):
        """
        Create a Razorpay order
        
        Args:
            amount (int): Amount in paise (multiply rupees by 100)
            currency (str): Currency code (default: INR)
            receipt (str): Receipt ID for reference
            notes (dict): Additional notes
            
        Returns:
            dict: Order details or None on error
        """
        try:
            order_data = {
                'amount': amount,
                'currency': currency,
                'receipt': receipt or f'order_{datetime.utcnow().timestamp()}',
                'notes': notes or {}
            }
            
            order = self.client.order.create(data=order_data)
            logger.info(f"Created Razorpay order: {order['id']}")
            return order
            
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {e}")
            return None
    
    def verify_payment_signature(self, payment_id, order_id, signature):
        """
        Verify Razorpay payment signature
        
        Args:
            payment_id (str): Razorpay payment ID
            order_id (str): Razorpay order ID
            signature (str): Payment signature
            
        Returns:
            bool: True if signature is valid
        """
        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment signature verified: {payment_id}")
            return True
            
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"Payment signature verification failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            return False
    
    def fetch_payment(self, payment_id):
        """
        Fetch payment details
        
        Args:
            payment_id (str): Razorpay payment ID
            
        Returns:
            dict: Payment details or None
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            logger.error(f"Error fetching payment: {e}")
            return None
    
    def create_subscription_order(self, user_id, plan_id):
        """
        Create order for subscription purchase
        
        Args:
            user_id (int): User ID
            plan_id (int): Subscription plan ID
            
        Returns:
            dict: Order details with plan info or None
        """
        try:
            # Get plan details
            plan = SubscriptionPlan.query.get(plan_id)
            if not plan or not plan.is_active:
                logger.error(f"Invalid or inactive plan: {plan_id}")
                return None
            
            # Free plan doesn't need payment
            if plan.price == 0:
                return self.activate_free_subscription(user_id, plan_id)
            
            # Create order
            amount = int(plan.price * 100)  # Convert to paise
            receipt = f'sub_{user_id}_{plan_id}_{int(datetime.utcnow().timestamp())}'
            notes = {
                'user_id': user_id,
                'plan_id': plan_id,
                'plan_name': plan.name
            }
            
            order = self.create_order(amount, receipt=receipt, notes=notes)
            
            if order:
                return {
                    'order': order,
                    'plan': {
                        'id': plan.id,
                        'name': plan.name,
                        'price': plan.price,
                        'credits': plan.credits_per_month
                    }
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating subscription order: {e}")
            return None
    
    def activate_free_subscription(self, user_id, plan_id):
        """
        Activate free subscription without payment
        
        Args:
            user_id (int): User ID
            plan_id (int): Plan ID (must be free plan)
            
        Returns:
            dict: Subscription details or None
        """
        try:
            plan = SubscriptionPlan.query.get(plan_id)
            if not plan or plan.price != 0:
                return None
            
            # Deactivate any existing subscriptions
            UserSubscription.query.filter_by(user_id=user_id).update({
                'status': 'cancelled'
            })
            
            # Create new subscription
            now = datetime.utcnow()
            subscription = UserSubscription(
                user_id=user_id,
                plan_id=plan_id,
                status='active',
                current_period_start=now,
                current_period_end=now + timedelta(days=30)
            )
            
            db.session.add(subscription)
            
            # Update user credits
            user = User.query.get(user_id)
            user.credits = plan.credits_per_month
            
            # Log credit transaction
            transaction = CreditTransaction(
                user_id=user_id,
                amount=plan.credits_per_month,
                transaction_type='credit',
                description=f'Monthly credits for {plan.name} plan'
            )
            db.session.add(transaction)
            
            db.session.commit()
            
            logger.info(f"Activated free subscription for user {user_id}")
            return {
                'subscription_id': subscription.id,
                'plan_name': plan.name,
                'credits': plan.credits_per_month
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error activating free subscription: {e}")
            return None
    
    def activate_paid_subscription(self, user_id, plan_id, payment_id, order_id):
        """
        Activate paid subscription after successful payment
        
        Args:
            user_id (int): User ID
            plan_id (int): Plan ID
            payment_id (str): Razorpay payment ID
            order_id (str): Razorpay order ID
            
        Returns:
            dict: Subscription details or None
        """
        try:
            plan = SubscriptionPlan.query.get(plan_id)
            if not plan:
                return None
            
            # Deactivate existing subscriptions
            UserSubscription.query.filter_by(user_id=user_id).update({
                'status': 'cancelled'
            })
            
            # Create new subscription
            now = datetime.utcnow()
            subscription = UserSubscription(
                user_id=user_id,
                plan_id=plan_id,
                status='active',
                current_period_start=now,
                current_period_end=now + timedelta(days=30),
                stripe_subscription_id=payment_id  # Store payment ID for reference
            )
            
            db.session.add(subscription)
            
            # Update user credits
            user = User.query.get(user_id)
            user.credits = plan.credits_per_month
            user.subscription_id = subscription.id
            
            # Log credit transaction
            transaction = CreditTransaction(
                user_id=user_id,
                amount=plan.credits_per_month,
                transaction_type='credit',
                description=f'Subscription: {plan.name} - Payment: {payment_id}'
            )
            db.session.add(transaction)
            
            db.session.commit()
            
            logger.info(f"Activated paid subscription for user {user_id}, plan {plan.name}")
            return {
                'subscription_id': subscription.id,
                'plan_name': plan.name,
                'credits': plan.credits_per_month,
                'payment_id': payment_id
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error activating paid subscription: {e}")
            return None
    
    def cancel_subscription(self, user_id):
        """
        Cancel user's active subscription
        
        Args:
            user_id (int): User ID
            
        Returns:
            bool: True if cancelled successfully
        """
        try:
            subscription = UserSubscription.query.filter_by(
                user_id=user_id,
                status='active'
            ).first()
            
            if not subscription:
                return False
            
            subscription.status = 'cancelled'
            
            # Update user
            user = User.query.get(user_id)
            user.subscription_id = None
            
            db.session.commit()
            
            logger.info(f"Cancelled subscription for user {user_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error cancelling subscription: {e}")
            return False
    
    def get_user_subscription(self, user_id):
        """
        Get user's current subscription details
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Subscription details or None
        """
        try:
            subscription = UserSubscription.query.filter_by(
                user_id=user_id,
                status='active'
            ).first()
            
            if not subscription:
                return None
            
            plan = SubscriptionPlan.query.get(subscription.plan_id)
            
            return {
                'subscription_id': subscription.id,
                'plan_name': plan.name,
                'plan_price': plan.price,
                'credits_per_month': plan.credits_per_month,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'days_remaining': (subscription.current_period_end - datetime.utcnow()).days
            }
            
        except Exception as e:
            logger.error(f"Error getting user subscription: {e}")
            return None


class CreditManager:
    """Manage user credits and transactions"""
    
    @staticmethod
    def check_credits(user_id, required_credits=1):
        """
        Check if user has enough credits
        
        Args:
            user_id (int): User ID
            required_credits (int): Credits required
            
        Returns:
            bool: True if user has enough credits
        """
        try:
            user = User.query.get(user_id)
            return user and user.credits >= required_credits
        except Exception as e:
            logger.error(f"Error checking credits: {e}")
            return False
    
    @staticmethod
    def deduct_credits(user_id, amount, description):
        """
        Deduct credits from user account
        
        Args:
            user_id (int): User ID
            amount (int): Credits to deduct
            description (str): Transaction description
            
        Returns:
            bool: True if deducted successfully
        """
        try:
            user = User.query.get(user_id)
            
            if not user or user.credits < amount:
                return False
            
            user.credits -= amount
            
            # Log transaction
            transaction = CreditTransaction(
                user_id=user_id,
                amount=-amount,
                transaction_type='debit',
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            
            logger.info(f"Deducted {amount} credits from user {user_id}: {description}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deducting credits: {e}")
            return False
    
    @staticmethod
    def add_credits(user_id, amount, description):
        """
        Add credits to user account
        
        Args:
            user_id (int): User ID
            amount (int): Credits to add
            description (str): Transaction description
            
        Returns:
            bool: True if added successfully
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return False
            
            user.credits += amount
            
            # Log transaction
            transaction = CreditTransaction(
                user_id=user_id,
                amount=amount,
                transaction_type='credit',
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            
            logger.info(f"Added {amount} credits to user {user_id}: {description}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding credits: {e}")
            return False
    
    @staticmethod
    def get_transaction_history(user_id, limit=50):
        """
        Get user's credit transaction history
        
        Args:
            user_id (int): User ID
            limit (int): Max transactions to return
            
        Returns:
            list: Transaction records
        """
        try:
            transactions = CreditTransaction.query.filter_by(
                user_id=user_id
            ).order_by(CreditTransaction.created_at.desc()).limit(limit).all()
            
            return [{
                'id': t.id,
                'amount': t.amount,
                'type': t.transaction_type,
                'description': t.description,
                'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for t in transactions]
            
        except Exception as e:
            logger.error(f"Error getting transaction history: {e}")
            return []
