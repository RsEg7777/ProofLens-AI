"""
Database Initialization Script for ProofLens AI
Creates all tables and initializes subscription plans
"""

import sys
from app import app, db
from models import SubscriptionPlan, User
from datetime import datetime

def init_database():
    """Initialize database tables"""
    print("Initializing database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if subscription plans already exist
            existing_plans = SubscriptionPlan.query.count()
            
            if existing_plans > 0:
                print(f"✓ {existing_plans} subscription plan(s) already exist")
                return True
            
            # Create subscription plans
            plans_data = [
                {
                    'name': 'Free',
                    'price': 0.0,
                    'credits_per_month': 10,
                    'features': [
                        '10 verifications/month',
                        'Text verification',
                        'Image detection',
                        'Basic reports',
                        'Community support'
                    ],
                    'is_active': True
                },
                {
                    'name': 'Individual',
                    'price': 9.99,
                    'credits_per_month': 100,
                    'features': [
                        '100 verifications/month',
                        'All verification types',
                        'Video deepfake detection',
                        'Audio deepfake detection',
                        'URL reputation checker',
                        'Export reports (PDF/JSON/CSV)',
                        'Advanced analytics',
                        'Priority support'
                    ],
                    'is_active': True
                },
                {
                    'name': 'Enterprise',
                    'price': 0.0,  # Custom pricing
                    'credits_per_month': 999999,  # Unlimited
                    'features': [
                        'Unlimited verifications',
                        'All verification types',
                        'Full API access',
                        'Bulk verification',
                        'Custom integrations',
                        'White-label options',
                        'Dedicated support',
                        'SLA guarantee',
                        'Custom training'
                    ],
                    'is_active': True
                }
            ]
            
            # Add plans to database
            for plan_data in plans_data:
                features = plan_data.pop('features')
                plan = SubscriptionPlan(**plan_data)
                plan.set_features(features)
                db.session.add(plan)
            
            db.session.commit()
            print(f"✓ Created {len(plans_data)} subscription plans")
            
            # List created plans
            plans = SubscriptionPlan.query.all()
            print("\nCreated Plans:")
            for plan in plans:
                print(f"  - {plan.name}: ${plan.price}/month ({plan.credits_per_month} credits)")
            
            return True
            
        except Exception as e:
            print(f"✗ Error initializing database: {e}")
            db.session.rollback()
            return False

def list_plans():
    """List all subscription plans"""
    with app.app_context():
        plans = SubscriptionPlan.query.all()
        
        if not plans:
            print("No subscription plans found.")
            return
        
        print("\n" + "="*60)
        print("SUBSCRIPTION PLANS")
        print("="*60)
        
        for plan in plans:
            print(f"\n{plan.name} Plan")
            print(f"  ID: {plan.id}")
            print(f"  Price: ${plan.price}/month")
            print(f"  Credits: {plan.credits_per_month}/month")
            print(f"  Active: {'Yes' if plan.is_active else 'No'}")
            print(f"  Features:")
            for feature in plan.features:
                print(f"    - {feature}")
        
        print("\n" + "="*60)

def update_existing_users():
    """Add default credits to existing users"""
    with app.app_context():
        try:
            users_updated = 0
            users = User.query.filter(User.credits == None).all()
            
            for user in users:
                user.credits = 10  # Default free tier credits
                users_updated += 1
            
            if users_updated > 0:
                db.session.commit()
                print(f"✓ Updated {users_updated} existing user(s) with default credits")
            else:
                print("✓ All existing users already have credits assigned")
            
            return True
            
        except Exception as e:
            print(f"✗ Error updating users: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            list_plans()
        elif command == 'update-users':
            update_existing_users()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: list, update-users")
    else:
        # Default: initialize database
        print("ProofLens AI - Database Initialization")
        print("="*60)
        
        success = init_database()
        
        if success:
            print("\n✓ Database initialization complete!")
            print("\nNext steps:")
            print("1. Run 'python app.py' to start the application")
            print("2. Visit http://localhost:5000/pricing to see plans")
            print("3. Sign up for an account to get started")
        else:
            print("\n✗ Database initialization failed!")
            sys.exit(1)
