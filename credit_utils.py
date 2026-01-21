"""
Credit System Utilities and Decorators for ProofLens AI
Provides decorators for credit checking and deduction
"""

from functools import wraps
from flask import jsonify
from flask_login import current_user
from payment_handler import CreditManager
import logging

logger = logging.getLogger(__name__)


def requires_credits(credits_required=1, error_message=None):
    """
    Decorator to check and deduct credits before executing a route
    
    Args:
        credits_required (int): Number of credits required for this operation
        error_message (str): Custom error message if insufficient credits
    
    Usage:
        @app.route('/some-route')
        @login_required
        @requires_credits(credits_required=1)
        def some_route():
            # Route logic here
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401
            
            # Check if user has enough credits
            if not CreditManager.check_credits(current_user.id, credits_required):
                return jsonify({
                    'success': False,
                    'error': error_message or f'Insufficient credits. You need {credits_required} credit(s) for this operation.',
                    'credits_required': credits_required,
                    'credits_available': current_user.credits
                }), 402  # 402 Payment Required
            
            # Deduct credits
            description = f'{f.__name__.replace("_", " ").title()}'
            if not CreditManager.deduct_credits(current_user.id, credits_required, description):
                logger.error(f"Failed to deduct credits for user {current_user.id}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to process credit deduction'
                }), 500
            
            # Execute the route
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                # If route fails, refund the credits
                logger.warning(f"Route failed, refunding credits: {e}")
                CreditManager.add_credits(
                    current_user.id,
                    credits_required,
                    f'Refund: {description} failed'
                )
                raise
        
        return decorated_function
    return decorator


def check_user_credits(user_id, required_credits=1):
    """
    Check if user has sufficient credits
    
    Args:
        user_id (int): User ID
        required_credits (int): Credits required
        
    Returns:
        tuple: (has_credits: bool, current_credits: int)
    """
    has_credits = CreditManager.check_credits(user_id, required_credits)
    from models import User
    user = User.query.get(user_id)
    current_credits = user.credits if user else 0
    
    return has_credits, current_credits


def deduct_user_credits(user_id, amount, description):
    """
    Deduct credits from user account
    
    Args:
        user_id (int): User ID
        amount (int): Credits to deduct
        description (str): Description of the transaction
        
    Returns:
        bool: True if successful
    """
    return CreditManager.deduct_credits(user_id, amount, description)


def add_user_credits(user_id, amount, description):
    """
    Add credits to user account
    
    Args:
        user_id (int): User ID
        amount (int): Credits to add
        description (str): Description of the transaction
        
    Returns:
        bool: True if successful
    """
    return CreditManager.add_credits(user_id, amount, description)


def get_user_credit_info(user_id):
    """
    Get comprehensive credit information for user
    
    Args:
        user_id (int): User ID
        
    Returns:
        dict: Credit information including balance, subscription, and history
    """
    from models import User
    from payment_handler import RazorpayHandler
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    handler = RazorpayHandler()
    subscription = handler.get_user_subscription(user_id)
    
    transactions = CreditManager.get_transaction_history(user_id, limit=10)
    
    return {
        'credits': user.credits,
        'subscription': subscription,
        'recent_transactions': transactions
    }


class CreditCost:
    """Credit costs for different operations"""
    TEXT_VERIFICATION = 1
    IMAGE_VERIFICATION = 1
    VIDEO_VERIFICATION = 2
    AUDIO_VERIFICATION = 2
    URL_CHECK = 1
    BULK_VERIFICATION = 5
    EXPORT_REPORT = 0  # Free
    
    @classmethod
    def get_cost(cls, operation_type):
        """Get credit cost for operation type"""
        costs = {
            'text': cls.TEXT_VERIFICATION,
            'image': cls.IMAGE_VERIFICATION,
            'video': cls.VIDEO_VERIFICATION,
            'audio': cls.AUDIO_VERIFICATION,
            'url': cls.URL_CHECK,
            'bulk': cls.BULK_VERIFICATION,
            'export': cls.EXPORT_REPORT
        }
        return costs.get(operation_type, 1)


def format_credit_transaction(transaction):
    """
    Format transaction for display
    
    Args:
        transaction (dict): Transaction data
        
    Returns:
        dict: Formatted transaction
    """
    return {
        'id': transaction['id'],
        'amount': transaction['amount'],
        'type': transaction['type'],
        'description': transaction['description'],
        'date': transaction['created_at'],
        'is_credit': transaction['amount'] > 0
    }
