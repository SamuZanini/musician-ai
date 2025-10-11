"""
Practice model for the #Dô application
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PracticeSessionStatus(str, Enum):
    """Practice session status"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class NoteAccuracy(str, Enum):
    """Note accuracy levels"""
    PERFECT = "perfect"  # ±5 cents
    GOOD = "good"       # ±10 cents
    FAIR = "fair"       # ±20 cents
    POOR = "poor"       # >±20 cents


class PracticeSession(BaseModel):
    """Practice session model"""
    id: str
    user_id: str
    instrument_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: int = 0
    status: PracticeSessionStatus = PracticeSessionStatus.ACTIVE
    notes_played: int = 0
    correct_notes: int = 0
    accuracy_percentage: float = 0.0
    streak_days: int = 0


class NoteDetection(BaseModel):
    """Note detection result"""
    note: str  # e.g., "C4", "D#5"
    frequency: float
    confidence: float  # 0.0 to 1.0
    accuracy: NoteAccuracy
    timestamp: datetime


class TuningResult(BaseModel):
    """Tuning result model"""
    target_note: str
    detected_note: str
    frequency: float
    cents_offset: float  # -50 to +50
    is_in_tune: bool  # within ±5 cents
    confidence: float


class PracticeStats(BaseModel):
    """Practice statistics"""
    user_id: str
    total_practice_time: int  # in minutes
    current_streak: int  # days
    longest_streak: int  # days
    total_sessions: int
    average_accuracy: float
    favorite_instrument: str
    last_practice: Optional[datetime] = None


class Composer(BaseModel):
    """Composer model"""
    id: str
    name: str
    period: str  # e.g., "Baroque", "Classical", "Romantic"
    nationality: str
    bio: str
    image_url: str
    is_premium: bool = False


class Score(BaseModel):
    """Musical score model"""
    id: str
    title: str
    composer_id: str
    composer_name: str
    instrument_type: str
    difficulty_level: int  # 1-5
    file_url: str  # URL to score file
    preview_url: Optional[str] = None
    is_premium: bool = False
    duration_minutes: Optional[int] = None


class PlayAlongSession(BaseModel):
    """Play-along session model"""
    id: str
    user_id: str
    score_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    notes_detected: List[NoteDetection]
    accuracy_score: float
    is_completed: bool = False
