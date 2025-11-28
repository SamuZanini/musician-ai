# Documentação da API - Musician AI ML Services

Documentação completa dos endpoints dos serviços de Machine Learning para detecção de áudio musical.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [ML Service (Porta 8001)](#ml-service-porta-8001)
- [Tuner Service (Porta 8002)](#tuner-service-porta-8002)
- [Detection Service (Porta 8003)](#detection-service-porta-8003)
- [Real-Time Processor (WebSocket 8765)](#real-time-processor-websocket-8765)
- [Códigos de Erro](#códigos-de-erro)
- [Exemplos de Integração](#exemplos-de-integração)

---

## Visão Geral

O sistema Musician AI ML é composto por 5 serviços principais:

| Serviço | Porta | Protocolo | Descrição |
|---------|-------|-----------|-----------|
| ML Service | 8001 | HTTP/REST | Detecção básica de pitch e notas |
| Tuner Service | 8002 | HTTP/REST | Afinação específica por instrumento |
| Detection Service | 8003 | HTTP/REST + WebSocket | Detecção em tempo real |
| Practice Service | 8004 | HTTP/REST | Validação de prática musical |
| Real-Time Processor | 8765 | WebSocket | Processamento de stream de áudio |

**Base URL:** `http://localhost:8001` (ML Service), `http://localhost:8002` (Tuner), `http://localhost:8003` (Detection), `http://localhost:8004` (Practice)

---

## ML Service (Porta 8001)

Serviço principal para detecção de pitch e notas musicais.

### Endpoints

#### `GET /`

Retorna informações sobre o serviço e lista de endpoints disponíveis.

**Requisição:**
```http
GET http://localhost:8001/
```

**Resposta:**
```json
{
  "message": "Musician AI - ML Service",
  "version": "1.0.0",
  "endpoints": {
    "tune": "/tune",
    "detect": "/detect",
    "health": "/health"
  }
}
```

---

#### `GET /health`

Verifica o status de saúde do serviço.

**Requisição:**
```http
GET http://localhost:8001/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "ml-service"
}
```

---

#### `POST /tune`

Endpoint para afinação de áudio. Recebe uma frequência e retorna feedback de afinação.

**Requisição:**
```http
POST http://localhost:8001/tune
Content-Type: application/json
```

**Body:**
```json
{
  "frequency": 440.0,
  "tolerance_cents": 50
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `frequency` | `float` | Sim | - | Frequência detectada em Hz |
| `tolerance_cents` | `float` | Não | `50` | Tolerância em cents para considerar afinado |

**Resposta de Sucesso (200):**
```json
{
  "note": "A4",
  "frequency": 440.0,
  "is_in_tune": true,
  "cents_diff": 2.5,
  "tuning_direction": "Afinado",
  "confidence": 0.8
}
```

**Campos da Resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `note` | `string` | Nota musical detectada (ex: "A4", "C#5") |
| `frequency` | `float` | Frequência detectada em Hz |
| `is_in_tune` | `boolean` | Indica se está afinado dentro da tolerância |
| `cents_diff` | `float` | Diferença em cents da nota ideal |
| `tuning_direction` | `string` | Direção de afinação: "Afinado", "Muito alto", "Muito baixo" |
| `confidence` | `float` | Confiança da detecção (0.0 a 1.0) |

**Exemplo com cURL:**
```bash
curl -X POST http://localhost:8001/tune \
  -H "Content-Type: application/json" \
  -d '{
    "frequency": 440.0,
    "tolerance_cents": 50
  }'
```

**Exemplo com Python:**
```python
import requests

response = requests.post(
    "http://localhost:8001/tune",
    json={
        "frequency": 440.0,
        "tolerance_cents": 50
    }
)

data = response.json()
print(f"Nota: {data['note']}")
print(f"Está afinado: {data['is_in_tune']}")
```

---

#### `POST /detect`

Endpoint para detecção de áudio em tempo real. Processa dados de áudio e retorna pitch detectado.

**Requisição:**
```http
POST http://localhost:8001/detect
Content-Type: application/json
```

**Body:**
```json
{
  "audio_data": [0.1, 0.2, 0.15, -0.1, -0.2, ...],
  "sample_rate": 44100
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `audio_data` | `array[float]` | Sim | - | Array com amostras de áudio (normalizadas entre -1.0 e 1.0) |
| `sample_rate` | `int` | Não | `44100` | Taxa de amostragem do áudio em Hz |

**Resposta de Sucesso (200):**
```json
{
  "pitch": 440.5,
  "note": "A4",
  "confidence": 0.85,
  "is_detected": true
}
```

**Campos da Resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `pitch` | `float \| null` | Frequência detectada em Hz (null se não detectado) |
| `note` | `string` | Nota musical detectada ou "Silêncio" |
| `confidence` | `float` | Confiança da detecção (0.0 a 1.0) |
| `is_detected` | `boolean` | Indica se uma nota foi detectada (confidence > 0.3) |

**Exemplo com Python:**
```python
import requests
import numpy as np

# Gera dados de áudio simulados (440 Hz - A4)
sample_rate = 44100
duration = 0.1  # 100ms
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t).tolist()

response = requests.post(
    "http://localhost:8001/detect",
    json={
        "audio_data": audio_data,
        "sample_rate": sample_rate
    }
)

data = response.json()
print(f"Pitch detectado: {data['pitch']} Hz")
print(f"Nota: {data['note']}")
print(f"Confiança: {data['confidence']}")
```

---

#### `POST /detect-file`

Endpoint para detecção de áudio via upload de arquivo.

**Requisição:**
```http
POST http://localhost:8001/detect-file
Content-Type: multipart/form-data
```

**Body (multipart/form-data):**
- `file`: Arquivo de áudio (WAV, MP3, FLAC, etc.)

**Resposta de Sucesso (200):**
```json
{
  "pitch": 440.5,
  "note": "A4",
  "confidence": 0.85,
  "cents_diff": 2.1,
  "is_tuned": true,
  "sample_rate": 44100
}
```

**Exemplo com cURL:**
```bash
curl -X POST http://localhost:8001/detect-file \
  -F "file=@audio_sample.wav"
```

**Exemplo com Python:**
```python
import requests

with open("audio_sample.wav", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8001/detect-file",
        files=files
    )

data = response.json()
print(f"Nota detectada: {data['note']}")
```

---

#### `GET /notes`

Retorna lista completa de notas musicais e suas frequências.

**Requisição:**
```http
GET http://localhost:8001/notes
```

**Resposta:**
```json
{
  "notes": {
    "C0": 16.35,
    "C#0": 17.32,
    "D0": 18.35,
    ...
    "A4": 440.0,
    ...
    "B7": 3951.07
  },
  "total_notes": 96
}
```

**Exemplo:**
```python
import requests

response = requests.get("http://localhost:8001/notes")
data = response.json()

print(f"Total de notas: {data['total_notes']}")
print(f"Frequência de A4: {data['notes']['A4']} Hz")
```

---

## Tuner Service (Porta 8002)

Serviço especializado em afinação de instrumentos musicais.

### Endpoints

#### `GET /`

Retorna informações sobre o serviço.

**Requisição:**
```http
GET http://localhost:8002/
```

**Resposta:**
```json
{
  "message": "Musician AI - Tuner Service",
  "version": "1.0.0",
  "endpoints": {
    "tune": "/tune",
    "instruments": "/instruments",
    "health": "/health"
  }
}
```

---

#### `GET /health`

Verifica o status de saúde do serviço.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "tuner-service"
}
```

---

#### `GET /instruments`

Retorna lista de instrumentos suportados.

**Requisição:**
```http
GET http://localhost:8002/instruments
```

**Resposta:**
```json
{
  "instruments": ["guitar", "violin", "piano"],
  "total": 3
}
```

---

#### `GET /instruments/{instrument}/notes`

Retorna notas de afinação para um instrumento específico.

**Requisição:**
```http
GET http://localhost:8002/instruments/violin/notes
```

**Parâmetros de URL:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `instrument` | `string` | Nome do instrumento (guitar, violin, piano, bass, ukulele) |

**Resposta de Sucesso (200):**
```json
{
  "instrument": "violin",
  "notes": {
    "E5": 659.25,
    "A4": 440.0,
    "D4": 293.66,
    "G3": 196.0
  },
  "total_notes": 4
}
```

**Resposta de Erro (404):**
```json
{
  "detail": "Instrumento 'xyz' não suportado"
}
```

**Exemplo:**
```python
import requests

response = requests.get("http://localhost:8002/instruments/violin/notes")
data = response.json()

for note, freq in data["notes"].items():
    print(f"{note}: {freq} Hz")
```

---

#### `POST /tune`

Endpoint principal para afinação. Detecta a nota atual e compara com a nota alvo.

**Requisição:**
```http
POST http://localhost:8002/tune
Content-Type: application/json
```

**Body:**
```json
{
  "frequency": 440.0,
  "target_note": "A4",
  "tolerance_cents": 50
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `frequency` | `float` | Sim | - | Frequência detectada em Hz |
| `target_note` | `string` | Não | `null` | Nota alvo (ex: "A4"). Se não fornecido, usa a nota mais próxima |
| `tolerance_cents` | `float` | Não | `50` | Tolerância em cents |

**Resposta de Sucesso (200):**
```json
{
  "current_note": "A4",
  "target_note": "A4",
  "frequency": 440.0,
  "target_frequency": 440.0,
  "cents_diff": 0.0,
  "is_in_tune": true,
  "tuning_direction": "Afinado",
  "confidence": 0.8
}
```

**Exemplo:**
```python
import requests

response = requests.post(
    "http://localhost:8002/tune",
    json={
        "frequency": 442.0,  # Ligeiramente acima de A4
        "target_note": "A4",
        "tolerance_cents": 50
    }
)

data = response.json()
print(f"Nota atual: {data['current_note']}")
print(f"Está afinado: {data['is_in_tune']}")
print(f"Direção: {data['tuning_direction']}")
print(f"Diferença: {data['cents_diff']} cents")
```

---

#### `POST /tune/{instrument}`

Afina para um instrumento específico. Encontra automaticamente a nota mais próxima do instrumento.

**Requisição:**
```http
POST http://localhost:8002/tune/violin
Content-Type: application/json
```

**Parâmetros de URL:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `instrument` | `string` | Nome do instrumento |

**Body:**
```json
{
  "frequency": 440.0,
  "tolerance_cents": 50
}
```

**Resposta de Sucesso (200):**
```json
{
  "instrument": "violin",
  "current_note": "A4",
  "target_note": "A4",
  "frequency": 440.0,
  "target_frequency": 440.0,
  "cents_diff": 0.0,
  "is_in_tune": true,
  "tuning_direction": "Afinado",
  "confidence": 0.8
}
```

**Exemplo:**
```python
import requests

# Afina violino com frequência detectada
response = requests.post(
    "http://localhost:8002/tune/violin",
    json={
        "frequency": 293.5,  # Próximo de D4
        "tolerance_cents": 50
    }
)

data = response.json()
print(f"Nota alvo do violino: {data['target_note']}")
print(f"Frequência alvo: {data['target_frequency']} Hz")
```

---

#### `GET /tune/{instrument}/guide`

Retorna guia de afinação ordenado para um instrumento.

**Requisição:**
```http
GET http://localhost:8002/tune/violin/guide
```

**Resposta de Sucesso (200):**
```json
{
  "instrument": "violin",
  "tuning_guide": [
    {
      "note": "G3",
      "frequency": 196.0,
      "order": 1
    },
    {
      "note": "D4",
      "frequency": 293.66,
      "order": 2
    },
    {
      "note": "A4",
      "frequency": 440.0,
      "order": 3
    },
    {
      "note": "E5",
      "frequency": 659.25,
      "order": 4
    }
  ],
  "total_strings": 4
}
```

**Exemplo:**
```python
import requests

response = requests.get("http://localhost:8002/tune/guitar/guide")
data = response.json()

print(f"Guia de afinação para {data['instrument']}:")
for string_info in data["tuning_guide"]:
    print(f"  {string_info['order']}. {string_info['note']}: {string_info['frequency']} Hz")
```

---

## Detection Service (Porta 8003)

Serviço para detecção de áudio em tempo real com suporte a WebSocket.

### Endpoints HTTP

#### `GET /`

Informações sobre o serviço.

**Resposta:**
```json
{
  "message": "Musician AI - Detection Service",
  "version": "1.0.0",
  "endpoints": {
    "detect": "/detect",
    "websocket": "/ws",
    "health": "/health"
  }
}
```

---

#### `GET /health`

Status de saúde do serviço.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "detection-service",
  "active_connections": 2
}
```

---

#### `POST /detect`

Detecção única de áudio.

**Requisição:**
```http
POST http://localhost:8003/detect
Content-Type: application/json
```

**Body:**
```json
{
  "audio_data": [0.1, 0.2, 0.15, ...],
  "sample_rate": 44100,
  "instrument": "violin"
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `audio_data` | `array[float]` | Sim | - | Array com amostras de áudio |
| `sample_rate` | `int` | Não | `44100` | Taxa de amostragem |
| `instrument` | `string` | Não | `null` | Nome do instrumento (opcional) |

**Resposta:**
```json
{
  "pitch": 440.5,
  "note": "A4",
  "confidence": 0.85,
  "is_detected": true,
  "timestamp": 1234567890.123,
  "instrument": "violin"
}
```

---

#### `POST /detect/batch`

Detecção em lote de múltiplos áudios.

**Requisição:**
```http
POST http://localhost:8003/detect/batch
Content-Type: application/json
```

**Body:**
```json
[
  {
    "audio_data": [0.1, 0.2, ...],
    "sample_rate": 44100,
    "instrument": "violin"
  },
  {
    "audio_data": [0.15, 0.25, ...],
    "sample_rate": 44100,
    "instrument": "guitar"
  }
]
```

**Resposta:**
```json
{
  "results": [
    {
      "pitch": 440.5,
      "note": "A4",
      "confidence": 0.85,
      "is_detected": true,
      "instrument": "violin"
    },
    {
      "pitch": 329.63,
      "note": "E4",
      "confidence": 0.78,
      "is_detected": true,
      "instrument": "guitar"
    }
  ],
  "total": 2
}
```

---

#### `GET /stats`

Estatísticas do serviço.

**Resposta:**
```json
{
  "active_connections": 2,
  "service_status": "running",
  "supported_instruments": ["guitar", "violin", "piano", "bass", "ukulele"]
}
```

---

### WebSocket Endpoint

#### `WS /ws`

Endpoint WebSocket para detecção em tempo real.

**URL:** `ws://localhost:8003/ws`

**Mensagens Enviadas pelo Cliente:**

1. **Configuração:**
```json
{
  "type": "config",
  "config": {
    "sample_rate": 44100,
    "buffer_size": 1024,
    "detection_threshold": 0.3,
    "instrument": "violin"
  }
}
```

2. **Dados de Áudio:**
```json
{
  "type": "audio_data",
  "audio_data": [0.1, 0.2, 0.15, ...],
  "timestamp": 1234567890.123
}
```

3. **Ping:**
```json
{
  "type": "ping"
}
```

**Mensagens Recebidas do Servidor:**

1. **Resultado de Detecção:**
```json
{
  "type": "detection_result",
  "pitch": 440.5,
  "note": "A4",
  "confidence": 0.85,
  "is_detected": true,
  "cents_diff": 2.1,
  "timestamp": 1234567890.123,
  "instrument": "violin"
}
```

2. **Configuração Atualizada:**
```json
{
  "type": "config_updated",
  "message": "Configuração atualizada"
}
```

3. **Pong:**
```json
{
  "type": "pong"
}
```

**Exemplo com JavaScript:**
```javascript
const ws = new WebSocket('ws://localhost:8003/ws');

// Configurar
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'config',
    config: {
      sample_rate: 44100,
      detection_threshold: 0.3,
      instrument: 'violin'
    }
  }));
};

// Enviar dados de áudio
function sendAudioData(audioBuffer) {
  const audioData = Array.from(audioBuffer);
  ws.send(JSON.stringify({
    type: 'audio_data',
    audio_data: audioData,
    timestamp: Date.now() / 1000
  }));
}

// Receber resultados
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'detection_result') {
    console.log(`Nota detectada: ${data.note}`);
    console.log(`Pitch: ${data.pitch} Hz`);
    console.log(`Confiança: ${data.confidence}`);
  }
};
```

**Exemplo com Python:**
```python
import asyncio
import websockets
import json
import numpy as np

async def detect_audio():
    uri = "ws://localhost:8003/ws"
    
    async with websockets.connect(uri) as websocket:
        # Configurar
        config = {
            "type": "config",
            "config": {
                "sample_rate": 44100,
                "detection_threshold": 0.3,
                "instrument": "violin"
            }
        }
        await websocket.send(json.dumps(config))
        
        # Enviar dados de áudio
        sample_rate = 44100
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t).tolist()
        
        message = {
            "type": "audio_data",
            "audio_data": audio_data,
            "timestamp": asyncio.get_event_loop().time()
        }
        await websocket.send(json.dumps(message))
        
        # Receber resultado
        response = await websocket.recv()
        data = json.loads(response)
        print(f"Nota: {data['note']}")
        print(f"Pitch: {data['pitch']} Hz")

asyncio.run(detect_audio())
```

---

## Real-Time Processor (WebSocket 8765)

Servidor WebSocket standalone para processamento de stream de áudio.

**URL:** `ws://localhost:8765`

**Mensagens Enviadas pelo Cliente:**

1. **Iniciar Stream:**
```json
{
  "type": "start_stream"
}
```

2. **Dados de Áudio:**
```json
{
  "type": "audio_data",
  "audio_data": [0.1, 0.2, 0.15, ...],
  "sample_rate": 44100,
  "timestamp": 1234567890.123
}
```

3. **Parar Stream:**
```json
{
  "type": "stop_stream"
}
```

**Mensagens Recebidas do Servidor:**

1. **Resultado de Detecção:**
```json
{
  "type": "detection_result",
  "pitch": 440.5,
  "note": "A4",
  "confidence": 0.85,
  "cents_diff": 2.1,
  "is_tuned": true,
  "is_detected": true,
  "timestamp": 1234567890.123
}
```

2. **Stream Iniciado:**
```json
{
  "type": "stream_started",
  "message": "Processamento iniciado"
}
```

3. **Stream Parado:**
```json
{
  "type": "stream_stopped",
  "message": "Processamento parado"
}
```

4. **Erro:**
```json
{
  "type": "error",
  "message": "Descrição do erro"
}
```

---

## Códigos de Erro

### HTTP Status Codes

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| `200` | OK | Requisição bem-sucedida |
| `400` | Bad Request | Parâmetros inválidos ou faltando |
| `404` | Not Found | Recurso não encontrado (ex: instrumento não suportado) |
| `500` | Internal Server Error | Erro interno do servidor |

### Exemplos de Respostas de Erro

**400 Bad Request:**
```json
{
  "detail": "Frequência não fornecida"
}
```

**404 Not Found:**
```json
{
  "detail": "Instrumento 'xyz' não suportado"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Erro interno: [descrição do erro]"
}
```

---

## Exemplos de Integração

### Exemplo Completo: Afinação de Violino

```python
import requests
import time

# 1. Verificar instrumentos disponíveis
response = requests.get("http://localhost:8002/instruments")
print(f"Instrumentos disponíveis: {response.json()['instruments']}")

# 2. Obter notas do violino
response = requests.get("http://localhost:8002/instruments/violin/notes")
violin_notes = response.json()["notes"]
print(f"Notas do violino: {violin_notes}")

# 3. Afinar cada corda
for note, target_freq in violin_notes.items():
    # Simula frequência detectada (ligeiramente fora de afinação)
    detected_freq = target_freq + 2.0
    
    response = requests.post(
        "http://localhost:8002/tune/violin",
        json={
            "frequency": detected_freq,
            "tolerance_cents": 50
        }
    )
    
    data = response.json()
    print(f"\nCorda {note}:")
    print(f"  Frequência detectada: {data['frequency']} Hz")
    print(f"  Frequência alvo: {data['target_frequency']} Hz")
    print(f"  Diferença: {data['cents_diff']} cents")
    print(f"  Status: {data['tuning_direction']}")
    print(f"  Está afinado: {data['is_in_tune']}")
    
    time.sleep(0.5)
```

### Exemplo Completo: Detecção em Tempo Real com WebSocket

```python
import asyncio
import websockets
import json
import numpy as np

async def real_time_detection():
    uri = "ws://localhost:8003/ws"
    
    async with websockets.connect(uri) as websocket:
        # Configurar
        await websocket.send(json.dumps({
            "type": "config",
            "config": {
                "sample_rate": 44100,
                "buffer_size": 1024,
                "detection_threshold": 0.3,
                "instrument": "violin"
            }
        }))
        
        # Aguardar confirmação
        response = await websocket.recv()
        print(f"Configuração: {json.loads(response)}")
        
        # Simular envio contínuo de áudio
        sample_rate = 44100
        buffer_size = 1024
        
        for i in range(10):  # 10 buffers
            # Gera áudio sintético (440 Hz - A4)
            t = np.linspace(0, buffer_size / sample_rate, buffer_size)
            audio_data = np.sin(2 * np.pi * 440 * t).tolist()
            
            # Envia dados
            await websocket.send(json.dumps({
                "type": "audio_data",
                "audio_data": audio_data,
                "timestamp": asyncio.get_event_loop().time()
            }))
            
            # Recebe resultado
            response = await websocket.recv()
            data = json.loads(response)
            
            if data["type"] == "detection_result":
                print(f"Buffer {i+1}:")
                print(f"  Nota: {data['note']}")
                print(f"  Pitch: {data['pitch']} Hz")
                print(f"  Confiança: {data['confidence']:.2f}")
                print(f"  Detectado: {data['is_detected']}")
            
            await asyncio.sleep(0.1)  # 100ms entre buffers

asyncio.run(real_time_detection())
```

### Exemplo: Integração com Frontend (JavaScript)

```javascript
// Função para detectar nota usando ML Service
async function detectNote(audioBuffer) {
  const audioData = Array.from(audioBuffer);
  
  const response = await fetch('http://localhost:8001/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      audio_data: audioData,
      sample_rate: 44100
    })
  });
  
  const data = await response.json();
  return data;
}

// Função para afinar usando Tuner Service
async function tuneInstrument(frequency, targetNote, tolerance = 50) {
  const response = await fetch('http://localhost:8002/tune', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      frequency: frequency,
      target_note: targetNote,
      tolerance_cents: tolerance
    })
  });
  
  const data = await response.json();
  return data;
}

// Exemplo de uso
const audioBuffer = /* ... dados do microfone ... */;
const result = await detectNote(audioBuffer);
console.log(`Nota detectada: ${result.note}`);

const tuning = await tuneInstrument(result.pitch, 'A4');
console.log(`Está afinado: ${tuning.is_in_tune}`);
console.log(`Direção: ${tuning.tuning_direction}`);
```

---

## Notas Importantes

1. **Taxa de Amostragem:** O padrão é 44100 Hz. Certifique-se de que os dados de áudio correspondem à taxa especificada.

2. **Formato de Áudio:** Os arrays de áudio devem estar normalizados entre -1.0 e 1.0 (float32).

3. **Confiança:** O threshold padrão de confiança é 0.3. Valores abaixo disso são considerados "Silêncio".

4. **Tolerância de Afinação:** O padrão é 50 cents. Ajuste conforme necessário para maior ou menor precisão.

5. **Instrumentos Suportados:** Atualmente suporta guitar, violin, piano, bass e ukulele.

6. **WebSocket:** Mantenha a conexão WebSocket aberta para detecção contínua. Use ping/pong para manter a conexão viva.

---

## Suporte

Para mais informações, consulte:
- `README.md` - Documentação geral do projeto
- `example_usage.py` - Exemplos de uso
- `test_services.py` - Testes dos serviços

---

## Practice Service (Porta 8004)

Serviço especializado para validação de notas durante prática musical.

### Endpoints

#### `GET /`

Informações sobre o serviço.

**Resposta:**
```json
{
  "message": "Musician AI - Practice Service",
  "version": "1.0.0",
  "endpoints": {
    "check": "/practice/check",
    "session": "/practice/session",
    "health": "/health"
  }
}
```

---

#### `GET /health`

Status de saúde do serviço.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "practice-service"
}
```

---

#### `POST /practice/check`

Valida se a nota tocada (via frequência) corresponde à nota alvo. Retorna análise completa incluindo acerto/erro, precisão, feedback, etc.

**Requisição:**
```http
POST http://localhost:8004/practice/check
Content-Type: application/json
```

**Body:**
```json
{
  "frequency": 440.5,
  "target_note": "A4",
  "tolerance_cents": 50,
  "instrument": "violin"
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `frequency` | `float` | Sim | - | Frequência detectada em Hz |
| `target_note` | `string` | Sim | - | Nota alvo esperada (ex: "A4", "C#5") |
| `tolerance_cents` | `float` | Não | `50` | Tolerância em cents |
| `instrument` | `string` | Não | `null` | Nome do instrumento (opcional) |

**Resposta de Sucesso (200):**
```json
{
  "detected_note": "A4",
  "target_note": "A4",
  "frequency": 440.5,
  "target_frequency": 440.0,
  "is_correct": true,
  "confidence": 0.8,
  "cents_diff": 2.0,
  "accuracy_score": 95.2,
  "feedback_message": "Perfeito! Nota correta e bem afinada.",
  "tuning_direction": "Afinado",
  "harmonics_detected": null
}
```

**Campos da Resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `detected_note` | `string` | Nota detectada pelo ML |
| `target_note` | `string` | Nota alvo esperada |
| `frequency` | `float` | Frequência detectada em Hz |
| `target_frequency` | `float` | Frequência ideal da nota alvo |
| `is_correct` | `boolean` | Indica se a nota está correta e afinada |
| `confidence` | `float` | Confiança da detecção (0.0 a 1.0) |
| `cents_diff` | `float` | Diferença em cents da nota ideal |
| `accuracy_score` | `float` | Score de precisão de 0 a 100 |
| `feedback_message` | `string` | Mensagem de feedback para o usuário |
| `tuning_direction` | `string` | Direção de afinação: "Afinado", "Muito alto", "Muito baixo" |
| `harmonics_detected` | `array[float] \| null` | Frequências de harmônicos detectados |

**Exemplo com Python:**
```python
import requests

response = requests.post(
    "http://localhost:8004/practice/check",
    json={
        "frequency": 440.5,
        "target_note": "A4",
        "tolerance_cents": 50
    }
)

data = response.json()
print(f"Nota detectada: {data['detected_note']}")
print(f"Acertou: {data['is_correct']}")
print(f"Precisão: {data['accuracy_score']}%")
print(f"Feedback: {data['feedback_message']}")
```

---

#### `POST /practice/session`

Processa áudio completo de uma sessão de prática e valida contra nota alvo. Retorna análise completa incluindo detecção de harmônicos.

**Requisição:**
```http
POST http://localhost:8004/practice/session
Content-Type: application/json
```

**Body:**
```json
{
  "audio_data": [0.1, 0.2, 0.15, -0.1, -0.2, ...],
  "target_note": "A4",
  "sample_rate": 44100,
  "tolerance_cents": 50,
  "instrument": "violin"
}
```

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `audio_data` | `array[float]` | Sim | - | Array com amostras de áudio |
| `target_note` | `string` | Sim | - | Nota alvo esperada |
| `sample_rate` | `int` | Não | `44100` | Taxa de amostragem |
| `tolerance_cents` | `float` | Não | `50` | Tolerância em cents |
| `instrument` | `string` | Não | `null` | Nome do instrumento |

**Resposta de Sucesso (200):**
```json
{
  "detected_note": "A4",
  "target_note": "A4",
  "pitch": 440.5,
  "target_frequency": 440.0,
  "is_correct": true,
  "confidence": 0.85,
  "cents_diff": 2.0,
  "accuracy_score": 95.2,
  "feedback_message": "Perfeito! Nota correta e bem afinada.",
  "tuning_direction": "Afinado",
  "is_detected": true,
  "harmonics_detected": [881.0, 1321.5, 1762.0]
}
```

**Exemplo com Python:**
```python
import requests
import numpy as np

# Gera dados de áudio simulados
sample_rate = 44100
duration = 0.1
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t).tolist()

response = requests.post(
    "http://localhost:8004/practice/session",
    json={
        "audio_data": audio_data,
        "target_note": "A4",
        "sample_rate": sample_rate,
        "tolerance_cents": 50
    }
)

data = response.json()
print(f"Nota detectada: {data['detected_note']}")
print(f"Acertou: {data['is_correct']}")
print(f"Precisão: {data['accuracy_score']}%")
print(f"Harmônicos: {data['harmonics_detected']}")
```

---

**Última atualização:** 2025-01-XX  
**Versão da API:** 1.0.0

