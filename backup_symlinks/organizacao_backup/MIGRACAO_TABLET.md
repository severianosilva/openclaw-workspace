# 📱 Migração OpenClaw: PC → Tablet

## 📋 O QUE MIGRAR

### 1. **OpenClaw Core** (~50-100 MB)
```
~/.openclaw/
├── openclaw.json          ← Configuração principal
├── sessions/              ← Sessões ativas
├── workspace/             ← Workspace atual
├── memory/                ← Memória do agente
└── media/                 ← Mídia (opcional, pode ser grande)
```

### 2. **Sistema Jurídico** (~200-500 MB)
```
~/organizacao/
├── advocacia/             ← Processos jurídicos
├── servidor-publico/      ← Comissão/processos
├── controle-prazos/       ← Scripts de controle
├── captura/               ← Transcrição áudio
├── youtube/               ← Sistema YouTube
├── notebooklm_integration/← Integrações
├── scripts/               ← Todos scripts
└── backup/                ← Backups (opcional)
```

### 3. **Configurações** (~1 MB)
```
~/.config/rclone/          ← Config Dropbox
~/.bashrc                  ← PATH e aliases
~/.local/bin/rclone        ← rclone instalado
```

---

## 🚀 **MÉTODO 1: Dropbox Sync (RECOMENDADO)**

### No PC (Origem):

```bash
# 1. Criar backup compactado
cd ~
tar -czf openclaw_backup_$(date +%Y%m%d).tar.gz \
  .openclaw/ \
  organizacao/ \
  .config/rclone/ \
  .bashrc

# 2. Enviar para Dropbox
~/.local/bin/rclone copy \
  openclaw_backup_*.tar.gz \
  gdrive:OpenClaw_Backup/Migracao_Tablet/

# 3. Verificar upload
~/.local/bin/rclone ls gdrive:OpenClaw_Backup/Migracao_Tablet/
```

### No Tablet (Destino):

```bash
# 1. Instalar Termux
# 2. Instalar dependências
pkg update
pkg install python nodejs git curl wget

# 3. Instalar OpenClaw
curl -fsSL https://openclaw.sh/install.sh | sh

# 4. Instalar rclone no Termux
curl https://rclone.org/install.sh | sudo bash

# 5. Configurar Dropbox no tablet
rclone config
# (mesmo processo do PC)

# 6. Baixar backup
rclone copy gdrive:OpenClaw_Backup/Migracao_Tablet/openclaw_backup_*.tar.gz ~/

# 7. Extrair
tar -xzf openclaw_backup_*.tar.gz

# 8. Restaurar configurações
cp .bashrc ~/.bashrc
source ~/.bashrc

# 9. Iniciar OpenClaw
openclaw start
```

---

## 🚀 **MÉTODO 2: Script Automático (MAIS FÁCIL)**

Criei scripts que fazem tudo automaticamente!

### No PC:
```bash
~/organizacao/scripts/criar_backup_migracao.sh
```

### No Tablet:
```bash
~/organizacao/scripts/restaurar_backup_migracao.sh
```

---

## 🚀 **MÉTODO 3: Sync Contínuo (IDEAL)**

Configurar **sync automático** entre PC e Tablet:

```
PC ←→ Dropbox ←→ Tablet
     (nuvem)
```

**Vantagem:** Mudanças no PC aparecem no tablet automaticamente!

---

## ⚠️ **ATENÇÃO: DIFERENÇAS TABLET**

| Item | PC | Tablet | Ajuste Necessário |
|------|----|--------|-------------------|
| **Caminhos** | `/home/severosa/` | `/data/data/com.termux/files/home/` | Scripts atualizam paths |
| **Sistema** | Ubuntu/WSL | Android/Termux | Alguns comandos diferentes |
| **RAM** | Variável | 16 GB | ✅ Melhor no tablet |
| **Armazenamento** | 1 TB | 1 TB | ✅ Igual |
| **Gateway WhatsApp** | Funciona | Funciona | ✅ Mesmo sistema |
| **Gateway Telegram** | Funciona | Funciona | ✅ Mesmo sistema |

---

## 📊 **TAMANHO ESTIMADO DO BACKUP**

| Componente | Tamanho |
|------------|---------|
| `.openclaw/` (sem media) | ~50 MB |
| `organizacao/` (scripts + projetos) | ~200 MB |
| `organizacao/youtube/` (vídeos) | ~1 GB (opcional) |
| `organizacao/backup/` | ~3 GB (opcional) |
| **Total essencial** | **~250 MB** |
| **Total completo** | **~4-5 GB** |

**Recomendação:** Migrar **essencial** primeiro (~250 MB), depois sync do resto.

---

## 🎯 **PLANO RECOMENDADO**

### **FASE 1: Preparação (PC)** - 10 min
1. Criar backup essencial
2. Enviar para Dropbox
3. Verificar integridade

### **FASE 2: Tablet Setup** - 30 min
1. Instalar Termux
2. Instalar OpenClaw
3. Configurar gateways
4. Baixar backup
5. Restaurar

### **FASE 3: Testes** - 15 min
1. Iniciar OpenClaw no tablet
2. Testar WhatsApp/Telegram
3. Verificar memória/sessões
4. Testar scripts jurídicos
5. Testar sistema YouTube

### **FASE 4: Sync Contínuo** - 15 min
1. Configurar rclone sync automático
2. Testar bidirecional
3. Agendar syncs periódicos

---

## ✅ **PRÓXIMOS PASSOS AGORA**

**Vou criar os scripts de migração automática!**

1. `criar_backup_migracao.sh` (PC)
2. `restaurar_backup_migracao.sh` (Tablet)
3. `configurar_sync_continuo.sh` (Ambos)

**Posso criar agora?**
