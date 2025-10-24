# Musician AI - Módulo de Inteligência Artificial

Este módulo implementa os serviços de IA para o aplicativo Musician AI, focando na detecção de áudio musical e afinação de instrumentos.

## 🎵 Funcionalidades

- **Detecção de Pitch**: Identifica frequências e notas musicais em tempo real
- **Afinador Musical**: Afina instrumentos com feedback visual e sonoro
- **Processamento em Tempo Real**: WebSocket para streaming de áudio
- **Suporte a Múltiplos Instrumentos**: Guitarra, violino, piano, baixo, ukulele

## 🏗️ Arquitetura

### Serviços Implementados

1. **ML Service** (Porta 8001)
   - Detecção básica de pitch e notas
   - Processamento de arquivos de áudio
   - API REST para integração

2. **Tuner Service** (Porta 8002)
   - Afinação específica por instrumento
   - Feedback de afinação em cents
   - Guias de afinação por instrumento

3. **Detection Service** (Porta 8003)
   - Detecção em tempo real via WebSocket
   - Processamento de stream de áudio
   - Configuração dinâmica de parâmetros

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- pip

### Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais

- `aubio`: Detecção de pitch
- `librosa`: Processamento de áudio
- `numpy`: Computação numérica
- `fastapi`: API REST
- `websockets`: Comunicação em tempo real

## 🎯 Uso

### Executar Todos os Serviços

```bash
python run_services.py start
```

### Executar Serviço Específico

```bash
# ML Service
python ml_service.py

# Tuner Service  
python tuner_service.py

# Detection Service
python detection_service.py
```

### Verificar Status

```bash
python run_services.py status
```

## 📡 Endpoints

### ML Service (http://localhost:8001)

- `GET /` - Informações do serviço
- `GET /health` - Status de saúde
- `POST /tune` - Afinação de áudio
- `POST /detect` - Detecção de pitch
- `POST /detect-file` - Upload de arquivo de áudio
- `GET /notes` - Lista de notas musicais

### Tuner Service (http://localhost:8002)

- `GET /` - Informações do serviço
- `GET /health` - Status de saúde
- `GET /instruments` - Instrumentos suportados
- `GET /instruments/{instrument}/notes` - Notas por instrumento
- `POST /tune` - Afinação geral
- `POST /tune/{instrument}` - Afinação por instrumento
- `GET /tune/{instrument}/guide` - Guia de afinação

### Detection Service (http://localhost:8003)

- `GET /` - Informações do serviço
- `GET /health` - Status de saúde
- `POST /detect` - Detecção única
- `POST /detect/batch` - Detecção em lote
- `WebSocket /ws` - Detecção em tempo real
- `GET /stats` - Estatísticas do serviço

## 🔧 Configuração

### Parâmetros de Detecção

- **Sample Rate**: 44100 Hz (padrão)
- **Hop Size**: 512 samples
- **Threshold de Confiança**: 0.3
- **Tolerância de Afinação**: 50 cents

### Instrumentos Suportados

- **Guitarra**: E2, A2, D3, G3, B3, E4
- **Violino**: G3, D4, A4, E5
- **Piano**: A4 (440 Hz)
- **Baixo**: E1, A1, D2, G2
- **Ukulele**: G4, C4, E4, A4

## 🧪 Testes

### Teste Básico de Detecção

```python
import requests
import numpy as np

# Dados de áudio simulados (440 Hz - A4)
audio_data = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100)).tolist()

response = requests.post("http://localhost:8001/detect", json={
    "audio_data": audio_data,
    "sample_rate": 44100
})

print(response.json())
```

### Teste de Afinação

```python
import requests

response = requests.post("http://localhost:8002/tune", json={
    "frequency": 440.0,
    "tolerance_cents": 50
})

print(response.json())
```

## 📊 Monitoramento

### Logs

Os serviços geram logs detalhados para monitoramento:

```bash
# Ver logs em tempo real
tail -f logs/ml_service.log
tail -f logs/tuner_service.log
tail -f logs/detection_service.log
```

### Métricas

- **Latência**: < 500ms para detecção
- **Precisão**: ±50 cents para afinação
- **Throughput**: 100+ detecções/segundo

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de Dependências**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Porta em Uso**
   ```bash
   # Verificar portas em uso
   netstat -tulpn | grep :800
   ```

3. **Erro de Áudio**
   - Verificar permissões de microfone
   - Testar com arquivo de áudio conhecido

### Logs de Debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para suporte técnico ou dúvidas:

- Abra uma issue no GitHub
- Consulte a documentação da API
- Verifique os logs de erro

---

**Desenvolvido com ❤️ para a educação musical**
