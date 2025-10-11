# #Dô - Assistente de Prática Musical

Backend API para aplicativo de prática musical com detecção de áudio via Machine Learning.

## 📋 Visão Geral

O #Dô é uma plataforma web responsiva focada na prática musical que permite que usuários toquem instrumentos musicais e recebam feedback em tempo real sobre notas e acordes via microfone do dispositivo, utilizando machine learning para processamento de áudio.

## 🏗️ Arquitetura

O sistema é baseado em uma arquitetura de microsserviços, dividindo responsabilidades em módulos independentes e especializados:

### Microsserviços

1. **Auth Service** - Autenticação e gerenciamento de sessões
2. **Profile Service** - Gerenciamento de perfis de usuário
3. **Instruments Service** - Seleção de instrumentos e FAQ
4. **ML Service** - Detecção de áudio e processamento ML
5. **Practice Service** - Sessões de prática e partituras
6. **Subscription Service** - Planos de assinatura e pagamentos

### Tecnologias

- **Backend**: Python 3.10+ com FastAPI
- **ML**: TensorFlow, Librosa, modelo SPICE (Google)
- **Database**: SQLite (local) / PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Authentication**: JWT + bcrypt
- **Payments**: Stripe
- **Cache**: Redis

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Redis server (opcional)
- Stripe account (para pagamentos)
- Supabase account (para produção)

### Configuração

1. Clone o repositório:
```bash
git clone <repository-url>
cd 6_PINT
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

4. Configure o banco de dados:
```bash
# Para SQLite (desenvolvimento)
DATABASE_URL=sqlite:///./dô.db

# Para Supabase (produção)
DATABASE_URL=postgresql://user:password@host:port/database
```

5. Inicialize o banco de dados:
```bash
python backend/scripts/setup.py
```

6. Execute a aplicação:
```bash
python start_server.py
```

## 📚 Documentação da API

### Endpoints Principais

#### Autenticação (`/auth`)
- `POST /auth/register` - Registrar novo usuário
- `POST /auth/login` - Fazer login
- `GET /auth/me` - Obter usuário atual
- `POST /auth/change-password` - Alterar senha
- `POST /auth/forgot-password` - Esqueci senha
- `POST /auth/reset-password` - Resetar senha

#### Perfil (`/profile`)
- `GET /profile/me` - Obter perfil do usuário
- `PUT /profile/me` - Atualizar perfil
- `POST /profile/avatar` - Upload de avatar
- `DELETE /profile/avatar` - Deletar avatar
- `GET /profile/statistics` - Estatísticas do usuário

#### Instrumentos (`/instruments`)
- `GET /instruments/` - Listar todos os instrumentos
- `GET /instruments/{type}` - Obter instrumento por tipo
- `POST /instruments/select` - Selecionar instrumento
- `GET /instruments/{type}/faq` - FAQ do instrumento
- `GET /instruments/faq/search` - Buscar FAQ

#### Machine Learning (`/ml`)
- `POST /ml/detect-note` - Detectar nota do áudio
- `POST /ml/tune` - Afinar instrumento
- `POST /ml/detect-chord` - Detectar acorde
- `POST /ml/analyze-session` - Analisar sessão de prática
- `GET /ml/tuning-notes/{instrument}` - Notas de afinação

#### Prática (`/practice`)
- `POST /practice/sessions` - Iniciar sessão de prática
- `PUT /practice/sessions/{id}` - Atualizar sessão
- `POST /practice/sessions/{id}/end` - Finalizar sessão
- `GET /practice/statistics` - Estatísticas de prática
- `GET /practice/history` - Histórico de prática
- `GET /practice/composers` - Listar compositores
- `GET /practice/scores` - Listar partituras

#### Assinaturas (`/subscription`)
- `GET /subscription/plans` - Listar planos
- `GET /subscription/current` - Assinatura atual
- `POST /subscription/create` - Criar assinatura
- `POST /subscription/confirm` - Confirmar pagamento
- `POST /subscription/cancel` - Cancelar assinatura
- `POST /subscription/trial` - Iniciar trial
- `GET /subscription/about` - Sobre nós

### Modelos de Dados

#### User
```json
{
  "id": "string",
  "email": "string",
  "username": "string",
  "avatar_url": "string",
  "favorite_instrument": "violin|flute|trumpet|piano|cello",
  "subscription_plan": "copper|silver|gold",
  "role": "anonymous|registered|premium|admin",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Practice Session
```json
{
  "id": "string",
  "user_id": "string",
  "instrument_type": "string",
  "start_time": "datetime",
  "end_time": "datetime",
  "duration_minutes": "integer",
  "status": "active|paused|completed|abandoned",
  "notes_played": "integer",
  "correct_notes": "integer",
  "accuracy_percentage": "float"
}
```

#### Note Detection
```json
{
  "note": "string",
  "frequency": "float",
  "confidence": "float",
  "accuracy": "perfect|good|fair|poor",
  "timestamp": "datetime"
}
```

## 🧪 Testes

### Executar Testes

```bash
# Testes unitários
pytest backend/tests/test_auth_service.py
pytest backend/tests/test_ml_service.py

# Testes de integração
pytest backend/tests/test_integration.py

# Todos os testes
pytest backend/tests/
```

### Cobertura de Testes

```bash
pytest --cov=backend backend/tests/
```

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
backend/
├── api/                 # Endpoints da API
├── models/              # Modelos de dados
├── services/            # Lógica de negócio
├── tests/               # Testes
├── main.py              # Aplicação principal
└── requirements.txt     # Dependências
```

### Padrões de Código

- **POO**: Uso de classes e herança
- **Type Hints**: Tipagem estática
- **Async/Await**: Programação assíncrona
- **Error Handling**: Tratamento de exceções
- **Logging**: Sistema de logs

### Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📊 Monitoramento

### Logs
- Logs estruturados em JSON
- Níveis: DEBUG, INFO, WARNING, ERROR
- Rotação automática de logs

### Métricas
- Latência de resposta
- Taxa de erro
- Uso de recursos
- Performance do ML

## 🚀 Deploy

### Produção
- Use um servidor WSGI como Gunicorn
- Configure proxy reverso (Nginx)
- Use HTTPS
- Configure variáveis de ambiente

### Docker (Opcional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "backend.main"]
```

## 📝 Licença

Este projeto é parte de um trabalho acadêmico do curso de Análise e Desenvolvimento de Sistemas.

## 👥 Equipe

- Desenvolvedores Backend
- Desenvolvedores Frontend
- Especialistas em ML
- Testadores

## 📞 Suporte

Para dúvidas ou problemas, entre em contato:
- Email: contato@dô.com
- GitHub Issues: [Link para issues]

---

**Versão**: 1.0.0  
**Última atualização**: Setembro 2025
