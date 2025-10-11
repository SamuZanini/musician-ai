# Guia de Migração para Supabase

Este guia explica como migrar do SQLite local para o Supabase (PostgreSQL).

## 🎯 Por que migrar para Supabase?

- **Escalabilidade**: PostgreSQL é mais robusto para produção
- **Cloud**: Acesso de qualquer lugar
- **Recursos**: Backup automático, monitoramento, etc.
- **Colaboração**: Múltiplos desenvolvedores podem acessar

## 📋 Pré-requisitos

1. Conta no [Supabase](https://supabase.com)
2. Projeto criado no Supabase
3. URL de conexão do banco de dados

## 🚀 Passos da Migração

### 1. Configurar Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Vá em **Settings** > **Database**
4. Copie a **Connection string**

### 2. Atualizar Configuração

Edite seu arquivo `.env`:

```bash
# Antes (SQLite)
DATABASE_URL=sqlite:///./dô.db

# Depois (Supabase)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

### 3. Executar Migração

```bash
# Migrar dados do SQLite para Supabase
python backend/database/migrations.py migrate
```

### 4. Verificar Migração

```bash
# Testar a aplicação
python start_server.py

# Verificar se os dados foram migrados
# Acesse http://localhost:8000/docs
```

## 🔧 Configurações Adicionais do Supabase

### Row Level Security (RLS)

Para segurança, configure RLS no Supabase:

```sql
-- Habilitar RLS para tabela users
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Política para usuários acessarem apenas seus próprios dados
CREATE POLICY "Users can access own data" ON users
    FOR ALL USING (auth.uid()::text = id);
```

### Índices para Performance

```sql
-- Índices para melhor performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_scores_composer_id ON scores(composer_id);
```

## 📊 Monitoramento

### Dashboard do Supabase

1. Acesse o dashboard do seu projeto
2. Vá em **Database** > **Tables**
3. Verifique se todas as tabelas foram criadas
4. Confira os dados migrados

### Logs e Métricas

- **Logs**: Database > Logs
- **Métricas**: Database > Metrics
- **Backups**: Database > Backups

## 🔄 Rollback (Se necessário)

Se algo der errado, você pode voltar ao SQLite:

```bash
# No arquivo .env
DATABASE_URL=sqlite:///./dô.db

# Reiniciar aplicação
python start_server.py
```

## 🚨 Troubleshooting

### Erro de Conexão

```
Error: connection to server at "db.xxx.supabase.co", port 5432 failed
```

**Solução**: Verifique se a URL de conexão está correta e se o projeto está ativo.

### Erro de Permissão

```
Error: permission denied for table users
```

**Solução**: Configure as políticas RLS no Supabase.

### Dados Não Aparecem

**Solução**: Verifique se a migração foi executada com sucesso e se não houve erros.

## 📈 Próximos Passos

Após a migração bem-sucedida:

1. **Teste Completo**: Execute todos os testes
2. **Backup**: Configure backup automático
3. **Monitoramento**: Configure alertas
4. **Performance**: Otimize consultas se necessário

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs do Supabase
2. Consulte a [documentação oficial](https://supabase.com/docs)
3. Abra uma issue no repositório

---

**Nota**: Esta migração é unidirecional. Após migrar para Supabase, recomendamos manter apenas o PostgreSQL para produção.
