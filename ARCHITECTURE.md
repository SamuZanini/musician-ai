# Arquitetura Musician AI

## Visão Geral

O projeto Musician AI foi separado em duas partes distintas para melhor organização e escalabilidade:

1. **Serviço de IA (Python)** - `ia/` - Processamento de IA e análise musical
2. **Backend Principal (PHP)** - `backend/` - Gerenciamento de dados, autenticação e APIs

## Estrutura do Projeto

```
musician-ai/
├── ia/                          # Serviço de IA em Python
│   ├── main.py                  # Servidor FastAPI principal
│   ├── ml_services.py           # Classes de serviços de ML
│   ├── requirements.txt         # Dependências Python
│   ├── env.example              # Configurações de ambiente
│   └── start_ai_service.sh      # Script de inicialização
│
├── backend/                     # Backend principal em PHP
│   ├── public/
│   │   └── index.php            # Ponto de entrada da aplicação
│   ├── src/
│   │   ├── Config/
│   │   │   └── Database.php     # Configuração do banco
│   │   ├── Controllers/         # Controladores da API
│   │   ├── Models/              # Modelos de dados
│   │   ├── Services/            # Serviços de negócio
│   │   └── Middleware/          # Middlewares
│   ├── database/
│   │   └── schema.sql           # Script de criação do banco
│   ├── composer.json            # Dependências PHP
│   ├── env.example              # Configurações de ambiente
│   └── setup.sh                 # Script de configuração
│
└── app/                         # Frontend Next.js (existente)
```

## Serviço de IA (Python)

### Responsabilidades
- Análise de áudio (detecção de acordes, tempo, tonalidade)
- Geração de música usando IA
- Análise de prática musical
- Processamento de arquivos de áudio

### Tecnologias
- **FastAPI** - Framework web moderno e rápido
- **Librosa** - Análise de áudio
- **NumPy/SciPy** - Computação científica
- **TensorFlow** - Machine Learning (para geração musical)

### Endpoints Disponíveis
- `POST /analyze-audio` - Analisa arquivo de áudio
- `POST /generate-music` - Gera música baseada em prompt
- `POST /analyze-practice` - Analisa performance do usuário
- `GET /health` - Status do serviço

### Configuração
```bash
cd ia/
./start_ai_service.sh
```

O serviço roda na porta **8001** por padrão.

## Backend Principal (PHP)

### Responsabilidades
- Autenticação e autorização de usuários
- Gerenciamento de dados (usuários, instrumentos, sessões de prática)
- Comunicação com o serviço de IA
- APIs REST para o frontend
- Gerenciamento de assinaturas

### Tecnologias
- **Slim Framework** - Micro-framework PHP
- **PDO** - Conexão com banco de dados
- **Firebase JWT** - Autenticação JWT
- **Guzzle HTTP** - Cliente HTTP para comunicação com IA
- **MySQL** - Banco de dados

### Endpoints Disponíveis

#### Autenticação (Público)
- `POST /api/auth/register` - Registro de usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Renovar token

#### Usuários (Protegido)
- `GET /api/user/profile` - Obter perfil
- `PUT /api/user/profile` - Atualizar perfil
- `DELETE /api/user/account` - Deletar conta

#### Instrumentos (Protegido)
- `GET /api/instruments` - Listar instrumentos
- `GET /api/instruments/{id}` - Obter instrumento
- `POST /api/instruments` - Criar instrumento
- `PUT /api/instruments/{id}` - Atualizar instrumento
- `DELETE /api/instruments/{id}` - Deletar instrumento

#### Prática (Protegido)
- `GET /api/practice/sessions` - Listar sessões
- `POST /api/practice/sessions` - Criar sessão
- `GET /api/practice/sessions/{id}` - Obter sessão
- `PUT /api/practice/sessions/{id}` - Atualizar sessão
- `DELETE /api/practice/sessions/{id}` - Deletar sessão

#### Assinaturas (Protegido)
- `GET /api/subscriptions` - Listar assinaturas
- `POST /api/subscriptions` - Criar assinatura
- `PUT /api/subscriptions/{id}` - Atualizar assinatura
- `DELETE /api/subscriptions/{id}` - Cancelar assinatura

#### IA (Protegido - Proxy para serviço Python)
- `POST /api/ai/analyze-audio` - Analisar áudio
- `POST /api/ai/generate-music` - Gerar música
- `POST /api/ai/analyze-practice` - Analisar prática

### Configuração
```bash
cd backend/
./setup.sh
composer start
```

O backend roda na porta **8000** por padrão.

## Comunicação Entre Serviços

O backend PHP atua como um proxy para o serviço de IA, fazendo requisições HTTP internas:

```
Frontend → Backend PHP → Serviço IA Python
```

### Fluxo de Comunicação
1. Frontend faz requisição para backend PHP
2. Backend valida autenticação/autorização
3. Backend faz requisição para serviço IA
4. Serviço IA processa e retorna resultado
5. Backend retorna resposta para frontend

## Banco de Dados

### Tabelas Principais
- `users` - Dados dos usuários
- `instruments` - Instrumentos disponíveis
- `practice_sessions` - Sessões de prática dos usuários
- `subscriptions` - Assinaturas dos usuários

### Configuração
```sql
-- Executar o script de criação
mysql -u root -p < backend/database/schema.sql
```

## Variáveis de Ambiente

### Serviço IA (.env)
```env
AI_SERVICE_PORT=8001
AI_SERVICE_HOST=0.0.0.0
BACKEND_URL=http://localhost:8000
```

### Backend PHP (.env)
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=musician_ai
DB_USER=root
DB_PASS=

JWT_SECRET=your-secret-key
AI_SERVICE_URL=http://localhost:8001
```

## Inicialização dos Serviços

### 1. Configurar Banco de Dados
```bash
mysql -u root -p < backend/database/schema.sql
```

### 2. Iniciar Backend PHP
```bash
cd backend/
composer install
cp env.example .env
# Editar .env com suas configurações
composer start
```

### 3. Iniciar Serviço IA
```bash
cd ia/
./start_ai_service.sh
```

### 4. Iniciar Frontend (Next.js)
```bash
npm run dev
```

## Vantagens da Nova Arquitetura

1. **Separação de Responsabilidades** - IA e backend separados
2. **Escalabilidade** - Serviços podem ser escalados independentemente
3. **Manutenibilidade** - Código mais organizado e focado
4. **Flexibilidade** - Tecnologias específicas para cada domínio
5. **Testabilidade** - Serviços podem ser testados isoladamente

## Monitoramento

- Backend PHP: `GET /api/health`
- Serviço IA: `GET /health`

Ambos retornam status de saúde dos serviços.