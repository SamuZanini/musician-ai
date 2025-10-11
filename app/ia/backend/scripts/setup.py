"""
Setup script for #Dô Backend
Initializes database tables and sample data
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import create_tables
from scripts.init_data import main as init_data


def setup_database():
    """Initialize database with sample data"""
    print("🚀 Setting up #Dô Backend Database...")
    
    try:
        # Create database tables
        print("📊 Creating database tables...")
        create_tables()
        
        # Initialize sample data
        print("📝 Initializing sample data...")
        init_data()
        
        print("✅ Database setup completed successfully!")
        print("\n📋 Tables created:")
        print("  - users")
        print("  - instruments")
        print("  - faq_items")
        print("  - composers")
        print("  - scores")
        print("  - practice_sessions")
        print("  - play_along_sessions")
        print("  - subscription_plans")
        print("  - user_subscriptions")
        print("  - payment_intents")
        print("  - about_us")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    
    return True


def verify_setup():
    """Verify that setup was successful"""
    print("\n🔍 Verifying setup...")
    
    try:
        from database.connection import SessionLocal
        from database.models import Instrument, Composer, SubscriptionPlanDetails
        
        db = SessionLocal()
        
        # Check instruments
        instruments_count = db.query(Instrument).count()
        print(f"✅ Found {instruments_count} instruments")
        
        # Check composers
        composers_count = db.query(Composer).count()
        print(f"✅ Found {composers_count} composers")
        
        # Check subscription plans
        plans_count = db.query(SubscriptionPlanDetails).count()
        print(f"✅ Found {plans_count} subscription plans")
        
        db.close()
        print("✅ Setup verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Setup verification failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🎵 #Dô - Assistente de Prática Musical")
    print("=" * 50)
    
    # Check environment variables
    required_env_vars = [
        "SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease configure your .env file with the required variables.")
        return False
    
    # Setup database
    success = setup_database()
    if not success:
        return False
    
    # Verify setup
    success = verify_setup()
    if not success:
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python start_server.py")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Run tests: python run_tests.py")
    
    return True


if __name__ == "__main__":
    main()
