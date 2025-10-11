"""
Instruments Service for #Dô application
Handles instrument selection, FAQ management, and educational content
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import firebase_admin
from firebase_admin import firestore
from ..models.instrument import Instrument, FAQItem, InstrumentFAQ, InstrumentSelection, InstrumentType


class InstrumentsService:
    """Instruments and FAQ management service"""
    
    def __init__(self):
        self.db = firestore.client()
        self._initialize_instruments()
        self._initialize_faq()
    
    def _initialize_instruments(self):
        """Initialize default instruments in database"""
        instruments_data = [
            {
                'id': 'violin_001',
                'name': 'Violino',
                'type': InstrumentType.VIOLIN,
                'description': 'Instrumento de cordas friccionadas com quatro cordas (G, D, A, E)',
                'image_url': '/images/instruments/violin.jpg',
                'tuning_notes': ['G3', 'D4', 'A4', 'E5'],
                'difficulty_level': 3,
                'is_premium': False
            },
            {
                'id': 'flute_001',
                'name': 'Flauta',
                'type': InstrumentType.FLUTE,
                'description': 'Instrumento de sopro de madeira com som doce e melodioso',
                'image_url': '/images/instruments/flute.jpg',
                'tuning_notes': ['C4'],
                'difficulty_level': 2,
                'is_premium': False
            },
            {
                'id': 'trumpet_001',
                'name': 'Trompete',
                'type': InstrumentType.TRUMPET,
                'description': 'Instrumento de sopro de metal com som brilhante e poderoso',
                'image_url': '/images/instruments/trumpet.jpg',
                'tuning_notes': ['C4'],
                'difficulty_level': 4,
                'is_premium': False
            },
            {
                'id': 'piano_001',
                'name': 'Piano',
                'type': InstrumentType.PIANO,
                'description': 'Instrumento de teclas com 88 teclas e ampla gama sonora',
                'image_url': '/images/instruments/piano.jpg',
                'tuning_notes': ['A4'],
                'difficulty_level': 2,
                'is_premium': False
            },
            {
                'id': 'cello_001',
                'name': 'Violoncelo',
                'type': InstrumentType.CELLO,
                'description': 'Instrumento de cordas friccionadas com som grave e expressivo',
                'image_url': '/images/instruments/cello.jpg',
                'tuning_notes': ['C2', 'G2', 'D3', 'A3'],
                'difficulty_level': 4,
                'is_premium': False
            }
        ]
        
        # Check if instruments already exist
        instruments_ref = self.db.collection('instruments')
        existing = instruments_ref.get()
        
        if not existing:
            for instrument_data in instruments_data:
                instruments_ref.document(instrument_data['id']).set(instrument_data)
    
    def _initialize_faq(self):
        """Initialize FAQ data"""
        faq_data = {
            InstrumentType.VIOLIN: [
                {
                    'id': 'violin_faq_001',
                    'question': 'Como afinar o violino?',
                    'answer': 'Use um afinador eletrônico ou aplicativo. As cordas devem ser afinadas em G3, D4, A4, E5. Gire as cravelhas suavemente.',
                    'category': 'tuning'
                },
                {
                    'id': 'violin_faq_002',
                    'question': 'Qual a postura correta para tocar violino?',
                    'answer': 'Mantenha o violino apoiado no ombro esquerdo, braço relaxado, e use o queixo para segurar o instrumento.',
                    'category': 'posture'
                },
                {
                    'id': 'violin_faq_003',
                    'question': 'Como cuidar do violino?',
                    'answer': 'Limpe o violino após cada uso, guarde em local seco, e troque as cordas regularmente.',
                    'category': 'maintenance'
                }
            ],
            InstrumentType.FLUTE: [
                {
                    'id': 'flute_faq_001',
                    'question': 'Como produzir som na flauta?',
                    'answer': 'Posicione os lábios no bisel, sopre suavemente e ajuste o ângulo até produzir um som claro.',
                    'category': 'technique'
                },
                {
                    'id': 'flute_faq_002',
                    'question': 'Como limpar a flauta?',
                    'answer': 'Use uma flanela limpa para secar a flauta após cada uso e limpe o interior com uma vareta.',
                    'category': 'maintenance'
                }
            ],
            InstrumentType.PIANO: [
                {
                    'id': 'piano_faq_001',
                    'question': 'Como posicionar as mãos no piano?',
                    'answer': 'Mantenha os dedos curvados, polegares relaxados, e toque com as pontas dos dedos.',
                    'category': 'technique'
                },
                {
                    'id': 'piano_faq_002',
                    'question': 'Como afinar um piano?',
                    'answer': 'Afinar piano requer ferramentas especiais e conhecimento técnico. Recomenda-se contratar um afinador profissional.',
                    'category': 'tuning'
                }
            ]
        }
        
        # Store FAQ data
        for instrument_type, faq_items in faq_data.items():
            faq_ref = self.db.collection('faq').document(str(instrument_type))
            faq_ref.set({
                'instrument_type': instrument_type,
                'faq_items': faq_items,
                'updated_at': datetime.utcnow()
            })
    
    async def get_all_instruments(self) -> List[Instrument]:
        """Get all available instruments"""
        instruments_ref = self.db.collection('instruments')
        instruments = instruments_ref.get()
        
        return [Instrument(**doc.to_dict()) for doc in instruments]
    
    async def get_instrument_by_type(self, instrument_type: InstrumentType) -> Optional[Instrument]:
        """Get instrument by type"""
        instruments_ref = self.db.collection('instruments')
        instrument_query = instruments_ref.where('type', '==', instrument_type).get()
        
        if instrument_query:
            return Instrument(**instrument_query[0].to_dict())
        return None
    
    async def select_instrument(self, user_id: str, instrument_type: InstrumentType) -> InstrumentSelection:
        """Select instrument for user"""
        # Check if instrument exists
        instrument = await self.get_instrument_by_type(instrument_type)
        if not instrument:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instrument not found"
            )
        
        # Create instrument selection record
        selection_id = f"{user_id}_{instrument_type}_{datetime.utcnow().timestamp()}"
        selection = InstrumentSelection(
            user_id=user_id,
            instrument_type=instrument_type,
            selected_at=datetime.utcnow().isoformat()
        )
        
        # Store selection
        self.db.collection('instrument_selections').document(selection_id).set({
            'user_id': user_id,
            'instrument_type': instrument_type,
            'selected_at': datetime.utcnow()
        })
        
        # Update user's favorite instrument
        self.db.collection('users').document(user_id).update({
            'favorite_instrument': instrument_type,
            'updated_at': datetime.utcnow()
        })
        
        return selection
    
    async def get_faq_by_instrument(self, instrument_type: InstrumentType) -> InstrumentFAQ:
        """Get FAQ for specific instrument"""
        faq_ref = self.db.collection('faq').document(str(instrument_type))
        faq_doc = faq_ref.get()
        
        if not faq_doc.exists:
            return InstrumentFAQ(
                instrument_type=instrument_type,
                faq_items=[]
            )
        
        faq_data = faq_doc.to_dict()
        faq_items = [FAQItem(**item) for item in faq_data.get('faq_items', [])]
        
        return InstrumentFAQ(
            instrument_type=instrument_type,
            faq_items=faq_items
        )
    
    async def search_faq(self, query: str, instrument_type: Optional[InstrumentType] = None) -> List[FAQItem]:
        """Search FAQ items by query"""
        results = []
        
        if instrument_type:
            # Search in specific instrument FAQ
            faq = await self.get_faq_by_instrument(instrument_type)
            for item in faq.faq_items:
                if query.lower() in item.question.lower() or query.lower() in item.answer.lower():
                    results.append(item)
        else:
            # Search in all instruments
            instruments = await self.get_all_instruments()
            for instrument in instruments:
                faq = await self.get_faq_by_instrument(instrument.type)
                for item in faq.faq_items:
                    if query.lower() in item.question.lower() or query.lower() in item.answer.lower():
                        results.append(item)
        
        return results
    
    async def add_faq_item(self, instrument_type: InstrumentType, faq_item: FAQItem) -> FAQItem:
        """Add new FAQ item (admin function)"""
        faq_ref = self.db.collection('faq').document(str(instrument_type))
        faq_doc = faq_ref.get()
        
        if faq_doc.exists:
            faq_data = faq_doc.to_dict()
            faq_items = faq_data.get('faq_items', [])
        else:
            faq_items = []
        
        # Add new item
        faq_items.append(faq_item.dict())
        
        # Update document
        faq_ref.set({
            'instrument_type': instrument_type,
            'faq_items': faq_items,
            'updated_at': datetime.utcnow()
        })
        
        return faq_item
    
    async def update_faq_item(self, instrument_type: InstrumentType, faq_id: str, updated_item: FAQItem) -> FAQItem:
        """Update FAQ item (admin function)"""
        faq_ref = self.db.collection('faq').document(str(instrument_type))
        faq_doc = faq_ref.get()
        
        if not faq_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ not found"
            )
        
        faq_data = faq_doc.to_dict()
        faq_items = faq_data.get('faq_items', [])
        
        # Find and update item
        for i, item in enumerate(faq_items):
            if item['id'] == faq_id:
                faq_items[i] = updated_item.dict()
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ item not found"
            )
        
        # Update document
        faq_ref.update({
            'faq_items': faq_items,
            'updated_at': datetime.utcnow()
        })
        
        return updated_item
    
    async def delete_faq_item(self, instrument_type: InstrumentType, faq_id: str) -> bool:
        """Delete FAQ item (admin function)"""
        faq_ref = self.db.collection('faq').document(str(instrument_type))
        faq_doc = faq_ref.get()
        
        if not faq_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ not found"
            )
        
        faq_data = faq_doc.to_dict()
        faq_items = faq_data.get('faq_items', [])
        
        # Remove item
        faq_items = [item for item in faq_items if item['id'] != faq_id]
        
        # Update document
        faq_ref.update({
            'faq_items': faq_items,
            'updated_at': datetime.utcnow()
        })
        
        return True
