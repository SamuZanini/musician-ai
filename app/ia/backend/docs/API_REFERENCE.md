# API Reference - #Dô Backend

## Base URL
```
http://localhost:8000
```

## Autenticação

A API usa JWT (JSON Web Tokens) para autenticação. Inclua o token no header:
```
Authorization: Bearer <token>
```

## Endpoints

### 🔐 Autenticação (`/auth`)

#### POST /auth/register
Registrar novo usuário.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "avatar_url": "https://example.com/avatar.jpg",
  "favorite_instrument": "violin",
  "subscription_plan": "copper",
  "role": "registered"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "username": "username",
    "created_at": "2025-09-25T10:00:00Z"
  }
}
```

#### POST /auth/login
Fazer login.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "remember_me": false
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "username": "username"
  }
}
```

#### GET /auth/me
Obter informações do usuário atual.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "username": "username",
  "avatar_url": "https://example.com/avatar.jpg",
  "favorite_instrument": "violin",
  "subscription_plan": "copper",
  "role": "registered",
  "created_at": "2025-09-25T10:00:00Z"
}
```

### 👤 Perfil (`/profile`)

#### GET /profile/me
Obter perfil do usuário com estatísticas.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "user_123",
  "username": "username",
  "email": "user@example.com",
  "avatar_url": "https://example.com/avatar.jpg",
  "favorite_instrument": "violin",
  "subscription_plan": "copper",
  "created_at": "2025-09-25T10:00:00Z",
  "practice_streak": 5,
  "total_practice_time": 120
}
```

#### PUT /profile/me
Atualizar perfil do usuário.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "username": "new_username",
  "email": "new@example.com",
  "favorite_instrument": "piano"
}
```

#### POST /profile/avatar
Upload de avatar.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "avatar_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "avatar_url": "https://storage.googleapis.com/bucket/avatars/user_123.jpg"
}
```

### 🎵 Instrumentos (`/instruments`)

#### GET /instruments/
Listar todos os instrumentos disponíveis.

**Response:**
```json
[
  {
    "id": "violin_001",
    "name": "Violino",
    "type": "violin",
    "description": "Instrumento de cordas friccionadas",
    "image_url": "/images/instruments/violin.jpg",
    "tuning_notes": ["G3", "D4", "A4", "E5"],
    "difficulty_level": 3,
    "is_premium": false
  }
]
```

#### GET /instruments/{type}
Obter instrumento por tipo.

**Path Parameters:**
- `type`: Tipo do instrumento (violin, flute, trumpet, piano, cello)

#### POST /instruments/select
Selecionar instrumento para o usuário.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "instrument_type": "violin"
}
```

#### GET /instruments/{type}/faq
Obter FAQ do instrumento.

**Response:**
```json
{
  "instrument_type": "violin",
  "faq_items": [
    {
      "id": "violin_faq_001",
      "question": "Como afinar o violino?",
      "answer": "Use um afinador eletrônico...",
      "category": "tuning"
    }
  ]
}
```

### 🤖 Machine Learning (`/ml`)

#### POST /ml/detect-note
Detectar nota do áudio.

**Request Body:**
```
Content-Type: application/octet-stream
<audio_data_binary>
```

**Response:**
```json
{
  "note": "A4",
  "frequency": 440.0,
  "confidence": 0.95,
  "accuracy": "perfect",
  "timestamp": "2025-09-25T10:00:00Z"
}
```

#### POST /ml/tune
Afinar instrumento.

**Request Body:**
```
Content-Type: application/octet-stream
<audio_data_binary>
```

**Query Parameters:**
- `target_note`: Nota alvo (ex: "A4")

**Response:**
```json
{
  "target_note": "A4",
  "detected_note": "A4",
  "frequency": 440.0,
  "cents_offset": 2.5,
  "is_in_tune": true,
  "confidence": 0.95
}
```

#### POST /ml/detect-chord
Detectar acorde do áudio.

**Request Body:**
```
Content-Type: application/octet-stream
<audio_data_binary>
```

**Response:**
```json
{
  "chord": "C Major",
  "confidence": 0.85,
  "notes": ["C", "E", "G"]
}
```

#### GET /ml/tuning-notes/{instrument}
Obter notas de afinação do instrumento.

**Path Parameters:**
- `instrument`: Tipo do instrumento

**Response:**
```json
{
  "instrument_type": "violin",
  "tuning_notes": ["G3", "D4", "A4", "E5"]
}
```

### 🎼 Prática (`/practice`)

#### POST /practice/sessions
Iniciar nova sessão de prática.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "instrument_type": "violin"
}
```

**Response:**
```json
{
  "id": "session_123",
  "user_id": "user_123",
  "instrument_type": "violin",
  "start_time": "2025-09-25T10:00:00Z",
  "status": "active"
}
```

#### PUT /practice/sessions/{session_id}
Atualizar sessão de prática.

**Request Body:**
```
Content-Type: application/octet-stream
<audio_data_binary>
```

**Query Parameters:**
- `target_notes`: Lista de notas alvo (ex: ["A4", "B4"])

#### GET /practice/composers
Listar compositores.

**Response:**
```json
[
  {
    "id": "chopin_001",
    "name": "Frédéric Chopin",
    "period": "Romantic",
    "nationality": "Polish",
    "bio": "Polish composer and virtuoso pianist...",
    "image_url": "/images/composers/chopin.jpg",
    "is_premium": false
  }
]
```

#### GET /practice/scores
Listar partituras.

**Query Parameters:**
- `composer_id`: Filtrar por compositor
- `instrument_type`: Filtrar por instrumento

**Response:**
```json
[
  {
    "id": "chopin_nocturne_001",
    "title": "Nocturne in E-flat major, Op. 9, No. 2",
    "composer_id": "chopin_001",
    "composer_name": "Frédéric Chopin",
    "instrument_type": "piano",
    "difficulty_level": 4,
    "file_url": "/scores/chopin_nocturne_op9_no2.pdf",
    "is_premium": true,
    "duration_minutes": 4
  }
]
```

### 💳 Assinaturas (`/subscription`)

#### GET /subscription/plans
Listar planos de assinatura.

**Response:**
```json
[
  {
    "id": "copper_plan",
    "name": "Copper Plan",
    "plan_type": "copper",
    "price_monthly": 5.00,
    "price_yearly": 50.00,
    "features": {
      "max_practice_sessions": 10,
      "max_scores_per_day": 3,
      "advanced_ml_features": false,
      "premium_scores": false,
      "priority_support": false,
      "offline_mode": false
    },
    "description": "Perfect for beginners",
    "is_popular": false
  }
]
```

#### POST /subscription/create
Criar nova assinatura.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "plan_type": "silver",
  "is_yearly": false
}
```

**Response:**
```json
{
  "payment_intent_id": "pi_1234567890",
  "client_secret": "pi_1234567890_secret_abc123",
  "amount": 15.00,
  "currency": "USD",
  "plan": "silver"
}
```

#### GET /subscription/current
Obter assinatura atual do usuário.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "sub_123",
  "user_id": "user_123",
  "plan": "silver",
  "status": "active",
  "start_date": "2025-09-25T10:00:00Z",
  "end_date": "2025-10-25T10:00:00Z",
  "auto_renew": true
}
```

#### GET /subscription/about
Obter informações sobre o aplicativo.

**Response:**
```json
{
  "title": "Sobre o #Dô",
  "description": "O #Dô é uma plataforma inovadora...",
  "mission": "Democratizar o acesso à educação musical...",
  "team": [
    {
      "name": "Equipe de Desenvolvimento",
      "role": "Desenvolvedores",
      "description": "Estudantes de ADS"
    }
  ],
  "image_url": "/images/about/orchestra.jpg",
  "contact_email": "contato@dô.com"
}
```

## Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Requisição inválida
- `401` - Não autorizado
- `403` - Proibido
- `404` - Não encontrado
- `422` - Erro de validação
- `500` - Erro interno do servidor

## Tratamento de Erros

Todas as respostas de erro seguem o formato:

```json
{
  "detail": "Mensagem de erro",
  "status_code": 400
}
```

## Rate Limiting

- **Gratuito**: 100 requests/hora
- **Premium**: 1000 requests/hora
- **Admin**: Sem limite

## Webhooks

### Stripe Events
- `payment_intent.succeeded` - Pagamento confirmado
- `customer.subscription.updated` - Assinatura atualizada
- `customer.subscription.deleted` - Assinatura cancelada

## SDKs

### Python
```python
import requests

# Configurar cliente
client = requests.Session()
client.headers.update({
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
})

# Exemplo de uso
response = client.get('http://localhost:8000/profile/me')
profile = response.json()
```

### JavaScript
```javascript
// Configurar cliente
const client = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

// Exemplo de uso
const response = await client.get('/profile/me');
const profile = response.data;
```

## Changelog

### v1.0.0 (2025-09-25)
- Versão inicial
- Implementação de todos os microsserviços
- Integração com Firebase
- Sistema de ML com SPICE
- Testes unitários e de integração
