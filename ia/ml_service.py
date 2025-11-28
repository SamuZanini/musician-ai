"""
Serviço de Machine Learning para detecção de áudio musical
Implementação simples usando FastAPI e processamento de áudio
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import numpy as np
import io
import soundfile as sf
import logging
from audio_processor import AudioProcessor

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Musician AI - ML Service",
    description="Serviço de Machine Learning para detecção de áudio musical",
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

# Modelos Pydantic para validação
class TuningRequest(BaseModel):
    """Modelo para requisição de afinação"""
    frequency: Optional[float] = None
    tolerance_cents: float = 50

class TuningResponse(BaseModel):
    """Modelo para resposta de afinação"""
    note: str
    frequency: float
    is_in_tune: bool
    cents_diff: float
    tuning_direction: str
    confidence: float
    target_frequency: Optional[float] = None
    harmonics_detected: Optional[list] = None

class DetectionRequest(BaseModel):
    """Modelo para requisição de detecção"""
    audio_data: Optional[list] = None
    sample_rate: int = 44100

class DetectionResponse(BaseModel):
    """Modelo para resposta de detecção"""
    pitch: Optional[float]
    note: str
    confidence: float
    is_detected: bool
    cents_diff: Optional[float] = None
    target_frequency: Optional[float] = None
    harmonics: Optional[list] = None

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Musician AI - ML Service",
        "version": "1.0.0",
        "endpoints": {
            "tune": "/tune",
            "detect": "/detect",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde do serviço"""
    return {"status": "healthy", "service": "ml-service"}

@app.post("/tune", response_model=TuningResponse)
async def tune_audio(request: TuningRequest):
    """
    Endpoint para afinação de áudio
    Simula detecção de pitch e retorna feedback de afinação
    """
    try:
        if request.frequency is None:
            raise HTTPException(status_code=400, detail="Frequência não fornecida")
        
        # Obtém feedback de afinação
        feedback = audio_processor.get_tuning_feedback(request.frequency)
        
        # Adiciona frequência alvo se disponível
        note, _ = audio_processor.frequency_to_note(request.frequency)
        target_freq = audio_processor.note_frequencies.get(note)
        
        return TuningResponse(
            **feedback,
            target_frequency=target_freq,
            harmonics_detected=None
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /tune: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/detect", response_model=DetectionResponse)
async def detect_audio(request: DetectionRequest):
    """
    Endpoint para detecção de áudio em tempo real
    Processa dados de áudio e retorna pitch detectado
    """
    try:
        if request.audio_data is None:
            raise HTTPException(status_code=400, detail="Dados de áudio não fornecidos")
        
        # Converte lista para numpy array
        audio_array = np.array(request.audio_data, dtype=np.float32)
        
        # Detecta pitch
        pitch, confidence = audio_processor.detect_pitch(audio_array)
        
        if pitch is not None:
            note, cents_diff = audio_processor.frequency_to_note(pitch)
            is_detected = confidence > 0.3  # Threshold de confiança
        else:
            note = "Silêncio"
            cents_diff = 0.0
            is_detected = False
        
        return DetectionResponse(
            pitch=pitch,
            note=note,
            confidence=confidence,
            is_detected=is_detected,
            cents_diff=round(cents_diff, 1) if pitch is not None else None,
            target_frequency=None,
            harmonics=None
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /detect: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/detect-file")
async def detect_audio_file(file: UploadFile = File(...)):
    """
    Endpoint para detecção de áudio via upload de arquivo
    """
    try:
        # Verifica se é arquivo de áudio
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser de áudio")
        
        # Lê o arquivo
        audio_data = await file.read()
        
        # Carrega áudio usando soundfile
        audio_array, sample_rate = sf.read(io.BytesIO(audio_data))
        
        # Converte para mono se estéreo
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)
        
        # Detecta pitch
        pitch, confidence = audio_processor.detect_pitch(audio_array)
        
        if pitch is not None:
            note, cents_diff = audio_processor.frequency_to_note(pitch)
            is_tuned = audio_processor.is_in_tune(pitch)
        else:
            note = "Silêncio"
            cents_diff = 0
            is_tuned = False
        
        return {
            "pitch": pitch,
            "note": note,
            "confidence": confidence,
            "cents_diff": cents_diff,
            "is_tuned": is_tuned,
            "sample_rate": sample_rate
        }
        
    except Exception as e:
        logger.error(f"Erro no endpoint /detect-file: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/notes")
async def get_notes():
    """Retorna lista de notas musicais e suas frequências"""
    return {
        "notes": audio_processor.note_frequencies,
        "total_notes": len(audio_processor.note_frequencies)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
