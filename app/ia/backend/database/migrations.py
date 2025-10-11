"""
Database migration utilities for #Dô application
Helps migrate from SQLite to PostgreSQL (Supabase)
"""
import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .connection import Base, engine as sqlite_engine
from .models import *


def export_sqlite_data():
    """Export all data from SQLite database"""
    print("📤 Exporting data from SQLite...")
    
    # Create SQLite session
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SQLiteSession()
    
    try:
        # Export all tables
        data = {}
        
        # Users
        users = sqlite_session.query(User).all()
        data['users'] = [{
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'password_hash': user.password_hash,
            'avatar_url': user.avatar_url,
            'favorite_instrument': user.favorite_instrument.value if user.favorite_instrument else None,
            'subscription_plan': user.subscription_plan.value,
            'role': user.role.value,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_active': user.is_active,
            'practice_streak': user.practice_streak,
            'total_practice_time': user.total_practice_time
        } for user in users]
        
        # Instruments
        instruments = sqlite_session.query(Instrument).all()
        data['instruments'] = [{
            'id': instrument.id,
            'name': instrument.name,
            'type': instrument.type.value,
            'description': instrument.description,
            'image_url': instrument.image_url,
            'tuning_notes': instrument.tuning_notes,
            'difficulty_level': instrument.difficulty_level,
            'is_premium': instrument.is_premium,
            'created_at': instrument.created_at.isoformat() if instrument.created_at else None
        } for instrument in instruments]
        
        # FAQ Items
        faq_items = sqlite_session.query(FAQItem).all()
        data['faq_items'] = [{
            'id': item.id,
            'question': item.question,
            'answer': item.answer,
            'instrument_type': item.instrument_type.value,
            'category': item.category,
            'created_at': item.created_at.isoformat() if item.created_at else None
        } for item in faq_items]
        
        # Composers
        composers = sqlite_session.query(Composer).all()
        data['composers'] = [{
            'id': composer.id,
            'name': composer.name,
            'period': composer.period,
            'nationality': composer.nationality,
            'bio': composer.bio,
            'image_url': composer.image_url,
            'is_premium': composer.is_premium,
            'created_at': composer.created_at.isoformat() if composer.created_at else None
        } for composer in composers]
        
        # Scores
        scores = sqlite_session.query(Score).all()
        data['scores'] = [{
            'id': score.id,
            'title': score.title,
            'composer_id': score.composer_id,
            'instrument_type': score.instrument_type,
            'difficulty_level': score.difficulty_level,
            'file_url': score.file_url,
            'preview_url': score.preview_url,
            'is_premium': score.is_premium,
            'duration_minutes': score.duration_minutes,
            'created_at': score.created_at.isoformat() if score.created_at else None
        } for score in scores]
        
        # Subscription Plans
        plans = sqlite_session.query(SubscriptionPlanDetails).all()
        data['subscription_plans'] = [{
            'id': plan.id,
            'name': plan.name,
            'plan_type': plan.plan_type.value,
            'price_monthly': float(plan.price_monthly),
            'price_yearly': float(plan.price_yearly),
            'max_practice_sessions': plan.max_practice_sessions,
            'max_scores_per_day': plan.max_scores_per_day,
            'advanced_ml_features': plan.advanced_ml_features,
            'premium_scores': plan.premium_scores,
            'priority_support': plan.priority_support,
            'offline_mode': plan.offline_mode,
            'description': plan.description,
            'is_popular': plan.is_popular,
            'created_at': plan.created_at.isoformat() if plan.created_at else None
        } for plan in plans]
        
        # Save to JSON file
        with open('data_export.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(users)} users, {len(instruments)} instruments, {len(composers)} composers")
        print("📄 Data saved to data_export.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False
    finally:
        sqlite_session.close()


def import_to_postgresql(postgres_url: str):
    """Import data to PostgreSQL database"""
    print("📥 Importing data to PostgreSQL...")
    
    # Create PostgreSQL engine
    postgres_engine = create_engine(postgres_url)
    PostgresSession = sessionmaker(bind=postgres_engine)
    postgres_session = PostgresSession()
    
    try:
        # Load data from JSON
        with open('data_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create tables
        Base.metadata.create_all(bind=postgres_engine)
        
        # Import users
        for user_data in data.get('users', []):
            user = User(**user_data)
            postgres_session.add(user)
        
        # Import instruments
        for instrument_data in data.get('instruments', []):
            instrument = Instrument(**instrument_data)
            postgres_session.add(instrument)
        
        # Import FAQ items
        for faq_data in data.get('faq_items', []):
            faq_item = FAQItem(**faq_data)
            postgres_session.add(faq_item)
        
        # Import composers
        for composer_data in data.get('composers', []):
            composer = Composer(**composer_data)
            postgres_session.add(composer)
        
        # Import scores
        for score_data in data.get('scores', []):
            score = Score(**score_data)
            postgres_session.add(score)
        
        # Import subscription plans
        for plan_data in data.get('subscription_plans', []):
            plan = SubscriptionPlanDetails(**plan_data)
            postgres_session.add(plan)
        
        postgres_session.commit()
        print("✅ Data imported successfully to PostgreSQL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        postgres_session.rollback()
        return False
    finally:
        postgres_session.close()


def migrate_to_supabase():
    """Complete migration to Supabase"""
    print("🚀 Migrating to Supabase...")
    
    # Get Supabase URL from environment
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url or not postgres_url.startswith("postgresql://"):
        print("❌ Please set DATABASE_URL to your Supabase PostgreSQL URL")
        return False
    
    # Export from SQLite
    if not export_sqlite_data():
        return False
    
    # Import to PostgreSQL
    if not import_to_postgresql(postgres_url):
        return False
    
    print("🎉 Migration to Supabase completed successfully!")
    print("\nNext steps:")
    print("1. Update your .env file with the new DATABASE_URL")
    print("2. Test the application with the new database")
    print("3. Remove the SQLite database file if everything works")
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        migrate_to_supabase()
    else:
        print("Usage: python migrations.py migrate")
        print("This will migrate your SQLite data to Supabase")
