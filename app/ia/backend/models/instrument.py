"""
Instrument model for the #Dô application
"""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class InstrumentType(str, Enum):
    """Instrument types"""
    VIOLIN = "violin"
    FLUTE = "flute"
    TRUMPET = "trumpet"
    PIANO = "piano"
    CELLO = "cello"


class Instrument(BaseModel):
    """Instrument model"""
    id: str
    name: str
    type: InstrumentType
    description: str
    image_url: str
    tuning_notes: List[str]  # Standard tuning notes
    difficulty_level: int  # 1-5 scale
    is_premium: bool = False


class FAQItem(BaseModel):
    """FAQ item model"""
    id: str
    question: str
    answer: str
    instrument_type: InstrumentType
    category: str  # e.g., "tuning", "practice", "maintenance"


class InstrumentFAQ(BaseModel):
    """FAQ for a specific instrument"""
    instrument_type: InstrumentType
    faq_items: List[FAQItem]


class InstrumentSelection(BaseModel):
    """Instrument selection model"""
    user_id: str
    instrument_type: InstrumentType
    selected_at: str  # ISO datetime string
