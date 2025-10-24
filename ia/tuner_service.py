"""
Serviço de Afinador Musical
Implementação simples para afinação de instrumentos
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import numpy as np
from audio_processor import AudioProcessor

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Musician AI - Tuner Service",
    description="Serviço de Afinador Musical",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o processador de áudio
audio_processor = AudioProcessor()

# Modelos Pydantic
class TunerRequest(BaseModel):
    """Modelo para requisição de afinação"""
    frequency: float
    target_note: Optional[str] = None
    tolerance_cents: float = 50

class TunerResponse(BaseModel):
    """Modelo para resposta de afinação"""
    current_note: str
    target_note: str
    frequency: float
    target_frequency: float
    cents_diff: float
    is_in_tune: bool
    tuning_direction: str
    confidence: float

class InstrumentTuning:
    """Classe para afinação específica de instrumentos"""
    
    def __init__(self):
        """Inicializa configurações de afinação por instrumento"""
        self.instrument_tunings = {
            "guitar": {
                "E4": 329.63,  # Mi
                "B3": 246.94,  # Si
                "G3": 196.00,  # Sol
                "D3": 146.83,  # Ré
                "A2": 110.00,  # Lá
                "E2": 82.41    # Mi grave
            },
            "violin": {
                "E5": 659.25,  # Mi
                "A4": 440.00,  # Lá
                "D4": 293.66,  # Ré
                "G3": 196.00   # Sol
            },
            "piano": {
                "A4": 440.00   # Lá central
            }
        }
    
    def get_instrument_notes(self, instrument: str) -> Dict[str, float]:
        """
        Retorna notas de afinação para um instrumento
        
        Args:
            instrument: Nome do instrumento
            
        Returns:
            Dicionário com notas e frequências
        """
        return self.instrument_tunings.get(instrument, {})
    
    def get_closest_target(self, frequency: float, instrument: str) -> tuple:
        """
        Encontra a nota mais próxima para afinação
        
        Args:
            frequency: Frequência detectada
            instrument: Nome do instrumento
            
        Returns:
            Tuple com (nota_alvo, frequência_alvo)
        """
        instrument_notes = self.get_instrument_notes(instrument)
        
        if not instrument_notes:
            return None, None
        
        closest_note = None
        min_diff = float('inf')
        
        for note, note_freq in instrument_notes.items():
            diff = abs(frequency - note_freq)
            if diff < min_diff:
                min_diff = diff
                closest_note = note
        
        return closest_note, instrument_notes.get(closest_note)

# Inicializa o afinador de instrumentos
instrument_tuner = InstrumentTuning()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Musician AI - Tuner Service",
        "version": "1.0.0",
        "endpoints": {
            "tune": "/tune",
            "instruments": "/instruments",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde do serviço"""
    return {"status": "healthy", "service": "tuner-service"}

@app.get("/instruments")
async def get_instruments():
    """Retorna lista de instrumentos suportados"""
    return {
        "instruments": list(instrument_tuner.instrument_tunings.keys()),
        "total": len(instrument_tuner.instrument_tunings)
    }

@app.get("/instruments/{instrument}/notes")
async def get_instrument_notes(instrument: str):
    """
    Retorna notas de afinação para um instrumento específico
    
    Args:
        instrument: Nome do instrumento
    """
    notes = instrument_tuner.get_instrument_notes(instrument)
    
    if not notes:
        raise HTTPException(
            status_code=404, 
            detail=f"Instrumento '{instrument}' não suportado"
        )
    
    return {
        "instrument": instrument,
        "notes": notes,
        "total_notes": len(notes)
    }

@app.post("/tune", response_model=TunerResponse)
async def tune_audio(request: TunerRequest):
    """
    Endpoint principal para afinação
    
    Args:
        request: Dados da requisição de afinação
        
    Returns:
        Resposta com informações de afinação
    """
    try:
        # Detecta nota atual
        current_note, cents_diff = audio_processor.frequency_to_note(request.frequency)
        
        # Determina nota alvo
        if request.target_note:
            target_note = request.target_note
            target_frequency = audio_processor.note_frequencies.get(target_note)
            if not target_frequency:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Nota '{target_note}' não reconhecida"
                )
        else:
            # Usa a nota mais próxima como alvo
            target_note = current_note
            target_frequency = request.frequency
        
        # Calcula diferença em cents
        if target_frequency and target_frequency > 0:
            cents_diff = 1200 * np.log2(request.frequency / target_frequency)
        else:
            cents_diff = 0
        
        # Verifica se está afinado
        is_in_tune = abs(cents_diff) <= request.tolerance_cents
        
        # Determina direção de afinação
        if is_in_tune:
            tuning_direction = "Afinado"
        elif cents_diff > 0:
            tuning_direction = "Muito alto"
        else:
            tuning_direction = "Muito baixo"
        
        return TunerResponse(
            current_note=current_note,
            target_note=target_note,
            frequency=request.frequency,
            target_frequency=target_frequency or 0,
            cents_diff=round(cents_diff, 1),
            is_in_tune=is_in_tune,
            tuning_direction=tuning_direction,
            confidence=0.8  # Confiança simulada
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /tune: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/tune/{instrument}")
async def tune_instrument(instrument: str, request: TunerRequest):
    """
    Afina para um instrumento específico
    
    Args:
        instrument: Nome do instrumento
        request: Dados da requisição
        
    Returns:
        Resposta de afinação específica do instrumento
    """
    try:
        # Verifica se instrumento é suportado
        instrument_notes = instrument_tuner.get_instrument_notes(instrument)
        if not instrument_notes:
            raise HTTPException(
                status_code=404,
                detail=f"Instrumento '{instrument}' não suportado"
            )
        
        # Encontra nota mais próxima do instrumento
        target_note, target_frequency = instrument_tuner.get_closest_target(
            request.frequency, instrument
        )
        
        if not target_note:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível determinar nota alvo"
            )
        
        # Detecta nota atual
        current_note, _ = audio_processor.frequency_to_note(request.frequency)
        
        # Calcula diferença em cents
        if target_frequency and target_frequency > 0:
            cents_diff = 1200 * np.log2(request.frequency / target_frequency)
        else:
            cents_diff = 0
        
        # Verifica se está afinado
        is_in_tune = abs(cents_diff) <= request.tolerance_cents
        
        # Determina direção de afinação
        if is_in_tune:
            tuning_direction = "Afinado"
        elif cents_diff > 0:
            tuning_direction = "Muito alto"
        else:
            tuning_direction = "Muito baixo"
        
        return {
            "instrument": instrument,
            "current_note": current_note,
            "target_note": target_note,
            "frequency": request.frequency,
            "target_frequency": target_frequency,
            "cents_diff": round(cents_diff, 1),
            "is_in_tune": is_in_tune,
            "tuning_direction": tuning_direction,
            "confidence": 0.8
        }
        
    except Exception as e:
        logger.error(f"Erro no endpoint /tune/{instrument}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/tune/{instrument}/guide")
async def get_tuning_guide(instrument: str):
    """
    Retorna guia de afinação para um instrumento
    
    Args:
        instrument: Nome do instrumento
        
    Returns:
        Guia de afinação
    """
    try:
        instrument_notes = instrument_tuner.get_instrument_notes(instrument)
        
        if not instrument_notes:
            raise HTTPException(
                status_code=404,
                detail=f"Instrumento '{instrument}' não suportado"
            )
        
        # Ordena notas por frequência
        sorted_notes = sorted(instrument_notes.items(), key=lambda x: x[1])
        
        return {
            "instrument": instrument,
            "tuning_guide": [
                {
                    "note": note,
                    "frequency": freq,
                    "order": i + 1
                }
                for i, (note, freq) in enumerate(sorted_notes)
            ],
            "total_strings": len(sorted_notes)
        }
        
    except Exception as e:
        logger.error(f"Erro no endpoint /tune/{instrument}/guide: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
