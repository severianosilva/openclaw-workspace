# Sistema de Auditoria e Segurança - OpenClaw

## 📋 VISÃO GERAL

Sistema completo de auditoria e proteção contra invasões e anomalias no OpenClaw.

---

## 🛡️ COMPONENTES DO SISTEMA

### 1. **sistema_auditoria.py** - Auditoria Periódica
Verificações automáticas de segurança:
- ✅ Credenciais WhatsApp (dispositivos autorizados)
- ✅ Integridade do arquivo de configuração
- ✅ Sessões ativas
- ✅ Processo do gateway

**Execução:** Manual ou via cron

### 2. **protecao_ativa.py** - Proteção em Tempo Real
Monitoramento contínuo:
- 🚨 Detecção de dispositivos não autorizados
- 🚨 Movimentação automática para quarentena
- 🚨 Alertas de modificações suspeitas
- 🚨 Logs de segurança

**Execução:** Contínua (background)

### 3. **auditoria_cron.sh** - Agendador
Executa auditoria automaticamente:
- ⏰ A cada 2 horas
- 📊 Gera relatórios
- 🔔 Envia alertas para canais

---

## 🚀 INSTALAÇÃO

### Passo 1: Executar Instalador
```bash
bash /home/severosa/organizacao/seguranca/instalar_auditoria.sh
```

### Passo 2: Testar Auditoria
```bash
python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py
```

### Passo 3: Iniciar Proteção Ativa (opcional - para monitoramento contínuo)
```bash
# Em um terminal separado
python3 /home/severosa/organizacao/seguranca/protecao_ativa.py
```

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
/home/severosa/organizacao/seguranca/
├── sistema_auditoria.py       # Script de auditoria
├── protecao_ativa.py          # Proteção em tempo real
├── auditoria_cron.sh          # Agendador
├── instalar_auditoria.sh      # Instalador
├── logs/                      # Logs de segurança
│   ├── security_YYYY-MM-DD.log
│   └── proteacao_ativa.log
├── relatorios/                # Relatórios periódicos
├── quarentena/                # Arquivos suspeitos
└── backups/                   # Backups automáticos
```

---

## 🔐 MECANISMOS DE PROTEÇÃO

### 1. Whitelist de Dispositivos
**Apenas dispositivos autorizados:**
- `+5531982436396` (seu número)

**Qualquer outro dispositivo:**
- 🚫 Detectado automaticamente
- 🚫 Movido para quarentena
- 🚫 Alerta enviado imediatamente

### 2. Monitoramento de Integridade
- Hash SHA-256 do arquivo de configuração
- Detecção de modificações não autorizadas
- Logs de alterações

### 3. Verificação de Processos
- Gateway rodando corretamente
- Processos não identificados
- Anomalias de execução

---

## 🔔 ALERTAS

### Níveis de Alerta
- **INFO** - Informações gerais
- **WARNING** - Atenção necessária
- **ERROR** - Erro detectado
- **CRITICAL** - 🚨 AÇÃO IMEDIATA NECESSÁRIA

### Canais de Notificação
- Telegram (automático)
- WhatsApp (quando conectado)
- Logs de arquivo

---

## 🧪 TESTES

### Testar Auditoria Manual
```bash
python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py
```

### Verificar Logs
```bash
# Últimos eventos
tail -20 /home/severosa/organizacao/seguranca/logs/security_$(date +%Y-%m-%d).log

# Monitorar em tempo real
tail -f /home/severosa/organizacao/seguranca/logs/proteacao_ativa.log
```

### Verificar Quarentena
```bash
ls -la /home/severosa/organizacao/seguranca/quarentena/
```

---

## 📊 RELATÓRIOS

Relatórios gerados automaticamente em:
- `/home/severosa/organizacao/seguranca/relatorios/`

Formato: `relatorio_YYYYMMDD_HHMM.json`

---

## 🔧 COMANDOS ÚTEIS

### Verificar Status de Segurança
```bash
# Auditoria rápida
python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py

# Listar dispositivos autorizados
grep -r "whitelist" /home/severosa/organizacao/seguranca/

# Verificar cron jobs
crontab -l
```

### Limpeza de Segurança (Emergência)
```bash
# Limpar credenciais
rm -rf ~/.openclaw/credentials/whatsapp/default/*

# Reiniciar pareamento
openclaw channels login --channel whatsapp --account default
```

---

## 🛡️ BOAS PRÁTICAS

1. **Execute auditoria manualmente** após qualquer mudança
2. **Verifique logs diariamente** nos primeiros dias
3. **Mantenha o Telegram ativo** para receber alertas
4. **Não compartilhe** credenciais do OpenClaw
5. **Revise a quarentena** periodicamente

---

## ✅ CHECKLIST DE SEGURANÇA

- [ ] Auditoria instalada e rodando
- [ ] Cron job configurado (a cada 2 horas)
- [ ] Proteção ativa iniciada (opcional)
- [ ] Logs verificados (sem alertas críticos)
- [ ] Apenas dispositivo autorizado na lista
- [ ] Backup das credenciais criado

---

## 🆘 SUPORTE

Em caso de alertas críticos:
1. Verifique logs imediatamente
2. Revize quarentena
3. Contate pelo Telegram

**Sistema criado em:** 2026-02-25
**Versão:** 1.0.0
