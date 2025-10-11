"""
Instruments API endpoints for #Dô application
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from ..models.instrument import Instrument, InstrumentFAQ, InstrumentSelection, InstrumentType
from ..models.user import User
from ..services.instruments_service import InstrumentsService

router = APIRouter(prefix="/instruments", tags=["Instruments"])
instruments_service = InstrumentsService()


async def get_current_user() -> User:
    """Get current authenticated user"""
    # This would be implemented with proper JWT validation
    pass


@router.get("/", response_model=List[Instrument])
async def get_all_instruments():
    """Get all available instruments"""
    try:
        instruments = await instruments_service.get_all_instruments()
        return instruments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{instrument_type}", response_model=Instrument)
async def get_instrument_by_type(instrument_type: InstrumentType):
    """Get instrument by type"""
    try:
        instrument = await instruments_service.get_instrument_by_type(instrument_type)
        if not instrument:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instrument not found"
            )
        return instrument
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/select", response_model=InstrumentSelection)
async def select_instrument(
    instrument_type: InstrumentType,
    current_user: User = Depends(get_current_user)
):
    """Select instrument for user"""
    try:
        selection = await instruments_service.select_instrument(
            current_user.id, instrument_type
        )
        return selection
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{instrument_type}/faq", response_model=InstrumentFAQ)
async def get_faq_by_instrument(instrument_type: InstrumentType):
    """Get FAQ for specific instrument"""
    try:
        faq = await instruments_service.get_faq_by_instrument(instrument_type)
        return faq
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/faq/search", response_model=List[Dict[str, Any]])
async def search_faq(
    query: str = Query(..., description="Search query"),
    instrument_type: Optional[InstrumentType] = Query(None, description="Filter by instrument type")
):
    """Search FAQ items by query"""
    try:
        results = await instruments_service.search_faq(query, instrument_type)
        return [item.dict() for item in results]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
