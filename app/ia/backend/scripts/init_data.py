"""
Initialize database with sample data
"""
import json
import uuid
from sqlalchemy.orm import Session
from ..database.connection import SessionLocal, create_tables
from ..database.models import (
    Instrument, FAQItem, Composer, Score, SubscriptionPlanDetails, AboutUs
)


def init_instruments(db: Session):
    """Initialize instruments data"""
    instruments_data = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Violino',
            'type': 'violin',
            'description': 'Instrumento de cordas friccionadas com quatro cordas (G, D, A, E)',
            'image_url': '/images/instruments/violin.jpg',
            'tuning_notes': json.dumps(['G3', 'D4', 'A4', 'E5']),
            'difficulty_level': 3,
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Flauta',
            'type': 'flute',
            'description': 'Instrumento de sopro de madeira com som doce e melodioso',
            'image_url': '/images/instruments/flute.jpg',
            'tuning_notes': json.dumps(['C4']),
            'difficulty_level': 2,
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Trompete',
            'type': 'trumpet',
            'description': 'Instrumento de sopro de metal com som brilhante e poderoso',
            'image_url': '/images/instruments/trumpet.jpg',
            'tuning_notes': json.dumps(['C4']),
            'difficulty_level': 4,
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Piano',
            'type': 'piano',
            'description': 'Instrumento de teclas com 88 teclas e ampla gama sonora',
            'image_url': '/images/instruments/piano.jpg',
            'tuning_notes': json.dumps(['A4']),
            'difficulty_level': 2,
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Violoncelo',
            'type': 'cello',
            'description': 'Instrumento de cordas friccionadas com som grave e expressivo',
            'image_url': '/images/instruments/cello.jpg',
            'tuning_notes': json.dumps(['C2', 'G2', 'D3', 'A3']),
            'difficulty_level': 4,
            'is_premium': False
        }
    ]
    
    for instrument_data in instruments_data:
        instrument = Instrument(**instrument_data)
        db.add(instrument)
    
    db.commit()
    print("✅ Instruments initialized")


def init_faq(db: Session):
    """Initialize FAQ data"""
    faq_data = [
        {
            'id': str(uuid.uuid4()),
            'question': 'Como afinar o violino?',
            'answer': 'Use um afinador eletrônico ou aplicativo. As cordas devem ser afinadas em G3, D4, A4, E5. Gire as cravelhas suavemente.',
            'instrument_type': 'violin',
            'category': 'tuning'
        },
        {
            'id': str(uuid.uuid4()),
            'question': 'Qual a postura correta para tocar violino?',
            'answer': 'Mantenha o violino apoiado no ombro esquerdo, braço relaxado, e use o queixo para segurar o instrumento.',
            'instrument_type': 'violin',
            'category': 'posture'
        },
        {
            'id': str(uuid.uuid4()),
            'question': 'Como produzir som na flauta?',
            'answer': 'Posicione os lábios no bisel, sopre suavemente e ajuste o ângulo até produzir um som claro.',
            'instrument_type': 'flute',
            'category': 'technique'
        },
        {
            'id': str(uuid.uuid4()),
            'question': 'Como posicionar as mãos no piano?',
            'answer': 'Mantenha os dedos curvados, polegares relaxados, e toque com as pontas dos dedos.',
            'instrument_type': 'piano',
            'category': 'technique'
        }
    ]
    
    for faq_item_data in faq_data:
        faq_item = FAQItem(**faq_item_data)
        db.add(faq_item)
    
    db.commit()
    print("✅ FAQ initialized")


def init_composers(db: Session):
    """Initialize composers data"""
    composers_data = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Frédéric Chopin',
            'period': 'Romantic',
            'nationality': 'Polish',
            'bio': 'Polish composer and virtuoso pianist of the Romantic era.',
            'image_url': '/images/composers/chopin.jpg',
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Johann Sebastian Bach',
            'period': 'Baroque',
            'nationality': 'German',
            'bio': 'German composer and musician of the Baroque period.',
            'image_url': '/images/composers/bach.jpg',
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Ludwig van Beethoven',
            'period': 'Classical/Romantic',
            'nationality': 'German',
            'bio': 'German composer and pianist, a crucial figure in the transition between Classical and Romantic eras.',
            'image_url': '/images/composers/beethoven.jpg',
            'is_premium': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Niccolò Paganini',
            'period': 'Romantic',
            'nationality': 'Italian',
            'bio': 'Italian violinist, violist, guitarist, and composer.',
            'image_url': '/images/composers/paganini.jpg',
            'is_premium': True
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Antonio Vivaldi',
            'period': 'Baroque',
            'nationality': 'Italian',
            'bio': 'Italian Baroque composer, virtuoso violinist, and teacher.',
            'image_url': '/images/composers/vivaldi.jpg',
            'is_premium': False
        }
    ]
    
    for composer_data in composers_data:
        composer = Composer(**composer_data)
        db.add(composer)
    
    db.commit()
    print("✅ Composers initialized")


def init_scores(db: Session):
    """Initialize scores data"""
    # Get composer IDs
    composers = db.query(Composer).all()
    composer_map = {composer.name: composer.id for composer in composers}
    
    scores_data = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Nocturne in E-flat major, Op. 9, No. 2',
            'composer_id': composer_map.get('Frédéric Chopin'),
            'instrument_type': 'piano',
            'difficulty_level': 4,
            'file_url': '/scores/chopin_nocturne_op9_no2.pdf',
            'preview_url': '/scores/previews/chopin_nocturne_preview.jpg',
            'is_premium': True,
            'duration_minutes': 4
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Cello Suite No. 1 in G major, BWV 1007 - Prelude',
            'composer_id': composer_map.get('Johann Sebastian Bach'),
            'instrument_type': 'cello',
            'difficulty_level': 5,
            'file_url': '/scores/bach_cello_suite_1_prelude.pdf',
            'preview_url': '/scores/previews/bach_cello_prelude_preview.jpg',
            'is_premium': False,
            'duration_minutes': 2
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Piano Sonata No. 14 "Moonlight" - 1st Movement',
            'composer_id': composer_map.get('Ludwig van Beethoven'),
            'instrument_type': 'piano',
            'difficulty_level': 5,
            'file_url': '/scores/beethoven_moonlight_sonata.pdf',
            'preview_url': '/scores/previews/beethoven_moonlight_preview.jpg',
            'is_premium': True,
            'duration_minutes': 6
        }
    ]
    
    for score_data in scores_data:
        if score_data['composer_id']:  # Only add if composer exists
            score = Score(**score_data)
            db.add(score)
    
    db.commit()
    print("✅ Scores initialized")


def init_subscription_plans(db: Session):
    """Initialize subscription plans"""
    plans_data = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Copper Plan',
            'plan_type': 'copper',
            'price_monthly': 5.00,
            'price_yearly': 50.00,
            'max_practice_sessions': 10,
            'max_scores_per_day': 3,
            'advanced_ml_features': False,
            'premium_scores': False,
            'priority_support': False,
            'offline_mode': False,
            'description': 'Perfect for beginners - Basic practice features',
            'is_popular': False
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Silver Plan',
            'plan_type': 'silver',
            'price_monthly': 15.00,
            'price_yearly': 150.00,
            'max_practice_sessions': 50,
            'max_scores_per_day': 10,
            'advanced_ml_features': True,
            'premium_scores': True,
            'priority_support': True,
            'offline_mode': False,
            'description': 'For serious musicians - Advanced features included',
            'is_popular': True
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Gold Plan',
            'plan_type': 'gold',
            'price_monthly': 25.00,
            'price_yearly': 250.00,
            'max_practice_sessions': -1,  # Unlimited
            'max_scores_per_day': -1,     # Unlimited
            'advanced_ml_features': True,
            'premium_scores': True,
            'priority_support': True,
            'offline_mode': True,
            'description': 'For professionals - Everything unlimited',
            'is_popular': False
        }
    ]
    
    for plan_data in plans_data:
        plan = SubscriptionPlanDetails(**plan_data)
        db.add(plan)
    
    db.commit()
    print("✅ Subscription plans initialized")


def init_about_us(db: Session):
    """Initialize about us content"""
    about_data = {
        'id': str(uuid.uuid4()),
        'title': 'Sobre o #Dô',
        'description': 'O #Dô é uma plataforma inovadora que combina tecnologia de machine learning com educação musical para ajudar músicos de todos os níveis a melhorar sua prática.',
        'mission': 'Democratizar o acesso à educação musical de qualidade através da tecnologia, oferecendo feedback em tempo real e ferramentas avançadas de prática.',
        'team': json.dumps([
            {
                'name': 'Equipe de Desenvolvimento',
                'role': 'Desenvolvedores',
                'description': 'Estudantes de Análise e Desenvolvimento de Sistemas'
            }
        ]),
        'image_url': '/images/about/orchestra.jpg',
        'contact_email': 'contato@dô.com'
    }
    
    about = AboutUs(**about_data)
    db.add(about)
    db.commit()
    print("✅ About us initialized")


def main():
    """Initialize all data"""
    print("🚀 Initializing #Dô Database...")
    
    # Create tables
    create_tables()
    print("✅ Database tables created")
    
    # Initialize data
    db = SessionLocal()
    try:
        init_instruments(db)
        init_faq(db)
        init_composers(db)
        init_scores(db)
        init_subscription_plans(db)
        init_about_us(db)
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Data initialized:")
        print("  - Instruments")
        print("  - FAQ items")
        print("  - Composers")
        print("  - Musical scores")
        print("  - Subscription plans")
        print("  - About us content")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
