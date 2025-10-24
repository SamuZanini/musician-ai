"""
Script de teste para os serviços de IA
Implementação simples para validar funcionalidades
"""

import requests
import json
import time
import numpy as np
import asyncio
import websockets
from typing import Dict, Any

class ServiceTester:
    """Classe para testar os serviços de IA"""
    
    def __init__(self):
        """Inicializa o testador"""
        self.base_urls = {
            "ml_service": "http://localhost:8001",
            "tuner_service": "http://localhost:8002", 
            "detection_service": "http://localhost:8003"
        }
        self.results = {}
    
    def test_ml_service(self) -> Dict[str, Any]:
        """Testa o ML Service"""
        print("🧪 Testando ML Service...")
        results = {"service": "ml_service", "tests": []}
        
        try:
            # Teste 1: Health check
            response = requests.get(f"{self.base_urls['ml_service']}/health", timeout=5)
            if response.status_code == 200:
                results["tests"].append({"test": "health_check", "status": "PASS"})
            else:
                results["tests"].append({"test": "health_check", "status": "FAIL"})
            
            # Teste 2: Detecção de áudio
            # Gera sinal de 440 Hz (A4)
            sample_rate = 44100
            duration = 1.0
            frequency = 440.0
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio_data = np.sin(2 * np.pi * frequency * t).tolist()
            
            response = requests.post(
                f"{self.base_urls['ml_service']}/detect",
                json={"audio_data": audio_data, "sample_rate": sample_rate},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("note") == "A4" and data.get("is_detected"):
                    results["tests"].append({"test": "audio_detection", "status": "PASS"})
                else:
                    results["tests"].append({"test": "audio_detection", "status": "FAIL", "details": data})
            else:
                results["tests"].append({"test": "audio_detection", "status": "FAIL"})
            
            # Teste 3: Lista de notas
            response = requests.get(f"{self.base_urls['ml_service']}/notes", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if len(data.get("notes", {})) > 0:
                    results["tests"].append({"test": "notes_list", "status": "PASS"})
                else:
                    results["tests"].append({"test": "notes_list", "status": "FAIL"})
            else:
                results["tests"].append({"test": "notes_list", "status": "FAIL"})
                
        except Exception as e:
            results["tests"].append({"test": "connection", "status": "FAIL", "error": str(e)})
        
        return results
    
    def test_tuner_service(self) -> Dict[str, Any]:
        """Testa o Tuner Service"""
        print("🎸 Testando Tuner Service...")
        results = {"service": "tuner_service", "tests": []}
        
        try:
            # Teste 1: Health check
            response = requests.get(f"{self.base_urls['tuner_service']}/health", timeout=5)
            if response.status_code == 200:
                results["tests"].append({"test": "health_check", "status": "PASS"})
            else:
                results["tests"].append({"test": "health_check", "status": "FAIL"})
            
            # Teste 2: Afinação
            response = requests.post(
                f"{self.base_urls['tuner_service']}/tune",
                json={"frequency": 440.0, "tolerance_cents": 50},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("note") == "A4" and data.get("is_in_tune"):
                    results["tests"].append({"test": "tuning", "status": "PASS"})
                else:
                    results["tests"].append({"test": "tuning", "status": "FAIL", "details": data})
            else:
                results["tests"].append({"test": "tuning", "status": "FAIL"})
            
            # Teste 3: Instrumentos suportados
            response = requests.get(f"{self.base_urls['tuner_service']}/instruments", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if len(data.get("instruments", [])) > 0:
                    results["tests"].append({"test": "instruments", "status": "PASS"})
                else:
                    results["tests"].append({"test": "instruments", "status": "FAIL"})
            else:
                results["tests"].append({"test": "instruments", "status": "FAIL"})
            
            # Teste 4: Afinação por instrumento
            response = requests.post(
                f"{self.base_urls['tuner_service']}/tune/guitar",
                json={"frequency": 329.63},  # E4 da guitarra
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("instrument") == "guitar":
                    results["tests"].append({"test": "instrument_tuning", "status": "PASS"})
                else:
                    results["tests"].append({"test": "instrument_tuning", "status": "FAIL"})
            else:
                results["tests"].append({"test": "instrument_tuning", "status": "FAIL"})
                
        except Exception as e:
            results["tests"].append({"test": "connection", "status": "FAIL", "error": str(e)})
        
        return results
    
    def test_detection_service(self) -> Dict[str, Any]:
        """Testa o Detection Service"""
        print("🎵 Testando Detection Service...")
        results = {"service": "detection_service", "tests": []}
        
        try:
            # Teste 1: Health check
            response = requests.get(f"{self.base_urls['detection_service']}/health", timeout=5)
            if response.status_code == 200:
                results["tests"].append({"test": "health_check", "status": "PASS"})
            else:
                results["tests"].append({"test": "health_check", "status": "FAIL"})
            
            # Teste 2: Detecção única
            sample_rate = 44100
            frequency = 440.0
            t = np.linspace(0, 1, sample_rate, False)
            audio_data = np.sin(2 * np.pi * frequency * t).tolist()
            
            response = requests.post(
                f"{self.base_urls['detection_service']}/detect",
                json={"audio_data": audio_data, "sample_rate": sample_rate},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("is_detected"):
                    results["tests"].append({"test": "single_detection", "status": "PASS"})
                else:
                    results["tests"].append({"test": "single_detection", "status": "FAIL"})
            else:
                results["tests"].append({"test": "single_detection", "status": "FAIL"})
            
            # Teste 3: Detecção em lote
            batch_data = [
                {"audio_data": audio_data, "sample_rate": sample_rate},
                {"audio_data": audio_data, "sample_rate": sample_rate}
            ]
            
            response = requests.post(
                f"{self.base_urls['detection_service']}/detect/batch",
                json=batch_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if len(data.get("results", [])) == 2:
                    results["tests"].append({"test": "batch_detection", "status": "PASS"})
                else:
                    results["tests"].append({"test": "batch_detection", "status": "FAIL"})
            else:
                results["tests"].append({"test": "batch_detection", "status": "FAIL"})
            
            # Teste 4: Estatísticas
            response = requests.get(f"{self.base_urls['detection_service']}/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "active_connections" in data:
                    results["tests"].append({"test": "stats", "status": "PASS"})
                else:
                    results["tests"].append({"test": "stats", "status": "FAIL"})
            else:
                results["tests"].append({"test": "stats", "status": "FAIL"})
                
        except Exception as e:
            results["tests"].append({"test": "connection", "status": "FAIL", "error": str(e)})
        
        return results
    
    async def test_websocket(self) -> Dict[str, Any]:
        """Testa WebSocket do Detection Service"""
        print("🔌 Testando WebSocket...")
        results = {"service": "websocket", "tests": []}
        
        try:
            uri = "ws://localhost:8003/ws"
            
            async with websockets.connect(uri) as websocket:
                # Teste 1: Conexão
                results["tests"].append({"test": "connection", "status": "PASS"})
                
                # Teste 2: Configuração
                config_message = {
                    "type": "config",
                    "config": {
                        "sample_rate": 44100,
                        "detection_threshold": 0.3
                    }
                }
                await websocket.send(json.dumps(config_message))
                
                response = await websocket.recv()
                data = json.loads(response)
                if data.get("type") == "config_updated":
                    results["tests"].append({"test": "config", "status": "PASS"})
                else:
                    results["tests"].append({"test": "config", "status": "FAIL"})
                
                # Teste 3: Dados de áudio
                sample_rate = 44100
                frequency = 440.0
                t = np.linspace(0, 0.1, int(sample_rate * 0.1), False)
                audio_data = np.sin(2 * np.pi * frequency * t).tolist()
                
                audio_message = {
                    "type": "audio_data",
                    "audio_data": audio_data,
                    "timestamp": time.time()
                }
                await websocket.send(json.dumps(audio_message))
                
                response = await websocket.recv()
                data = json.loads(response)
                if data.get("type") == "detection_result":
                    results["tests"].append({"test": "audio_stream", "status": "PASS"})
                else:
                    results["tests"].append({"test": "audio_stream", "status": "FAIL"})
                
        except Exception as e:
            results["tests"].append({"test": "websocket", "status": "FAIL", "error": str(e)})
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Executa todos os testes"""
        print("🚀 Iniciando testes dos serviços de IA...")
        print("=" * 60)
        
        all_results = {}
        
        # Testa serviços HTTP
        all_results["ml_service"] = self.test_ml_service()
        all_results["tuner_service"] = self.test_tuner_service()
        all_results["detection_service"] = self.test_detection_service()
        
        # Testa WebSocket
        try:
            all_results["websocket"] = asyncio.run(self.test_websocket())
        except Exception as e:
            all_results["websocket"] = {
                "service": "websocket",
                "tests": [{"test": "websocket", "status": "FAIL", "error": str(e)}]
            }
        
        return all_results
    
    def print_results(self, results: Dict[str, Any]):
        """Imprime resultados dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DOS TESTES")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        for service_name, service_results in results.items():
            print(f"\n🔧 {service_name.upper()}")
            print("-" * 40)
            
            for test in service_results.get("tests", []):
                total_tests += 1
                status = test.get("status", "UNKNOWN")
                
                if status == "PASS":
                    passed_tests += 1
                    print(f"  ✅ {test.get('test', 'Unknown')}: PASS")
                else:
                    print(f"  ❌ {test.get('test', 'Unknown')}: FAIL")
                    if test.get("error"):
                        print(f"      Erro: {test['error']}")
                    if test.get("details"):
                        print(f"      Detalhes: {test['details']}")
        
        print("\n" + "=" * 60)
        print(f"📈 RESUMO: {passed_tests}/{total_tests} testes passaram")
        
        if passed_tests == total_tests:
            print("🎉 Todos os testes passaram!")
        else:
            print(f"⚠️  {total_tests - passed_tests} testes falharam")
        
        print("=" * 60)

def main():
    """Função principal"""
    tester = ServiceTester()
    results = tester.run_all_tests()
    tester.print_results(results)

if __name__ == "__main__":
    main()
