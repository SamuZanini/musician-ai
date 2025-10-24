"""
Configurações para os serviços de IA
Implementação simples para gerenciamento de configurações
"""

import os
from typing import Dict, Any, Optional

class Config:
    """Classe de configuração para os serviços de IA"""
    
    # Configurações de áudio
    DEFAULT_SAMPLE_RATE = 44100
    DEFAULT_HOP_SIZE = 512
    DEFAULT_BUFFER_SIZE = 1024
    
    # Configurações de detecção
    DEFAULT_CONFIDENCE_THRESHOLD = 0.3
    DEFAULT_TUNING_TOLERANCE = 50  # cents
    
    # Configurações de serviços
    ML_SERVICE_PORT = 8001
    TUNER_SERVICE_PORT = 8002
    DETECTION_SERVICE_PORT = 8003
    WEBSOCKET_PORT = 8765
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configurações de performance
    MAX_CONNECTIONS = 100
    REQUEST_TIMEOUT = 30
    WEBSOCKET_PING_INTERVAL = 20
    WEBSOCKET_PING_TIMEOUT = 10
    
    # Configurações de instrumentos
    SUPPORTED_INSTRUMENTS = {
        "guitar": {
            "name": "Guitarra",
            "strings": ["E2", "A2", "D3", "G3", "B3", "E4"],
            "frequencies": [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]
        },
        "violin": {
            "name": "Violino", 
            "strings": ["G3", "D4", "A4", "E5"],
            "frequencies": [196.00, 293.66, 440.00, 659.25]
        },
        "piano": {
            "name": "Piano",
            "strings": ["A4"],
            "frequencies": [440.00]
        },
        "bass": {
            "name": "Baixo",
            "strings": ["E1", "A1", "D2", "G2"],
            "frequencies": [41.20, 55.00, 73.42, 98.00]
        },
        "ukulele": {
            "name": "Ukulele",
            "strings": ["G4", "C4", "E4", "A4"],
            "frequencies": [392.00, 261.63, 329.63, 440.00]
        }
    }
    
    # Configurações de notas musicais
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVES = list(range(0, 8))
    A4_FREQUENCY = 440.0  # Frequência de referência
    
    @classmethod
    def get_instrument_config(cls, instrument: str) -> Optional[Dict[str, Any]]:
        """
        Retorna configuração de um instrumento
        
        Args:
            instrument: Nome do instrumento
            
        Returns:
            Configuração do instrumento ou None
        """
        return cls.SUPPORTED_INSTRUMENTS.get(instrument.lower())
    
    @classmethod
    def get_all_instruments(cls) -> Dict[str, Dict[str, Any]]:
        """
        Retorna todos os instrumentos suportados
        
        Returns:
            Dicionário com todos os instrumentos
        """
        return cls.SUPPORTED_INSTRUMENTS
    
    @classmethod
    def get_service_port(cls, service: str) -> int:
        """
        Retorna porta de um serviço
        
        Args:
            service: Nome do serviço
            
        Returns:
            Porta do serviço
        """
        ports = {
            "ml_service": cls.ML_SERVICE_PORT,
            "tuner_service": cls.TUNER_SERVICE_PORT,
            "detection_service": cls.DETECTION_SERVICE_PORT,
            "websocket": cls.WEBSOCKET_PORT
        }
        return ports.get(service, 8000)
    
    @classmethod
    def get_service_url(cls, service: str, host: str = "localhost") -> str:
        """
        Retorna URL de um serviço
        
        Args:
            service: Nome do serviço
            host: Host do serviço
            
        Returns:
            URL do serviço
        """
        port = cls.get_service_port(service)
        protocol = "ws" if service == "websocket" else "http"
        return f"{protocol}://{host}:{port}"
    
    @classmethod
    def load_from_env(cls):
        """
        Carrega configurações de variáveis de ambiente
        
        Returns:
            Configurações carregadas
        """
        config = {}
        
        # Configurações de áudio
        config["sample_rate"] = int(os.getenv("SAMPLE_RATE", cls.DEFAULT_SAMPLE_RATE))
        config["hop_size"] = int(os.getenv("HOP_SIZE", cls.DEFAULT_HOP_SIZE))
        config["buffer_size"] = int(os.getenv("BUFFER_SIZE", cls.DEFAULT_BUFFER_SIZE))
        
        # Configurações de detecção
        config["confidence_threshold"] = float(os.getenv("CONFIDENCE_THRESHOLD", cls.DEFAULT_CONFIDENCE_THRESHOLD))
        config["tuning_tolerance"] = int(os.getenv("TUNING_TOLERANCE", cls.DEFAULT_TUNING_TOLERANCE))
        
        # Configurações de serviços
        config["ml_service_port"] = int(os.getenv("ML_SERVICE_PORT", cls.ML_SERVICE_PORT))
        config["tuner_service_port"] = int(os.getenv("TUNER_SERVICE_PORT", cls.TUNER_SERVICE_PORT))
        config["detection_service_port"] = int(os.getenv("DETECTION_SERVICE_PORT", cls.DETECTION_SERVICE_PORT))
        config["websocket_port"] = int(os.getenv("WEBSOCKET_PORT", cls.WEBSOCKET_PORT))
        
        # Configurações de logging
        config["log_level"] = os.getenv("LOG_LEVEL", cls.LOG_LEVEL)
        config["log_format"] = os.getenv("LOG_FORMAT", cls.LOG_FORMAT)
        
        # Configurações de performance
        config["max_connections"] = int(os.getenv("MAX_CONNECTIONS", cls.MAX_CONNECTIONS))
        config["request_timeout"] = int(os.getenv("REQUEST_TIMEOUT", cls.REQUEST_TIMEOUT))
        config["websocket_ping_interval"] = int(os.getenv("WEBSOCKET_PING_INTERVAL", cls.WEBSOCKET_PING_INTERVAL))
        config["websocket_ping_timeout"] = int(os.getenv("WEBSOCKET_PING_TIMEOUT", cls.WEBSOCKET_PING_TIMEOUT))
        
        return config

# Instância global de configuração
config = Config.load_from_env()
