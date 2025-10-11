"""
Practice Service for #Dô application
Handles practice sessions, score management, and composer information
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import firebase_admin
from firebase_admin import firestore
from ..models.practice import (
    PracticeSession, PracticeSessionStatus, PracticeStats, 
    Composer, Score, PlayAlongSession, NoteDetection
)
from ..services.ml_service import MLService
from ..services.profile_service import ProfileService


class PracticeService:
    """Practice and score management service"""
    
    def __init__(self):
        self.db = firestore.client()
        self.ml_service = MLService()
        self.profile_service = ProfileService()
        self._initialize_composers()
        self._initialize_scores()
    
    def _initialize_composers(self):
        """Initialize composer data"""
        composers_data = [
            {
                'id': 'chopin_001',
                'name': 'Frédéric Chopin',
                'period': 'Romantic',
                'nationality': 'Polish',
                'bio': 'Polish composer and virtuoso pianist of the Romantic era.',
                'image_url': '/images/composers/chopin.jpg',
                'is_premium': False
            },
            {
                'id': 'bach_001',
                'name': 'Johann Sebastian Bach',
                'period': 'Baroque',
                'nationality': 'German',
                'bio': 'German composer and musician of the Baroque period.',
                'image_url': '/images/composers/bach.jpg',
                'is_premium': False
            },
            {
                'id': 'beethoven_001',
                'name': 'Ludwig van Beethoven',
                'period': 'Classical/Romantic',
                'nationality': 'German',
                'bio': 'German composer and pianist, a crucial figure in the transition between Classical and Romantic eras.',
                'image_url': '/images/composers/beethoven.jpg',
                'is_premium': False
            },
            {
                'id': 'paganini_001',
                'name': 'Niccolò Paganini',
                'period': 'Romantic',
                'nationality': 'Italian',
                'bio': 'Italian violinist, violist, guitarist, and composer.',
                'image_url': '/images/composers/paganini.jpg',
                'is_premium': True
            },
            {
                'id': 'vivaldi_001',
                'name': 'Antonio Vivaldi',
                'period': 'Baroque',
                'nationality': 'Italian',
                'bio': 'Italian Baroque composer, virtuoso violinist, and teacher.',
                'image_url': '/images/composers/vivaldi.jpg',
                'is_premium': False
            }
        ]
        
        # Check if composers already exist
        composers_ref = self.db.collection('composers')
        existing = composers_ref.get()
        
        if not existing:
            for composer_data in composers_data:
                composers_ref.document(composer_data['id']).set(composer_data)
    
    def _initialize_scores(self):
        """Initialize score data"""
        scores_data = [
            {
                'id': 'chopin_nocturne_001',
                'title': 'Nocturne in E-flat major, Op. 9, No. 2',
                'composer_id': 'chopin_001',
                'composer_name': 'Frédéric Chopin',
                'instrument_type': 'piano',
                'difficulty_level': 4,
                'file_url': '/scores/chopin_nocturne_op9_no2.pdf',
                'preview_url': '/scores/previews/chopin_nocturne_preview.jpg',
                'is_premium': True,
                'duration_minutes': 4
            },
            {
                'id': 'bach_cello_suite_001',
                'title': 'Cello Suite No. 1 in G major, BWV 1007 - Prelude',
                'composer_id': 'bach_001',
                'composer_name': 'Johann Sebastian Bach',
                'instrument_type': 'cello',
                'difficulty_level': 5,
                'file_url': '/scores/bach_cello_suite_1_prelude.pdf',
                'preview_url': '/scores/previews/bach_cello_prelude_preview.jpg',
                'is_premium': False,
                'duration_minutes': 2
            },
            {
                'id': 'beethoven_moonlight_001',
                'title': 'Piano Sonata No. 14 "Moonlight" - 1st Movement',
                'composer_id': 'beethoven_001',
                'composer_name': 'Ludwig van Beethoven',
                'instrument_type': 'piano',
                'difficulty_level': 5,
                'file_url': '/scores/beethoven_moonlight_sonata.pdf',
                'preview_url': '/scores/previews/beethoven_moonlight_preview.jpg',
                'is_premium': True,
                'duration_minutes': 6
            },
            {
                'id': 'paganini_caprice_001',
                'title': '24 Caprices for Solo Violin, Op. 1 - No. 1',
                'composer_id': 'paganini_001',
                'composer_name': 'Niccolò Paganini',
                'instrument_type': 'violin',
                'difficulty_level': 5,
                'file_url': '/scores/paganini_caprice_1.pdf',
                'preview_url': '/scores/previews/paganini_caprice_preview.jpg',
                'is_premium': True,
                'duration_minutes': 3
            },
            {
                'id': 'vivaldi_four_seasons_001',
                'title': 'The Four Seasons - Spring, RV 269',
                'composer_id': 'vivaldi_001',
                'composer_name': 'Antonio Vivaldi',
                'instrument_type': 'violin',
                'difficulty_level': 4,
                'file_url': '/scores/vivaldi_spring.pdf',
                'preview_url': '/scores/previews/vivaldi_spring_preview.jpg',
                'is_premium': False,
                'duration_minutes': 10
            }
        ]
        
        # Check if scores already exist
        scores_ref = self.db.collection('scores')
        existing = scores_ref.get()
        
        if not existing:
            for score_data in scores_data:
                scores_ref.document(score_data['id']).set(score_data)
    
    async def start_practice_session(self, user_id: str, instrument_type: str) -> PracticeSession:
        """Start a new practice session"""
        session_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        
        session = PracticeSession(
            id=session_id,
            user_id=user_id,
            instrument_type=instrument_type,
            start_time=datetime.utcnow(),
            status=PracticeSessionStatus.ACTIVE
        )
        
        # Store session in database
        self.db.collection('practice_sessions').document(session_id).set({
            'id': session_id,
            'user_id': user_id,
            'instrument_type': instrument_type,
            'start_time': session.start_time,
            'status': session.status.value,
            'notes_played': 0,
            'correct_notes': 0,
            'accuracy_percentage': 0.0,
            'streak_days': 0
        })
        
        return session
    
    async def update_practice_session(self, session_id: str, audio_data: bytes, target_notes: List[str]) -> Dict[str, Any]:
        """Update practice session with new audio data"""
        session_ref = self.db.collection('practice_sessions').document(session_id)
        session_doc = session_ref.get()
        
        if not session_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice session not found"
            )
        
        session_data = session_doc.to_dict()
        
        # Analyze audio with ML service
        analysis = await self.ml_service.analyze_practice_session([audio_data], target_notes)
        
        # Update session statistics
        current_notes_played = session_data.get('notes_played', 0) + analysis['total_notes']
        current_correct_notes = session_data.get('correct_notes', 0) + analysis['correct_notes']
        
        # Calculate overall accuracy
        overall_accuracy = (current_correct_notes / current_notes_played * 100) if current_notes_played > 0 else 0
        
        # Update database
        session_ref.update({
            'notes_played': current_notes_played,
            'correct_notes': current_correct_notes,
            'accuracy_percentage': round(overall_accuracy, 2),
            'updated_at': datetime.utcnow()
        })
        
        return {
            'session_id': session_id,
            'current_accuracy': round(overall_accuracy, 2),
            'notes_played': current_notes_played,
            'correct_notes': current_correct_notes,
            'analysis': analysis
        }
    
    async def end_practice_session(self, session_id: str) -> PracticeSession:
        """End practice session and update statistics"""
        session_ref = self.db.collection('practice_sessions').document(session_id)
        session_doc = session_ref.get()
        
        if not session_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice session not found"
            )
        
        session_data = session_doc.to_dict()
        end_time = datetime.utcnow()
        start_time = session_data['start_time']
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        
        # Update session
        session_ref.update({
            'end_time': end_time,
            'duration_minutes': duration_minutes,
            'status': PracticeSessionStatus.COMPLETED.value,
            'updated_at': end_time
        })
        
        # Update user streak
        user_id = session_data['user_id']
        await self.profile_service.update_practice_streak(user_id, increment=True)
        
        # Create completed session object
        return PracticeSession(
            id=session_data['id'],
            user_id=session_data['user_id'],
            instrument_type=session_data['instrument_type'],
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes,
            status=PracticeSessionStatus.COMPLETED,
            notes_played=session_data.get('notes_played', 0),
            correct_notes=session_data.get('correct_notes', 0),
            accuracy_percentage=session_data.get('accuracy_percentage', 0.0),
            streak_days=session_data.get('streak_days', 0)
        )
    
    async def get_practice_stats(self, user_id: str) -> PracticeStats:
        """Get practice statistics for user"""
        sessions_ref = self.db.collection('practice_sessions')
        sessions = sessions_ref.where('user_id', '==', user_id).get()
        
        total_practice_time = 0
        total_sessions = len(sessions)
        accuracy_sum = 0
        current_streak = 0
        longest_streak = 0
        last_practice = None
        
        # Calculate statistics
        for session in sessions:
            session_data = session.to_dict()
            total_practice_time += session_data.get('duration_minutes', 0)
            accuracy_sum += session_data.get('accuracy_percentage', 0)
            
            if session_data.get('start_time'):
                if last_practice is None or session_data['start_time'] > last_practice:
                    last_practice = session_data['start_time']
        
        average_accuracy = accuracy_sum / total_sessions if total_sessions > 0 else 0
        
        # Get user's favorite instrument
        user_doc = self.db.collection('users').document(user_id).get()
        favorite_instrument = "piano"  # default
        if user_doc.exists:
            user_data = user_doc.to_dict()
            favorite_instrument = user_data.get('favorite_instrument', 'piano')
        
        return PracticeStats(
            user_id=user_id,
            total_practice_time=total_practice_time,
            current_streak=current_streak,
            longest_streak=longest_streak,
            total_sessions=total_sessions,
            average_accuracy=round(average_accuracy, 2),
            favorite_instrument=favorite_instrument,
            last_practice=last_practice
        )
    
    async def get_all_composers(self) -> List[Composer]:
        """Get all composers"""
        composers_ref = self.db.collection('composers')
        composers = composers_ref.get()
        
        return [Composer(**doc.to_dict()) for doc in composers]
    
    async def get_composer_by_id(self, composer_id: str) -> Optional[Composer]:
        """Get composer by ID"""
        composer_doc = self.db.collection('composers').document(composer_id).get()
        
        if composer_doc.exists:
            return Composer(**composer_doc.to_dict())
        return None
    
    async def get_scores_by_composer(self, composer_id: str) -> List[Score]:
        """Get scores by composer"""
        scores_ref = self.db.collection('scores')
        scores = scores_ref.where('composer_id', '==', composer_id).get()
        
        return [Score(**doc.to_dict()) for doc in scores]
    
    async def get_scores_by_instrument(self, instrument_type: str, user_subscription: str = "copper") -> List[Score]:
        """Get scores by instrument type"""
        scores_ref = self.db.collection('scores')
        scores = scores_ref.where('instrument_type', '==', instrument_type).get()
        
        # Filter by subscription level
        filtered_scores = []
        for score in scores:
            score_data = score.to_dict()
            if not score_data.get('is_premium', False) or user_subscription in ['silver', 'gold']:
                filtered_scores.append(Score(**score_data))
        
        return filtered_scores
    
    async def get_score_by_id(self, score_id: str) -> Optional[Score]:
        """Get score by ID"""
        score_doc = self.db.collection('scores').document(score_id).get()
        
        if score_doc.exists:
            return Score(**score_doc.to_dict())
        return None
    
    async def start_play_along_session(self, user_id: str, score_id: str) -> PlayAlongSession:
        """Start play-along session with a score"""
        # Get score information
        score = await self.get_score_by_id(score_id)
        if not score:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Score not found"
            )
        
        session_id = f"play_along_{user_id}_{datetime.utcnow().timestamp()}"
        
        session = PlayAlongSession(
            id=session_id,
            user_id=user_id,
            score_id=score_id,
            start_time=datetime.utcnow(),
            notes_detected=[],
            accuracy_score=0.0,
            is_completed=False
        )
        
        # Store session
        self.db.collection('play_along_sessions').document(session_id).set({
            'id': session_id,
            'user_id': user_id,
            'score_id': score_id,
            'start_time': session.start_time,
            'notes_detected': [],
            'accuracy_score': 0.0,
            'is_completed': False
        })
        
        return session
    
    async def update_play_along_session(self, session_id: str, audio_data: bytes) -> Dict[str, Any]:
        """Update play-along session with new audio data"""
        session_ref = self.db.collection('play_along_sessions').document(session_id)
        session_doc = session_ref.get()
        
        if not session_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Play-along session not found"
            )
        
        # Detect notes from audio
        note_detection = await self.ml_service.detect_note(audio_data)
        
        # Update session with new detection
        session_data = session_doc.to_dict()
        notes_detected = session_data.get('notes_detected', [])
        notes_detected.append(note_detection.dict())
        
        # Calculate accuracy score
        total_notes = len(notes_detected)
        correct_notes = sum(1 for note in notes_detected if note['accuracy'] in ['perfect', 'good'])
        accuracy_score = (correct_notes / total_notes * 100) if total_notes > 0 else 0
        
        # Update database
        session_ref.update({
            'notes_detected': notes_detected,
            'accuracy_score': round(accuracy_score, 2),
            'updated_at': datetime.utcnow()
        })
        
        return {
            'session_id': session_id,
            'note_detected': note_detection.dict(),
            'total_notes': total_notes,
            'accuracy_score': round(accuracy_score, 2)
        }
    
    async def complete_play_along_session(self, session_id: str) -> PlayAlongSession:
        """Complete play-along session"""
        session_ref = self.db.collection('play_along_sessions').document(session_id)
        session_doc = session_ref.get()
        
        if not session_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Play-along session not found"
            )
        
        session_data = session_doc.to_dict()
        end_time = datetime.utcnow()
        
        # Update session
        session_ref.update({
            'end_time': end_time,
            'is_completed': True,
            'updated_at': end_time
        })
        
        return PlayAlongSession(
            id=session_data['id'],
            user_id=session_data['user_id'],
            score_id=session_data['score_id'],
            start_time=session_data['start_time'],
            end_time=end_time,
            notes_detected=[NoteDetection(**note) for note in session_data.get('notes_detected', [])],
            accuracy_score=session_data.get('accuracy_score', 0.0),
            is_completed=True
        )
    
    async def get_user_practice_history(self, user_id: str, limit: int = 10) -> List[PracticeSession]:
        """Get user's practice history"""
        sessions_ref = self.db.collection('practice_sessions')
        sessions = sessions_ref.where('user_id', '==', user_id)\
            .order_by('start_time', direction=firestore.Query.DESCENDING)\
            .limit(limit).get()
        
        practice_sessions = []
        for session in sessions:
            session_data = session.to_dict()
            practice_sessions.append(PracticeSession(**session_data))
        
        return practice_sessions
