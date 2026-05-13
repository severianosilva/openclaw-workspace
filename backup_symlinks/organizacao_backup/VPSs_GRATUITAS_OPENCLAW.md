# VPSs GRATUITAS para Hospedar OpenClaw

## 🎯 Requisitos Mínimos para OpenClaw
- RAM: 1-2 GB (2GB recomendado)
- CPU: 1 vCPU (compartilhado ok)
- Espaço: 5-10 GB SSD
- Banda: 100-500 GB/mês
- Sistema: Ubuntu 20.04/22.04 LTS

---

## ✅ OPÇÕES 100% GRATUITAS

### 1. ORACLE CLOUD FREE TIER ⭐ MELHOR OPÇÃO
**URL:** https://www.oracle.com/cloud/free/
- **Preço:** GRÁTIS para sempre (não expira!)
- **Configuração:** 2 vCPUs, 1GB RAM, 50GB SSD
- **Recursos:** Até 2 instâncias ARM + 2 DBs
- **Duração:** Permanente (não cancela)
- **Cartão:** Sim (validação, não cobra)
- **Vantagens:** 
  - Maior capacidade gratuita do mercado
  - Não expira após 12 meses
  - Dá para rodar OpenClaw confortavelmente
- **Contras:** 
  - Requer cartão de crédito internacional
  - Processo de cadastro mais burocrático
- **Setup:** ~30 minutos
- **Veredito:** **OPÇÃO #1 RECOMENDADA**

### 2. AWS FREE TIER
**URL:** https://aws.amazon.com/free/
- **Preço:** GRÁTIS (750h/mês por 12 meses)
- **Configuração:** t2.micro - 1 vCPU, 1GB RAM
- **Duração:** 12 meses
- **Cartão:** Sim (validação)
- **Vantagens:**
  - EC2 estável e confiável
  - Muitos tutoriais disponíveis
- **Contras:**
  - Expira em 12 meses
  - Precisa migrar depois
  - 1GB RAM é justo (mas funciona)
- **Setup:** ~20 minutos
- **Veredito:** Ótima, mas temporária

### 3. GOOGLE CLOUD FREE TIER
**URL:** https://cloud.google.com/free
- **Preço:** GRÁTIS ($300 créditos iniciais + always free)
- **Configuração:** e2-micro - 0.25 vCPU, 0.6GB RAM (always free)
- **Duração:** $300 expira em 90 dias; always free contínua
- **Cartão:** Sim
- **Vantagens:**
  - $300 para testar serviços pagos
  - Opção always free permanente
- **Contras:**
  - e2-micro é muito limitado (0.6GB RAM)
  - OpenClaw pode travar
- **Veredito:** Risco de ser muito lento

### 4. IBM CLOUD FREE TIER
**URL:** https://cloud.ibm.com/catalog
- **Preço:** GRÁTIS ( Lite tier )
- **Configuração:** 256 MB - 1GB RAM (limitado)
- **Duração:** Permanente para serviços lite
- **Cartão:** Não (opção sem cartão!)
- **Vantagens:**
  - Não precisa de cartão
  - Opções sem cartão são limitadas
- **Contras:**
  - Muito limitado para OpenClaw
  - Performance insuficiente
- **Veredito:** Não recomendado

### 5. ALIBABA CLOUD FREE TIER
**URL:** https://www.alibabacloud.com/free
- **Preço:** GRÁTIS ($450-850 créditos em produtos)
- **Duração:** 12 meses
- **Cartão:** Sim
- **Vantagens:**
  - Créditos generosos
- **Contras:**
  - Interface em chinês/inglês confusa
  - Suporte limitado
- **Veredito:** Complicado

### 6. AZURE FREE TIER (Microsoft)
**URL:** https://azure.microsoft.com/free
- **Preço:** GRÁTIS ($200 créditos + 12 meses serviços)
- **Duração:** 12 meses
- **Cartão:** Sim
- **Configuração:** B1s - 1 vCPU, 1GB RAM
- **Vantagens:**
  - Integração com Windows/Microsoft
  - Bons serviços de IA
- **Contras:**
  - Expira em 12 meses
  - 1GB RAM é limitado
- **Veredito:** Boa opção alternativa

### 7. RENDER.COM FREE TIER
**URL:** https://render.com/
- **Preço:** GRÁTIS (Web Services, 750h/mês)
- **Configuração:** 512MB RAM, compartilhado
- **Duração:** Permanente
- **Cartão:** Não
- **Vantagens:**
  - Simples de configurar
  - Não precisa de cartão
  - Container persistente
- **Contras:**
  - Apenas 512MB RAM (pode travar)
  - Sono após 15 min inativo (cold start)
- **Veredito:** **OPÇÃO SEM CARTÃO #1**

### 8. RAILWAY.COM FREE TIER
**URL:** https://railway.app/
- **Preço:** GRÁTIS ($5/mês em créditos)
- **Configuração:** Variável
- **Duração:** Enquanto tiver créditos
- **Cartão:** Não
- **Vantagens:**
  - Deploy ultrarrápido
  - Interface moderna
- **Contras:**
  - $5/mês não dura muito
  - Expira rapidamente
- **Veredito:** Para testes rápidos

### 9. FLY.IO FREE TIER
**URL:** https://fly.io/
- **Preço:** GRÁTIS ($5/mês em créditos)
- **Duração:** Enquanto tiver créditos
- **Cartão:** Sim
- **Vantagens:**
  - Edge deployment global
  - Containers leves
- **Contras:**
  - Créditos acabam rápido
  - Complexo para iniciantes
- **Veredito:** Técnico demais

### 10. HEROKU FREE (ACABOU)
**Nota:** Heroku eliminou o tier gratuito em 2022.
Alternativa: **Heroku Eco** ($5/dyno/mês) - não é gratuito

---

## 🏆 RANKING FINAL

| Posição | VPS | Pontuação | Cartão? | RAM | Notas |
|---------|-----|-----------|---------|-----|-------|
| 🥇 1º | Oracle Cloud | ⭐⭐⭐⭐⭐ | Sim | 1GB | Melhor gratuito, não expira |
| 🥈 2º | AWS Free Tier | ⭐⭐⭐⭐ | Sim | 1GB | Estável, mas expira em 12m |
| 🥉 3º | Render Free | ⭐⭐⭐⭐ | Não | 512MB | Melhor sem cartão |
| 4º | Azure Free | ⭐⭐⭐ | Sim | 1GB | Boa alternativa Microsoft |
| 5º | Railway | ⭐⭐⭐ | Não | Variável | Para testes rápidos |
| 6º | Google Cloud | ⭐⭐ | Sim | 0.6GB | Pouca RAM, arriscado |
| 7º | Fly.io | ⭐⭐ | Sim | Variável | Técnico, créditos rápidos |

---

## 🎯 RECOMENDAÇÃO FINAL

### SE TEM CARTÃO DE CRÉDITO:
**Oracle Cloud** - Única opção realmente gratuita e permanente
- Setup: 30 minutos
- Manutenção: zero
- Performance: boa para OpenClaw

### SE NÃO TEM CARTÃO:
**Render.com** + **manter local no WSL**
- Render para testes/deploys rápidos
- WSL permanece como principal
- Híbrido é o melhor caminho

### ALTERNATIVA SEM CARTÃO (RISCO):
Rodar OpenClaw em **GitHub Codespaces**
- Grátis 60-120h/mês
- Ambiente temporário
- Requer reconexão frequente

---

## 🛠️ QUICK START - ORACLE CLOUD (RECOMENDADO)

### Passo 1: Criar Conta
```
1. Acesse: https://www.oracle.com/cloud/free/
2. Clique "Start for free"
3. Preencha cadastro com cartão (não cobra)
4. Aguarde verificação (24-48h)
```

### Passo 2: Criar Instância
```
1. Console > Menu > Compute > Instances
2. Click "Create instance"
3. Nome: openclaw-server
4. Imagem: Ubuntu 22.04 LTS
5. Shape: VM.Standard.A1.Flex (ARM) - sempre gratuito
6. Configuração: 1 OCPU, 1GB RAM
7. Boot volume: 50GB
8. SSH keys: gerar nova
9. Click "Create"
```

### Passo 3: Configurar Firewall
```
1. Menu > Networking > Virtual Cloud Networks
2. Selecione sua VCN
3. Security Lists > Default
4. Add Ingress Rule:
   - Source: 0.0.0.0/0
   - Port: 22 (SSH)
   - Port: 3000-3100 (OpenClaw)
   - Port: 80, 443 (HTTP/HTTPS)
```

### Passo 4: Instalar OpenClaw
```bash
# Conectar via SSH
ssh -i ~/.ssh/id_rsa ubuntu@IP_DA_INSTANCIA

# Instalar dependências
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git nodejs npm docker.io

# Instalar OpenClaw
curl -fsSL https://openclaw.sh/install.sh | sh

# Configurar
openclaw configure

# Iniciar
openclaw start
```

---

## 💰 COMPARAÇÃO: LOCAL vs VPS ORACLE

| Aspecto | WSL Local | Oracle VPS |
|---------|-----------|------------|
| Custo | R$ 0 | R$ 0 forever |
| Performance | Depende do PC | 1GB dedicado |
| Disponibilidade | 24/7 ligado | 24/7 na nuvem |
| Energia | Consome luz | Zero |
| Manutenção | Você cuida | Oracle cuida |
| WhatsApp/Telegram | Local | Remoto |
| Backup | Seu problema | Automático |
| Migração futura | Complexo | Já está na nuvem |

---

## ⚡ DECISÃO RÁPIDA

**Pergunta:** Quer migrar OpenClaw para VPS agora?

**Se SIM:**
1. Criar conta Oracle Cloud (30 min)
2. Configurar instância (20 min)
3. Instalar OpenClaw (15 min)
4. Migrar configurações (30 min)
**Total: ~2 horas**

**Se NÃO (manter local):**
- Otimizar espaço local (transferir arquivos para nuvem)
- Usar VPS apenas para processamento pesado (vídeos)
- Híbrido é mais eficiente

**Qual você prefere?**
