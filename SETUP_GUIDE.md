# Guia de Inicialização - Musician AI

## Pré-requisitos

- **PHP 8.0+** com extensões: PDO, MySQL, JSON, OpenSSL
- **Python 3.8+** com pip
- **MySQL 5.7+** ou **MariaDB 10.3+**
- **Composer** (gerenciador de dependências PHP)
- **Node.js 16+** e **npm** (para o frontend)

## Configuração Passo a Passo

### 1. Configurar Banco de Dados

```bash
# Conectar ao MySQL
mysql -u root -p

# Executar script de criação
source backend/database/schema.sql
```

### 2. Configurar Backend PHP

```bash
cd backend/

# Instalar dependências
composer install

# Configurar variáveis de ambiente
cp env.example .env

# Editar arquivo .env com suas configurações
nano .env
```

**Configurações importantes no .env:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=musician_ai
DB_USER=seu_usuario_mysql
DB_PASS=sua_senha_mysql

JWT_SECRET=sua_chave_secreta_jwt_muito_segura
AI_SERVICE_URL=http://localhost:8001
```

### 3. Configurar Serviço de IA Python

```bash
cd ia/

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env

# Editar arquivo .env
nano .env
```

**Configurações importantes no .env:**
```env
AI_SERVICE_PORT=8001
AI_SERVICE_HOST=0.0.0.0
BACKEND_URL=http://localhost:8000
```

### 4. Iniciar os Serviços

#### Terminal 1 - Backend PHP
```bash
cd backend/
composer start
```

#### Terminal 2 - Serviço IA
```bash
cd ia/
./start_ai_service.sh
```

#### Terminal 3 - Frontend (se necessário)
```bash
npm run dev
```

## Verificação dos Serviços

### Testar Backend PHP
```bash
curl http://localhost:8000/api/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "service": "musician-backend"
}
```

### Testar Serviço IA
```bash
curl http://localhost:8001/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "service": "musician-ai"
}
```

## Testando a Integração

### 1. Registrar um usuário
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### 2. Fazer login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### 3. Testar análise de áudio (com token)
```bash
curl -X POST http://localhost:8000/api/ai/analyze-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "audio_file_path": "/path/to/audio.wav",
    "analysis_type": "chord_detection"
  }'
```

## Solução de Problemas

### Erro de Conexão com Banco
- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão: `mysql -u usuario -p -h host`

### Erro de Porta em Uso
- Backend PHP (8000): `lsof -i :8000`
- Serviço IA (8001): `lsof -i :8001`
- Mate o processo ou mude a porta no `.env`

### Erro de Dependências Python
```bash
cd ia/
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Dependências PHP
```bash
cd backend/
composer install --no-dev
composer dump-autoload
```

## Scripts de Automação

### Script Completo de Setup
```bash
#!/bin/bash
echo "Configurando Musician AI..."

# Backend PHP
cd backend/
composer install
cp env.example .env
echo "Configure o arquivo backend/.env com suas credenciais"

# Serviço IA
cd ../ia/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
echo "Configure o arquivo ia/.env com suas configurações"

echo "Setup concluído! Configure os arquivos .env e inicie os serviços."
```

## Monitoramento

### Logs do Backend PHP
- Logs são exibidos no terminal onde o servidor está rodando
- Para produção, configure logging em arquivo

### Logs do Serviço IA
- Logs são exibidos no terminal
- Configure `LOG_FILE` no `.env` para salvar em arquivo

### Health Checks
- Backend: `GET /api/health`
- IA: `GET /health`

## Próximos Passos

1. **Configurar HTTPS** para produção
2. **Implementar rate limiting** nos endpoints
3. **Configurar backup automático** do banco
4. **Implementar monitoramento** com ferramentas como Prometheus
5. **Configurar CI/CD** para deploy automático


