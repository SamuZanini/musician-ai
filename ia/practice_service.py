"""
Serviço de Prática Musical
Endpoint especializado para validação de notas durante prática
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import numpy as np
import re
from audio_processor import AudioProcessor

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Musician AI - Practice Service",
    description="Serviço especializado para prática musical",
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
class PracticeCheckRequest(BaseModel):
    """Modelo para requisição de validação de prática"""
    frequency: float
    target_note: str
    tolerance_cents: float = 50
    instrument: Optional[str] = None

class PracticeCheckResponse(BaseModel):
    """Modelo para resposta de validação de prática"""
    detected_note: str
    target_note: str
    frequency: float
    target_frequency: float
    is_correct: bool
    confidence: float
    cents_diff: float
    accuracy_score: float  # 0-100
    feedback_message: str
    tuning_direction: str
    harmonics_detected: Optional[List[float]] = None

class PracticeSessionRequest(BaseModel):
    """Modelo para requisição de sessão de prática"""
    audio_data: List[float]
    target_note: str
    sample_rate: int = 44100
    tolerance_cents: float = 50
    instrument: Optional[str] = None

class PracticeSessionResponse(BaseModel):
    """Modelo para resposta de sessão de prática"""
    detected_note: str
    target_note: str
    pitch: Optional[float]
    target_frequency: float
    is_correct: bool
    confidence: float
    cents_diff: float
    accuracy_score: float
    feedback_message: str
    tuning_direction: str
    is_detected: bool
    harmonics_detected: Optional[List[float]] = None

def detect_harmonics(audio_data: np.ndarray, fundamental_freq: float, sample_rate: int) -> List[float]:
    """
    Detecta harmônicos presentes no áudio
    
    Args:
        audio_data: Dados de áudio
        fundamental_freq: Frequência fundamental detectada
        sample_rate: Taxa de amostragem
        
    Returns:
        Lista de frequências de harmônicos detectados
    """
    try:
        import librosa
        
        # Calcula espectro de frequência
        fft = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
        magnitude = np.abs(fft)
        
        # Procura por harmônicos (múltiplos da fundamental)
        harmonics = []
        for i in range(2, 6):  # 2º ao 5º harmônico
            harmonic_freq = fundamental_freq * i
            if harmonic_freq < sample_rate / 2:
                # Encontra bin mais próximo
                idx = np.argmin(np.abs(freqs - harmonic_freq))
                if idx < len(magnitude) and magnitude[idx] > np.max(magnitude) * 0.1:
                    harmonics.append(float(harmonic_freq))
        
        return harmonics
    except Exception as e:
        logger.warning(f"Erro ao detectar harmônicos: {e}")
        return []

def calculate_accuracy_score(cents_diff: float, confidence: float, tolerance_cents: float) -> float:
    """
    Calcula score de precisão (0-100)
    
    Args:
        cents_diff: Diferença em cents
        confidence: Confiança da detecção
        tolerance_cents: Tolerância em cents
        
    Returns:
        Score de precisão de 0 a 100
    """
    # Score baseado na diferença em cents
    if abs(cents_diff) <= tolerance_cents:
        cents_score = 100 - (abs(cents_diff) / tolerance_cents * 20)  # Penaliza até 20 pontos
    else:
        cents_score = max(0, 80 - (abs(cents_diff) - tolerance_cents) * 2)
    
    # Combina com confiança
    final_score = (cents_score * 0.7) + (confidence * 100 * 0.3)
    
    return min(100, max(0, final_score))

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Musician AI - Practice Service",
        "version": "1.0.0",
        "endpoints": {
            "check": "/practice/check",
            "session": "/practice/session",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde do serviço"""
    return {"status": "healthy", "service": "practice-service"}

@app.post("/practice/check", response_model=PracticeCheckResponse)
async def check_practice_note(request: PracticeCheckRequest):
    """
    Valida se a nota tocada corresponde à nota alvo
    
    Args:
        request: Dados da requisição
        
    Returns:
        Resposta com validação completa
    """
    try:
        # Obtém frequência alvo da nota
        target_frequency = audio_processor.note_frequencies.get(request.target_note)
        if not target_frequency:
            raise HTTPException(
                status_code=400,
                detail=f"Nota alvo '{request.target_note}' não reconhecida"
            )
        
        # Detecta nota atual a partir da frequência
        detected_note, cents_diff = audio_processor.frequency_to_note(request.frequency)
        
        # Normaliza notas para comparação (remove oitava)
        def normalize_note(note: str) -> str:
            if not note:
                return ""
            return re.sub(r'\d+$', '', note)
        
        detected_base = normalize_note(detected_note)
        target_base = normalize_note(request.target_note)
        
        # Verifica se acertou
        is_correct = detected_base == target_base and abs(cents_diff) <= request.tolerance_cents
        
        # Calcula score de precisão
        confidence = 0.8  # Confiança baseada na detecção
        accuracy_score = calculate_accuracy_score(cents_diff, confidence, request.tolerance_cents)
        
        # Determina direção de afinação
        if abs(cents_diff) <= request.tolerance_cents:
            tuning_direction = "Afinado"
        elif cents_diff > 0:
            tuning_direction = "Muito alto"
        else:
            tuning_direction = "Muito baixo"
        
        # Gera mensagem de feedback
        if is_correct:
            if abs(cents_diff) < 5:
                feedback_message = "Perfeito! Nota correta e bem afinada."
            else:
                feedback_message = f"Nota correta! {abs(cents_diff):.1f} cents de diferença."
        else:
            if detected_base == target_base:
                feedback_message = f"Nota correta, mas precisa afinar. {abs(cents_diff):.1f} cents de diferença."
            else:
                feedback_message = f"Nota incorreta. Você tocou {detected_note}, mas deveria ser {request.target_note}."
        
        return PracticeCheckResponse(
            detected_note=detected_note,
            target_note=request.target_note,
            frequency=request.frequency,
            target_frequency=target_frequency,
            is_correct=is_correct,
            confidence=confidence,
            cents_diff=round(cents_diff, 1),
            accuracy_score=round(accuracy_score, 1),
            feedback_message=feedback_message,
            tuning_direction=tuning_direction,
            harmonics_detected=None  # Será preenchido quando houver dados de áudio
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /practice/check: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/practice/session", response_model=PracticeSessionResponse)
async def practice_session(request: PracticeSessionRequest):
    """
    Processa áudio de uma sessão de prática e valida contra nota alvo
    
    Args:
        request: Dados da requisição com áudio
        
    Returns:
        Resposta com análise completa
    """
    try:
        # Converte dados de áudio para numpy array
        audio_array = np.array(request.audio_data, dtype=np.float32)
        
        # Detecta pitch
        pitch, confidence = audio_processor.detect_pitch(audio_array)
        
        if pitch is None or confidence < 0.3:
            return PracticeSessionResponse(
                detected_note="Silêncio",
                target_note=request.target_note,
                pitch=None,
                target_frequency=audio_processor.note_frequencies.get(request.target_note, 0),
                is_correct=False,
                confidence=0.0,
                cents_diff=0.0,
                accuracy_score=0.0,
                feedback_message="Nenhum som detectado. Toque uma nota no seu instrumento.",
                tuning_direction="Nenhum",
                is_detected=False,
                harmonics_detected=None
            )
        
        # Obtém frequência alvo
        target_frequency = audio_processor.note_frequencies.get(request.target_note)
        if not target_frequency:
            raise HTTPException(
                status_code=400,
                detail=f"Nota alvo '{request.target_note}' não reconhecida"
            )
        
        # Detecta nota atual
        detected_note, cents_diff = audio_processor.frequency_to_note(pitch)
        
        # Normaliza notas para comparação
        def normalize_note(note: str) -> str:
            if not note:
                return ""
            return re.sub(r'\d+$', '', note)
        
        detected_base = normalize_note(detected_note)
        target_base = normalize_note(request.target_note)
        
        # Verifica se acertou
        is_correct = detected_base == target_base and abs(cents_diff) <= request.tolerance_cents
        
        # Detecta harmônicos
        harmonics = detect_harmonics(audio_array, pitch, request.sample_rate)
        
        # Calcula score de precisão
        accuracy_score = calculate_accuracy_score(cents_diff, confidence, request.tolerance_cents)
        
        # Determina direção de afinação
        if abs(cents_diff) <= request.tolerance_cents:
            tuning_direction = "Afinado"
        elif cents_diff > 0:
            tuning_direction = "Muito alto"
        else:
            tuning_direction = "Muito baixo"
        
        # Gera mensagem de feedback
        if is_correct:
            if abs(cents_diff) < 5:
                feedback_message = "Perfeito! Nota correta e bem afinada."
            else:
                feedback_message = f"Nota correta! {abs(cents_diff):.1f} cents de diferença."
        else:
            if detected_base == target_base:
                feedback_message = f"Nota correta, mas precisa afinar. {abs(cents_diff):.1f} cents de diferença."
            else:
                feedback_message = f"Nota incorreta. Você tocou {detected_note}, mas deveria ser {request.target_note}."
        
        return PracticeSessionResponse(
            detected_note=detected_note,
            target_note=request.target_note,
            pitch=float(pitch),
            target_frequency=target_frequency,
            is_correct=is_correct,
            confidence=float(confidence),
            cents_diff=round(cents_diff, 1),
            accuracy_score=round(accuracy_score, 1),
            feedback_message=feedback_message,
            tuning_direction=tuning_direction,
            is_detected=True,
            harmonics_detected=harmonics if harmonics else None
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /practice/session: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

