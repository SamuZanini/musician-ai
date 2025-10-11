"""
ML API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from ..models.practice import NoteDetection, TuningResult
from ..models.user import User
from ..services.ml_service import MLService

router = APIRouter(prefix="/ml", tags=["Machine Learning"])
ml_service = MLService()


async def get_current_user() -> User:
    """Get current authenticated user"""
    # This would be implemented with proper JWT validation
    pass


@router.post("/detect-note", response_model=NoteDetection)
async def detect_note(audio_data: bytes):
    """Detect note from audio data"""
    try:
        detection = await ml_service.detect_note(audio_data)
        return detection
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/tune", response_model=TuningResult)
async def tune_instrument(
    audio_data: bytes,
    target_note: str
):
    """Tune instrument to target note"""
    try:
        result = await ml_service.tune_instrument(audio_data, target_note)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/detect-chord", response_model=Dict[str, Any])
async def detect_chord(audio_data: bytes):
    """Detect chord from audio data"""
    try:
        result = await ml_service.detect_chord(audio_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/analyze-session", response_model=Dict[str, Any])
async def analyze_practice_session(
    audio_data: List[bytes],
    target_notes: List[str]
):
    """Analyze practice session for accuracy and feedback"""
    try:
        result = await ml_service.analyze_practice_session(audio_data, target_notes)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/tuning-notes/{instrument_type}")
async def get_tuning_notes(instrument_type: str):
    """Get standard tuning notes for instrument"""
    try:
        notes = ml_service.get_tuning_notes_for_instrument(instrument_type)
        return {"instrument_type": instrument_type, "tuning_notes": notes}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
