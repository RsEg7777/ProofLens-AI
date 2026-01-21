"""
ProofLens AI - Subscription Plans Initialization
Run this script to create the default subscription plans in the database
"""

from app import app
from models import db, SubscriptionPlan


def init_subscription_plans():
    """Initialize default subscription plans"""
    
    with app.app_context():
        print("Initializing subscription plans...")
        
        # Check if plans already exist
        existing_plans = SubscriptionPlan.query.all()
        if existing_plans:
            print(f"Found {len(existing_plans)} existing plans. Skipping initialization.")
            print("Plans:")
            for plan in existing_plans:
                print(f"  - {plan.name}: ${plan.price}/month ({plan.credits_per_month} credits)")
            return
        
        # Create Free Plan
        free_plan = SubscriptionPlan(
            name='Free',
            price=0.00,
            credits_per_month=10,
            is_active=True
        )
        free_plan.set_features([
            '10 verifications per month',
            'Text verification',
            'Image detection',
            'Basic reports',
            'Community support'
        ])
        
        # Create Individual Plan
        individual_plan = SubscriptionPlan(
            name='Individual',
            price=9.99,
            credits_per_month=100,
            is_active=True
        )
        individual_plan.set_features([
            '100 verifications per month',
            'All verification types',
            'Video deepfake detection',
            'Audio deepfake detection',
            'URL reputation checker',
            'Export reports (PDF/JSON/CSV)',
            'Advanced analytics',
            'Priority support'
        ])
        
        # Create Enterprise Plan
        enterprise_plan = SubscriptionPlan(
            name='Enterprise',
            price=99.00,
            credits_per_month=999999,  # Effectively unlimited
            is_active=True
        )
        enterprise_plan.set_features([
            'Unlimited verifications',
            'All verification types',
            'Full API access',
            'Bulk verification',
            'Custom integrations',
            'White-label options',
            'Dedicated support',
            'SLA guarantee',
            'Custom training'
        ])
        
        # Add plans to database
        db.session.add(free_plan)
        db.session.add(individual_plan)
        db.session.add(enterprise_plan)
        
        try:
            db.session.commit()
            print("✅ Successfully created subscription plans!")
            print("\nCreated plans:")
            print(f"  1. Free: ${free_plan.price}/month - {free_plan.credits_per_month} credits")
            print(f"  2. Individual: ${individual_plan.price}/month - {individual_plan.credits_per_month} credits")
            print(f"  3. Enterprise: ${enterprise_plan.price}/month - Unlimited credits")
            print("\nUsers can now subscribe to these plans!")
            
        except Exception as e:
            print(f"❌ Error creating plans: {str(e)}")
            db.session.rollback()


def list_plans():
    """List all subscription plans"""
    
    with app.app_context():
        plans = SubscriptionPlan.query.all()
        
        if not plans:
            print("No subscription plans found.")
            print("Run 'python init_subscriptions.py' to create default plans.")
            return
        
        print(f"\n{'='*60}")
        print(f"{'ProofLens AI - Subscription Plans':^60}")
        print(f"{'='*60}\n")
        
        for plan in plans:
            print(f"Plan: {plan.name}")
            print(f"Price: ${plan.price}/month")
            print(f"Credits: {plan.credits_per_month if plan.credits_per_month < 999999 else 'Unlimited'}")
            print(f"Active: {'Yes' if plan.is_active else 'No'}")
            print(f"Features:")
            for feature in plan.get_features():
                print(f"  ✓ {feature}")
            print(f"{'-'*60}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_plans()
    else:
        init_subscription_plans()
