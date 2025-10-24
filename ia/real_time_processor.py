"""
Processador de áudio em tempo real para detecção de pitch
Implementação simples para streaming de áudio via WebSocket
"""

import asyncio
import websockets
import json
import numpy as np
import logging
from typing import Dict, Any, Optional
from audio_processor import AudioProcessor
import base64

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeProcessor:
    """Classe para processamento de áudio em tempo real"""
    
    def __init__(self):
        """Inicializa o processador em tempo real"""
        self.audio_processor = AudioProcessor()
        self.connected_clients = set()
        self.is_processing = False
        
    async def handle_audio_stream(self, websocket, path):
        """
        Manipula stream de áudio via WebSocket
        
        Args:
            websocket: Conexão WebSocket
            path: Caminho da conexão
        """
        client_id = f"client_{len(self.connected_clients)}"
        self.connected_clients.add(websocket)
        
        logger.info(f"Cliente conectado: {client_id}")
        
        try:
            async for message in websocket:
                await self._process_audio_message(websocket, message, client_id)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Cliente desconectado: {client_id}")
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
        finally:
            self.connected_clients.discard(websocket)
    
    async def _process_audio_message(self, websocket, message: str, client_id: str):
        """
        Processa mensagem de áudio recebida
        
        Args:
            websocket: Conexão WebSocket
            message: Mensagem recebida
            client_id: ID do cliente
        """
        try:
            # Decodifica mensagem JSON
            data = json.loads(message)
            
            if data.get("type") == "audio_data":
                # Processa dados de áudio
                audio_data = data.get("audio_data", [])
                sample_rate = data.get("sample_rate", 44100)
                
                # Converte para numpy array
                audio_array = np.array(audio_data, dtype=np.float32)
                
                # Detecta pitch
                pitch, confidence = self.audio_processor.detect_pitch(audio_array)
                
                # Prepara resposta
                response = {
                    "type": "detection_result",
                    "pitch": float(pitch) if pitch is not None else None,
                    "confidence": float(confidence),
                    "timestamp": data.get("timestamp", 0)
                }
                
                if pitch is not None:
                    note, cents_diff = self.audio_processor.frequency_to_note(pitch)
                    is_tuned = self.audio_processor.is_in_tune(pitch)
                    
                    response.update({
                        "note": note,
                        "cents_diff": float(cents_diff),
                        "is_tuned": is_tuned,
                        "is_detected": confidence > 0.3
                    })
                else:
                    response.update({
                        "note": "Silêncio",
                        "cents_diff": 0.0,
                        "is_tuned": False,
                        "is_detected": False
                    })
                
                # Envia resultado
                await websocket.send(json.dumps(response))
                
            elif data.get("type") == "start_stream":
                # Inicia processamento em tempo real
                self.is_processing = True
                await websocket.send(json.dumps({
                    "type": "stream_started",
                    "message": "Processamento iniciado"
                }))
                
            elif data.get("type") == "stop_stream":
                # Para processamento
                self.is_processing = False
                await websocket.send(json.dumps({
                    "type": "stream_stopped",
                    "message": "Processamento parado"
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Formato JSON inválido"
            }))
        except Exception as e:
            logger.error(f"Erro no processamento da mensagem: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Erro interno: {str(e)}"
            }))
    
    async def start_server(self, host: str = "localhost", port: int = 8765):
        """
        Inicia servidor WebSocket
        
        Args:
            host: Host do servidor
            port: Porta do servidor
        """
        logger.info(f"Iniciando servidor WebSocket em {host}:{port}")
        
        async with websockets.serve(
            self.handle_audio_stream, 
            host, 
            port,
            ping_interval=20,
            ping_timeout=10
        ):
            logger.info("Servidor WebSocket iniciado")
            await asyncio.Future()  # Mantém servidor rodando

# Cliente de exemplo para testar o processamento em tempo real
class AudioStreamClient:
    """Cliente para testar o processamento em tempo real"""
    
    def __init__(self, uri: str = "ws://localhost:8765"):
        """
        Inicializa cliente WebSocket
        
        Args:
            uri: URI do servidor WebSocket
        """
        self.uri = uri
        self.websocket = None
    
    async def connect(self):
        """Conecta ao servidor WebSocket"""
        try:
            self.websocket = await websockets.connect(self.uri)
            logger.info("Conectado ao servidor WebSocket")
            return True
        except Exception as e:
            logger.error(f"Erro na conexão: {e}")
            return False
    
    async def send_audio_data(self, audio_data: list, sample_rate: int = 44100):
        """
        Envia dados de áudio para processamento
        
        Args:
            audio_data: Dados de áudio
            sample_rate: Taxa de amostragem
        """
        if not self.websocket:
            logger.error("WebSocket não conectado")
            return
        
        message = {
            "type": "audio_data",
            "audio_data": audio_data,
            "sample_rate": sample_rate,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            response = await self.websocket.recv()
            result = json.loads(response)
            
            if result.get("type") == "detection_result":
                logger.info(f"Pitch detectado: {result.get('pitch')} Hz")
                logger.info(f"Nota: {result.get('note')}")
                logger.info(f"Confiança: {result.get('confidence')}")
            
        except Exception as e:
            logger.error(f"Erro no envio de dados: {e}")
    
    async def start_stream(self):
        """Inicia stream de áudio"""
        if not self.websocket:
            return
        
        message = {"type": "start_stream"}
        await self.websocket.send(json.dumps(message))
    
    async def stop_stream(self):
        """Para stream de áudio"""
        if not self.websocket:
            return
        
        message = {"type": "stop_stream"}
        await self.websocket.send(json.dumps(message))
    
    async def disconnect(self):
        """Desconecta do servidor"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

# Função para iniciar o servidor
async def start_real_time_server():
    """Inicia o servidor de processamento em tempo real"""
    processor = RealTimeProcessor()
    await processor.start_server()

if __name__ == "__main__":
    # Inicia servidor WebSocket
    asyncio.run(start_real_time_server())
