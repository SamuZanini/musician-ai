"""
Serviço de Detecção de Áudio em Tempo Real
Implementação simples para detecção contínua de pitch e notas
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import asyncio
import logging
from audio_processor import AudioProcessor
import numpy as np

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Musician AI - Detection Service",
    description="Serviço de Detecção de Áudio em Tempo Real",
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
class DetectionRequest(BaseModel):
    """Modelo para requisição de detecção"""
    audio_data: List[float]
    sample_rate: int = 44100
    instrument: Optional[str] = None

class DetectionResponse(BaseModel):
    """Modelo para resposta de detecção"""
    pitch: Optional[float]
    note: str
    confidence: float
    is_detected: bool
    timestamp: float
    instrument: Optional[str] = None

class StreamConfig(BaseModel):
    """Modelo para configuração de stream"""
    sample_rate: int = 44100
    buffer_size: int = 1024
    detection_threshold: float = 0.3
    instrument: Optional[str] = None

# Gerenciador de conexões WebSocket
class ConnectionManager:
    """Gerencia conexões WebSocket"""
    
    def __init__(self):
        """Inicializa o gerenciador"""
        self.active_connections: List[WebSocket] = []
        self.detection_configs: Dict[WebSocket, StreamConfig] = {}
    
    async def connect(self, websocket: WebSocket, config: StreamConfig):
        """
        Conecta um cliente WebSocket
        
        Args:
            websocket: Conexão WebSocket
            config: Configuração do stream
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.detection_configs[websocket] = config
        logger.info(f"Cliente conectado. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Desconecta um cliente WebSocket
        
        Args:
            websocket: Conexão WebSocket
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.detection_configs:
            del self.detection_configs[websocket]
        logger.info(f"Cliente desconectado. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Envia mensagem para um cliente específico
        
        Args:
            message: Mensagem a ser enviada
            websocket: Conexão WebSocket de destino
        """
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
    
    async def broadcast(self, message: str):
        """
        Envia mensagem para todos os clientes conectados
        
        Args:
            message: Mensagem a ser enviada
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Erro ao enviar broadcast: {e}")

# Inicializa o gerenciador de conexões
manager = ConnectionManager()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Musician AI - Detection Service",
        "version": "1.0.0",
        "endpoints": {
            "detect": "/detect",
            "websocket": "/ws",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde do serviço"""
    return {
        "status": "healthy", 
        "service": "detection-service",
        "active_connections": len(manager.active_connections)
    }

@app.post("/detect", response_model=DetectionResponse)
async def detect_audio(request: DetectionRequest):
    """
    Endpoint para detecção de áudio
    
    Args:
        request: Dados da requisição
        
    Returns:
        Resultado da detecção
    """
    try:
        # Converte dados de áudio para numpy array
        audio_array = np.array(request.audio_data, dtype=np.float32)
        
        # Detecta pitch
        pitch, confidence = audio_processor.detect_pitch(audio_array)
        
        if pitch is not None and confidence > 0.3:
            note, _ = audio_processor.frequency_to_note(pitch)
            is_detected = True
        else:
            note = "Silêncio"
            is_detected = False
        
        return DetectionResponse(
            pitch=float(pitch) if pitch is not None else None,
            note=note,
            confidence=float(confidence),
            is_detected=is_detected,
            timestamp=asyncio.get_event_loop().time(),
            instrument=request.instrument
        )
        
    except Exception as e:
        logger.error(f"Erro no endpoint /detect: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket para detecção em tempo real
    
    Args:
        websocket: Conexão WebSocket
    """
    # Configuração padrão
    config = StreamConfig()
    
    try:
        # Conecta cliente
        await manager.connect(websocket, config)
        
        while True:
            # Recebe dados do cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "config":
                # Atualiza configuração
                config_data = message.get("config", {})
                config = StreamConfig(**config_data)
                manager.detection_configs[websocket] = config
                
                await manager.send_personal_message(
                    json.dumps({
                        "type": "config_updated",
                        "message": "Configuração atualizada"
                    }),
                    websocket
                )
                
            elif message.get("type") == "audio_data":
                # Processa dados de áudio
                audio_data = message.get("audio_data", [])
                
                if len(audio_data) > 0:
                    # Converte para numpy array
                    audio_array = np.array(audio_data, dtype=np.float32)
                    
                    # Detecta pitch
                    pitch, confidence = audio_processor.detect_pitch(audio_array)
                    
                    # Prepara resposta
                    if pitch is not None and confidence > config.detection_threshold:
                        note, cents_diff = audio_processor.frequency_to_note(pitch)
                        is_detected = True
                    else:
                        note = "Silêncio"
                        cents_diff = 0
                        is_detected = False
                    
                    response = {
                        "type": "detection_result",
                        "pitch": float(pitch) if pitch is not None else None,
                        "note": note,
                        "confidence": float(confidence),
                        "is_detected": is_detected,
                        "cents_diff": float(cents_diff),
                        "timestamp": message.get("timestamp", 0),
                        "instrument": config.instrument
                    }
                    
                    # Envia resultado
                    await manager.send_personal_message(
                        json.dumps(response),
                        websocket
                    )
                    
            elif message.get("type") == "ping":
                # Responde ping
                await manager.send_personal_message(
                    json.dumps({"type": "pong"}),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
        manager.disconnect(websocket)

@app.get("/stats")
async def get_stats():
    """Retorna estatísticas do serviço"""
    return {
        "active_connections": len(manager.active_connections),
        "service_status": "running",
        "supported_instruments": ["guitar", "violin", "piano", "bass", "ukulele"]
    }

@app.post("/detect/batch")
async def detect_batch(request: List[DetectionRequest]):
    """
    Endpoint para detecção em lote
    
    Args:
        request: Lista de requisições de detecção
        
    Returns:
        Lista de resultados
    """
    try:
        results = []
        
        for req in request:
            # Converte dados de áudio
            audio_array = np.array(req.audio_data, dtype=np.float32)
            
            # Detecta pitch
            pitch, confidence = audio_processor.detect_pitch(audio_array)
            
            if pitch is not None and confidence > 0.3:
                note, _ = audio_processor.frequency_to_note(pitch)
                is_detected = True
            else:
                note = "Silêncio"
                is_detected = False
            
            results.append({
                "pitch": float(pitch) if pitch is not None else None,
                "note": note,
                "confidence": float(confidence),
                "is_detected": is_detected,
                "instrument": req.instrument
            })
        
        return {"results": results, "total": len(results)}
        
    except Exception as e:
        logger.error(f"Erro no endpoint /detect/batch: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
