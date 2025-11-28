# Integração Frontend com ML Services

Documentação sobre a integração do frontend com os serviços de Machine Learning.

## 📋 Visão Geral

O frontend agora está conectado com os serviços de ML em Python, permitindo:
- Detecção de frequência no navegador (usando Web Audio API)
- Envio de frequências detectadas para validação/refinamento no ML
- Feedback de afinação em tempo real
- Comparação de notas detectadas localmente vs ML

## 🔧 Arquitetura

```
Frontend (Navegador)
├── useMicrophone → Captura áudio do microfone
├── useAudioProcessor → Detecta frequência localmente (FFT)
└── useMLIntegration → Envia dados para ML Services
    ├── ML Service (8001) → /tune, /detect
    ├── Tuner Service (8002) → /tune/{instrument}
    ├── Detection Service (8003) → /detect
    └── Practice Service (8004) → /practice/check, /practice/session
```

## 📁 Arquivos Criados

### `lib/api/mlService.ts`
Cliente TypeScript para comunicação com os serviços de ML:
- `detectAudio()` - Detecta pitch a partir de dados de áudio
- `tuneAudio()` - Obtém feedback de afinação
- `tuneInstrument()` - Afina para instrumento específico
- `detectAudioAdvanced()` - Detecção avançada com Detection Service

### `hooks/useMLIntegration.ts`
Hook React para integrar ML com componentes:
- Gerencia estado de processamento
- Envia frequências para ML
- Trata erros e callbacks
- Suporta detecção avançada e afinação por instrumento

## 🎯 Páginas Integradas

### 1. Página `tuning` (`app/(public)/tuning/page.tsx`)

**Funcionalidades:**
- Detecta frequência localmente usando FFT
- Envia frequência para ML Service (`/tune`) quando muda significativamente (>1 Hz)
- Exibe feedback de afinação do ML:
  - Diferença em cents
  - Direção de afinação (Afinado, Muito alto, Muito baixo)
  - Status de afinação
- Indicador visual do status do ML Service

**Fluxo:**
1. Usuário clica no Ripple → Ativa microfone
2. `useAudioProcessor` detecta frequência localmente
3. Se frequência mudou >1 Hz → Envia para ML
4. ML retorna feedback de afinação
5. UI atualiza com dados do ML

### 2. Página `practice-session` (`app/(public)/practice-session/page.tsx`)

**Funcionalidades:**
- Detecta frequência localmente
- Compara nota detectada com nota alvo
- Envia frequência para ML quando muda (>2 Hz)
- Exibe nota detectada localmente e pelo ML
- Usa feedback do ML para validar acerto/erro

**Fluxo:**
1. Usuário clica "Iniciar" → Ativa microfone
2. Sistema exibe nota alvo
3. `useAudioProcessor` detecta frequência
4. Compara localmente (feedback imediato)
5. Envia para ML (validação adicional)
6. Exibe feedback visual (Ripple verde/vermelho)

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do projeto:

```env
NEXT_PUBLIC_ML_SERVICE_URL=http://localhost:8001
NEXT_PUBLIC_TUNER_SERVICE_URL=http://localhost:8002
NEXT_PUBLIC_DETECTION_SERVICE_URL=http://localhost:8003
NEXT_PUBLIC_PRACTICE_SERVICE_URL=http://localhost:8004
```

### Iniciar Serviços ML

Certifique-se de que os serviços ML estão rodando:

```bash
cd ia
python run_services.py start
```

Ou individualmente:
```bash
python ml_service.py      # Porta 8001
python tuner_service.py   # Porta 8002
python detection_service.py # Porta 8003
```

## 🔄 Fluxo de Dados

### Detecção de Frequência

1. **Frontend (Local):**
   ```
   Microfone → AudioContext → AnalyserNode → FFT → Frequência detectada
   ```

2. **Envio para ML:**
   ```
   Frequência → POST /tune → ML Service → Feedback de afinação
   ```

3. **Processamento:**
   - Frequência detectada localmente: ~0.1 Hz de precisão
   - ML valida e refina: feedback de afinação, cents, direção

### Comparação Local vs ML

- **Detecção Local:** Rápida, funciona offline, boa precisão
- **ML Service:** Validação adicional, feedback de afinação, suporte a instrumentos

## 🎨 Interface do Usuário

### Indicadores Visuais

- **Status ML Service:**
  - 🟢 Verde: ML ativo e funcionando
  - 🟡 Amarelo: ML processando
  - ⚫ Cinza: ML desativado

- **Feedback de Afinação:**
  - 🟢 Verde: Afinado
  - 🔴 Vermelho: Muito alto
  - 🔵 Azul: Muito baixo

### Dados Exibidos

**Página Tuning:**
- Nota detectada
- Frequência atual
- Frequência alvo
- Diferença em cents
- Direção de afinação
- Precisão/Confiança
- Status do ML Service

**Página Practice:**
- Nota alvo
- Nota detectada (local)
- Nota detectada (ML)
- Score de precisão (0-100%)
- Mensagem de feedback do ML
- Status de acerto/erro
- Contador regressivo
- Status do ML Service

## 🐛 Tratamento de Erros

O sistema trata erros graciosamente:

1. **ML Service indisponível:**
   - Continua usando detecção local
   - Exibe aviso amarelo
   - Não bloqueia funcionalidade

2. **Erro de rede:**
   - Retry automático na próxima detecção
   - Log de erros no console
   - Fallback para detecção local

3. **Permissão de microfone negada:**
   - Exibe mensagem de erro
   - Permite tentar novamente

## 🚀 Melhorias Futuras

1. **WebSocket para tempo real:**
   - Conectar com Detection Service WebSocket (`ws://localhost:8003/ws`)
   - Stream contínuo de áudio
   - Menor latência

2. **Envio de dados de áudio brutos:**
   - Enviar buffer de áudio completo para ML
   - Detecção mais precisa
   - Análise de harmônicos

3. **Cache de resultados:**
   - Evitar chamadas repetidas para mesma frequência
   - Melhorar performance

4. **Suporte a instrumentos:**
   - Seleção de instrumento na UI
   - Afinação específica por instrumento
   - Guias de afinação

## 📝 Notas Técnicas

### Performance

- **Throttling:** Frequências são enviadas apenas quando mudam significativamente
- **Debouncing:** Evita múltiplas chamadas simultâneas
- **Async:** Processamento não bloqueia UI

### Precisão

- **Detecção Local:** ~0.1 Hz (FFT com interpolação parabólica)
- **ML Service:** Validação e feedback adicional
- **Combinação:** Melhor dos dois mundos

### Compatibilidade

- Requer navegadores modernos com Web Audio API
- HTTPS necessário para acesso ao microfone (exceto localhost)
- CORS configurado nos serviços ML

## 🔍 Debugging

### Verificar Conexão

```javascript
// No console do navegador
import { checkMLServiceHealth } from '@/lib/api/mlService';
checkMLServiceHealth().then(console.log);
```

### Logs

Os erros são logados no console do navegador:
- `Erro ao detectar áudio: ...`
- `Erro ao afinar com ML: ...`
- `Erro no ML: ...`

### Testar Endpoints

```bash
# Testar ML Service
curl http://localhost:8001/health

# Testar Tuner Service
curl http://localhost:8002/health

# Testar Detection Service
curl http://localhost:8003/health
```

---

**Última atualização:** 2025-01-XX  
**Versão:** 1.0.0

