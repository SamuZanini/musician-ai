"""
Script para executar todos os serviços de IA
Implementação simples para desenvolvimento e teste
"""

import subprocess
import sys
import time
import signal
import os
from typing import List, Dict

class ServiceManager:
    """Gerencia execução dos serviços de IA"""
    
    def __init__(self):
        """Inicializa o gerenciador de serviços"""
        self.processes: Dict[str, subprocess.Popen] = {}
        self.services = {
            "ml_service": {
                "script": "ml_service.py",
                "port": 8001,
                "description": "Serviço de ML principal"
            },
            "tuner_service": {
                "script": "tuner_service.py", 
                "port": 8002,
                "description": "Serviço de Afinador"
            },
            "detection_service": {
                "script": "detection_service.py",
                "port": 8003,
                "description": "Serviço de Detecção em Tempo Real"
            }
        }
    
    def start_service(self, service_name: str) -> bool:
        """
        Inicia um serviço específico
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            True se iniciado com sucesso
        """
        if service_name not in self.services:
            print(f"Serviço '{service_name}' não encontrado")
            return False
        
        service_config = self.services[service_name]
        script_path = service_config["script"]
        
        try:
            print(f"Iniciando {service_name} na porta {service_config['port']}...")
            
            # Inicia processo
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[service_name] = process
            print(f"✓ {service_name} iniciado (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao iniciar {service_name}: {e}")
            return False
    
    def stop_service(self, service_name: str) -> bool:
        """
        Para um serviço específico
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            True se parado com sucesso
        """
        if service_name not in self.processes:
            print(f"Serviço '{service_name}' não está rodando")
            return False
        
        try:
            process = self.processes[service_name]
            process.terminate()
            process.wait(timeout=5)
            
            del self.processes[service_name]
            print(f"✓ {service_name} parado")
            return True
            
        except subprocess.TimeoutExpired:
            process.kill()
            del self.processes[service_name]
            print(f"✓ {service_name} forçado a parar")
            return True
        except Exception as e:
            print(f"✗ Erro ao parar {service_name}: {e}")
            return False
    
    def start_all_services(self) -> bool:
        """
        Inicia todos os serviços
        
        Returns:
            True se todos iniciados com sucesso
        """
        print("Iniciando todos os serviços de IA...")
        success = True
        
        for service_name in self.services:
            if not self.start_service(service_name):
                success = False
        
        if success:
            print("\n✓ Todos os serviços iniciados com sucesso!")
            print("\nEndpoints disponíveis:")
            print("  - ML Service: http://localhost:8001")
            print("  - Tuner Service: http://localhost:8002") 
            print("  - Detection Service: http://localhost:8003")
            print("\nPressione Ctrl+C para parar todos os serviços")
        else:
            print("\n✗ Alguns serviços falharam ao iniciar")
        
        return success
    
    def stop_all_services(self):
        """Para todos os serviços"""
        print("\nParando todos os serviços...")
        
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)
        
        print("✓ Todos os serviços parados")
    
    def show_status(self):
        """Mostra status dos serviços"""
        print("\nStatus dos Serviços:")
        print("-" * 50)
        
        for service_name, config in self.services.items():
            if service_name in self.processes:
                process = self.processes[service_name]
                status = "Rodando" if process.poll() is None else "Parado"
                print(f"  {service_name}: {status} (PID: {process.pid})")
            else:
                print(f"  {service_name}: Parado")
        
        print(f"\nTotal de serviços ativos: {len(self.processes)}")

def signal_handler(signum, frame):
    """Manipula sinal de interrupção"""
    print("\n\nRecebido sinal de interrupção...")
    manager.stop_all_services()
    sys.exit(0)

def main():
    """Função principal"""
    global manager
    manager = ServiceManager()
    
    # Configura manipulador de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            manager.start_all_services()
            
            # Mantém serviços rodando
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
                
        elif command == "status":
            manager.show_status()
            
        elif command == "start-service" and len(sys.argv) > 2:
            service_name = sys.argv[2]
            manager.start_service(service_name)
            
        elif command == "stop-service" and len(sys.argv) > 2:
            service_name = sys.argv[2]
            manager.stop_service(service_name)
            
        else:
            print("Comandos disponíveis:")
            print("  start                    - Inicia todos os serviços")
            print("  status                   - Mostra status dos serviços")
            print("  start-service <nome>     - Inicia serviço específico")
            print("  stop-service <nome>      - Para serviço específico")
    else:
        print("Musician AI - Gerenciador de Serviços")
        print("Uso: python run_services.py <comando>")
        print("\nComandos disponíveis:")
        print("  start                    - Inicia todos os serviços")
        print("  status               - Mostra status dos serviços")
        print("  start-service <nome> - Inicia serviço específico")
        print("  stop-service <nome>  - Para serviço específico")

if __name__ == "__main__":
    main()
