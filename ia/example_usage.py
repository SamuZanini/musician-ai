"""
Exemplo de uso dos serviços de IA
Demonstra como utilizar as funcionalidades implementadas
"""

import requests
import json
import numpy as np
import asyncio
import websockets
import time
from typing import List, Dict, Any

class MusicianAIExample:
    """Classe de exemplo para uso dos serviços de IA"""
    
    def __init__(self):
        """Inicializa o exemplo"""
        self.base_urls = {
            "ml_service": "http://localhost:8001",
            "tuner_service": "http://localhost:8002",
            "detection_service": "http://localhost:8003"
        }
    
    def generate_audio_signal(self, frequency: float, duration: float = 1.0, sample_rate: int = 44100) -> List[float]:
        """
        Gera sinal de áudio sintético
        
        Args:
            frequency: Frequência em Hz
            duration: Duração em segundos
            sample_rate: Taxa de amostragem
            
        Returns:
            Lista com dados de áudio
        """
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        signal = np.sin(2 * np.pi * frequency * t)
        return signal.tolist()
    
    def example_ml_service(self):
        """Exemplo de uso do ML Service"""
        print("🎵 Exemplo: ML Service")
        print("-" * 40)
        
        try:
            # 1. Verificar saúde do serviço
            print("1. Verificando saúde do serviço...")
            response = requests.get(f"{self.base_urls['ml_service']}/health")
            print(f"   Status: {response.json()}")
            
            # 2. Detectar nota A4 (440 Hz)
            print("\n2. Detectando nota A4 (440 Hz)...")
            audio_data = self.generate_audio_signal(440.0)
            
            response = requests.post(
                f"{self.base_urls['ml_service']}/detect",
                json={"audio_data": audio_data, "sample_rate": 44100}
            )
            
            result = response.json()
            print(f"   Nota detectada: {result['note']}")
            print(f"   Pitch: {result['pitch']} Hz")
            print(f"   Confiança: {result['confidence']:.2f}")
            print(f"   Detectado: {result['is_detected']}")
            
            # 3. Listar notas disponíveis
            print("\n3. Listando notas disponíveis...")
            response = requests.get(f"{self.base_urls['ml_service']}/notes")
            notes = response.json()
            print(f"   Total de notas: {notes['total_notes']}")
            print(f"   Primeiras 5 notas: {list(notes['notes'].keys())[:5]}")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    def example_tuner_service(self):
        """Exemplo de uso do Tuner Service"""
        print("\n🎸 Exemplo: Tuner Service")
        print("-" * 40)
        
        try:
            # 1. Verificar saúde do serviço
            print("1. Verificando saúde do serviço...")
            response = requests.get(f"{self.base_urls['tuner_service']}/health")
            print(f"   Status: {response.json()}")
            
            # 2. Afinar nota A4
            print("\n2. Afinando nota A4...")
            response = requests.post(
                f"{self.base_urls['tuner_service']}/tune",
                json={"frequency": 440.0, "tolerance_cents": 50}
            )
            
            result = response.json()
            print(f"   Nota atual: {result['current_note']}")
            print(f"   Nota alvo: {result['target_note']}")
            print(f"   Frequência: {result['frequency']} Hz")
            print(f"   Frequência alvo: {result['target_frequency']} Hz")
            print(f"   Diferença: {result['cents_diff']} cents")
            print(f"   Afinado: {result['is_in_tune']}")
            print(f"   Direção: {result['tuning_direction']}")
            
            # 3. Listar instrumentos suportados
            print("\n3. Listando instrumentos suportados...")
            response = requests.get(f"{self.base_urls['tuner_service']}/instruments")
            instruments = response.json()
            print(f"   Instrumentos: {instruments['instruments']}")
            
            # 4. Afinar guitarra
            print("\n4. Afinando guitarra (E4)...")
            response = requests.post(
                f"{self.base_urls['tuner_service']}/tune/guitar",
                json={"frequency": 329.63}  # E4 da guitarra
            )
            
            result = response.json()
            print(f"   Instrumento: {result['instrument']}")
            print(f"   Nota atual: {result['current_note']}")
            print(f"   Nota alvo: {result['target_note']}")
            print(f"   Afinado: {result['is_in_tune']}")
            
            # 5. Guia de afinação da guitarra
            print("\n5. Guia de afinação da guitarra...")
            response = requests.get(f"{self.base_urls['tuner_service']}/tune/guitar/guide")
            guide = response.json()
            print(f"   Total de cordas: {guide['total_strings']}")
            for string_info in guide['tuning_guide']:
                print(f"   {string_info['order']}. {string_info['note']}: {string_info['frequency']} Hz")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    def example_detection_service(self):
        """Exemplo de uso do Detection Service"""
        print("\n🎯 Exemplo: Detection Service")
        print("-" * 40)
        
        try:
            # 1. Verificar saúde do serviço
            print("1. Verificando saúde do serviço...")
            response = requests.get(f"{self.base_urls['detection_service']}/health")
            print(f"   Status: {response.json()}")
            
            # 2. Detecção única
            print("\n2. Detecção única...")
            audio_data = self.generate_audio_signal(440.0)
            
            response = requests.post(
                f"{self.base_urls['detection_service']}/detect",
                json={"audio_data": audio_data, "sample_rate": 44100, "instrument": "guitar"}
            )
            
            result = response.json()
            print(f"   Nota: {result['note']}")
            print(f"   Pitch: {result['pitch']} Hz")
            print(f"   Confiança: {result['confidence']:.2f}")
            print(f"   Detectado: {result['is_detected']}")
            print(f"   Instrumento: {result['instrument']}")
            
            # 3. Detecção em lote
            print("\n3. Detecção em lote...")
            batch_data = [
                {"audio_data": self.generate_audio_signal(440.0), "sample_rate": 44100},
                {"audio_data": self.generate_audio_signal(523.25), "sample_rate": 44100}  # C5
            ]
            
            response = requests.post(
                f"{self.base_urls['detection_service']}/detect/batch",
                json=batch_data
            )
            
            results = response.json()
            print(f"   Total de resultados: {results['total']}")
            for i, result in enumerate(results['results']):
                print(f"   Resultado {i+1}: {result['note']} ({result['pitch']} Hz)")
            
            # 4. Estatísticas
            print("\n4. Estatísticas do serviço...")
            response = requests.get(f"{self.base_urls['detection_service']}/stats")
            stats = response.json()
            print(f"   Conexões ativas: {stats['active_connections']}")
            print(f"   Status: {stats['service_status']}")
            print(f"   Instrumentos suportados: {stats['supported_instruments']}")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    async def example_websocket(self):
        """Exemplo de uso do WebSocket"""
        print("\n🔌 Exemplo: WebSocket")
        print("-" * 40)
        
        try:
            uri = "ws://localhost:8003/ws"
            
            async with websockets.connect(uri) as websocket:
                print("1. Conectado ao WebSocket")
                
                # 2. Configurar detecção
                print("\n2. Configurando detecção...")
                config_message = {
                    "type": "config",
                    "config": {
                        "sample_rate": 44100,
                        "detection_threshold": 0.3,
                        "instrument": "guitar"
                    }
                }
                await websocket.send(json.dumps(config_message))
                
                response = await websocket.recv()
                config_result = json.loads(response)
                print(f"   Configuração: {config_result['message']}")
                
                # 3. Enviar dados de áudio
                print("\n3. Enviando dados de áudio...")
                audio_data = self.generate_audio_signal(440.0, duration=0.1)
                
                audio_message = {
                    "type": "audio_data",
                    "audio_data": audio_data,
                    "timestamp": time.time()
                }
                await websocket.send(json.dumps(audio_message))
                
                response = await websocket.recv()
                detection_result = json.loads(response)
                print(f"   Tipo: {detection_result['type']}")
                print(f"   Nota: {detection_result['note']}")
                print(f"   Pitch: {detection_result['pitch']} Hz")
                print(f"   Confiança: {detection_result['confidence']:.2f}")
                print(f"   Detectado: {detection_result['is_detected']}")
                
                # 4. Teste de ping
                print("\n4. Testando ping...")
                ping_message = {"type": "ping"}
                await websocket.send(json.dumps(ping_message))
                
                response = await websocket.recv()
                pong_result = json.loads(response)
                print(f"   Resposta: {pong_result['type']}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    def run_all_examples(self):
        """Executa todos os exemplos"""
        print("🚀 Exemplos de Uso dos Serviços de IA")
        print("=" * 60)
        
        # Exemplos HTTP
        self.example_ml_service()
        self.example_tuner_service()
        self.example_detection_service()
        
        # Exemplo WebSocket
        print("\n🔌 Executando exemplo WebSocket...")
        try:
            asyncio.run(self.example_websocket())
        except Exception as e:
            print(f"   ❌ Erro no WebSocket: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Exemplos concluídos!")
        print("=" * 60)

def main():
    """Função principal"""
    example = MusicianAIExample()
    example.run_all_examples()

if __name__ == "__main__":
    main()
