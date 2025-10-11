"""
Practice API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any
from ..models.practice import PracticeSession, PracticeStats, Composer, Score, PlayAlongSession
from ..models.user import User
from ..services.practice_service import PracticeService

router = APIRouter(prefix="/practice", tags=["Practice"])
practice_service = PracticeService()


async def get_current_user() -> User:
    """Get current authenticated user"""
    # This would be implemented with proper JWT validation
    pass


@router.post("/sessions", response_model=PracticeSession)
async def start_practice_session(
    instrument_type: str,
    current_user: User = Depends(get_current_user)
):
    """Start a new practice session"""
    try:
        session = await practice_service.start_practice_session(
            current_user.id, instrument_type
        )
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/sessions/{session_id}")
async def update_practice_session(
    session_id: str,
    audio_data: bytes,
    target_notes: List[str]
):
    """Update practice session with new audio data"""
    try:
        result = await practice_service.update_practice_session(
            session_id, audio_data, target_notes
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/sessions/{session_id}/end", response_model=PracticeSession)
async def end_practice_session(session_id: str):
    """End practice session and update statistics"""
    try:
        session = await practice_service.end_practice_session(session_id)
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/statistics", response_model=PracticeStats)
async def get_practice_stats(current_user: User = Depends(get_current_user)):
    """Get practice statistics for user"""
    try:
        stats = await practice_service.get_practice_stats(current_user.id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/history", response_model=List[PracticeSession])
async def get_practice_history(
    limit: int = Query(10, description="Number of sessions to return"),
    current_user: User = Depends(get_current_user)
):
    """Get user's practice history"""
    try:
        history = await practice_service.get_user_practice_history(
            current_user.id, limit
        )
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/composers", response_model=List[Composer])
async def get_all_composers():
    """Get all composers"""
    try:
        composers = await practice_service.get_all_composers()
        return composers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/composers/{composer_id}", response_model=Composer)
async def get_composer_by_id(composer_id: str):
    """Get composer by ID"""
    try:
        composer = await practice_service.get_composer_by_id(composer_id)
        if not composer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Composer not found"
            )
        return composer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/scores", response_model=List[Score])
async def get_scores(
    composer_id: str = Query(None, description="Filter by composer"),
    instrument_type: str = Query(None, description="Filter by instrument type")
):
    """Get scores with optional filters"""
    try:
        if composer_id:
            scores = await practice_service.get_scores_by_composer(composer_id)
        elif instrument_type:
            scores = await practice_service.get_scores_by_instrument(instrument_type)
        else:
            # Get all scores (this would need to be implemented)
            scores = []
        return scores
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/scores/{score_id}", response_model=Score)
async def get_score_by_id(score_id: str):
    """Get score by ID"""
    try:
        score = await practice_service.get_score_by_id(score_id)
        if not score:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Score not found"
            )
        return score
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/play-along", response_model=PlayAlongSession)
async def start_play_along_session(
    score_id: str,
    current_user: User = Depends(get_current_user)
):
    """Start play-along session with a score"""
    try:
        session = await practice_service.start_play_along_session(
            current_user.id, score_id
        )
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/play-along/{session_id}")
async def update_play_along_session(
    session_id: str,
    audio_data: bytes
):
    """Update play-along session with new audio data"""
    try:
        result = await practice_service.update_play_along_session(
            session_id, audio_data
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/play-along/{session_id}/complete", response_model=PlayAlongSession)
async def complete_play_along_session(session_id: str):
    """Complete play-along session"""
    try:
        session = await practice_service.complete_play_along_session(session_id)
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
