# Configuração de Modelos Gratuitos - NVIDIA NIM

**Data:** 2026-02-22
**Baseado no vídeo:** "Run OpenClaw for FREE – Stop Paying API Tokens!"
**Status:** ✅ Concluído

---

## 🎯 RESUMO

Configuração atualizada para usar **modelos 100% gratuitos** via NVIDIA NIM como provedor primário, com fallback em cascata para múltiplos modelos gratuitos.

---

## 📋 CONFIGURAÇÃO APLICADA

### **Modelo Primário:**
```
nvidia-nim/moonshotai/kimi-k2.5
Alias: kimi
```

### **Fallbacks (em ordem):**
1. `nvidia-nim/minimax/minimax-m2.1` (MiniMax M2.1 - NVIDIA)
2. `nvidia-nim/zai-org/glm-4.7` (GLM 4.7 - NVIDIA)
3. `nvidia-nim/deepseek-ai/deepseek-v3.2` (DeepSeek V3.2 - NVIDIA)
4. `synthetic/hf:moonshotai/Kimi-K2-Thinking` (Kimi K2.5 Thinking)
5. `synthetic/hf:deepseek-ai/DeepSeek-V3` (DeepSeek V3)
6. `synthetic/hf:zai-org/GLM-4.7` (GLM 4.7)
7. `minimax-portal/MiniMax-M2.1` (MiniMax M2.1 - Portal)
8. `qwen-portal/coder-model` (Qwen Coder)

---

## 🔑 PROVEDOR NVIDIA NIM

**Base URL:** `https://integrate.api.nvidia.com/v1`

**API Key:** `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`

**Modelos Configurados:**

| Modelo | Contexto | Max Tokens | Custo |
|--------|----------|------------|-------|
| Kimi K2.5 | 200K | 8192 | Grátis |
| MiniMax M2.1 | 256K | 8192 | Grátis |
| GLM 4.7 | 198K | 8192 | Grátis |
| DeepSeek V3.2 | 128K | 8192 | Grátis |

---

## 📂 ARQUIVOS MODIFICADOS

- `/home/severosa/.openclaw/openclaw.json`

---

## 🧪 COMO TESTAR

1. **Abra o chat do OpenClaw**
2. **Envie:** `hi`
3. **Pergunte:** `which LLM are you?`
4. **Resposta esperada:** "Kimi" ou "Kimi K2.5"

---

## 💰 CUSTOS

**Todos os modelos são GRATUITOS!**

- ✅ NVIDIA NIM: Free tier
- ✅ Synthetic/HuggingFace: 100% grátis
- ✅ Portal (Qwen/MiniMax): OAuth grátis

**Risco de custos:** 🟢 Mínimo/Nulo

---

## 🔄 COMANDOS ÚTEIS

**Verificar status do gateway:**
```bash
openclaw gateway status
```

**Reiniciar gateway:**
```bash
openclaw gateway restart
```

**Ver configuração atual:**
```bash
openclaw config get
```

**Testar modelo:**
```bash
openclaw chat "which model are you?"
```

---

## ⚠️ IMPORTANTE

**API Key da NVIDIA está salva em:**
`/home/severosa/.openclaw/openclaw.json`

**NÃO compartilhe este arquivo!**

---

## 📊 COMPARAÇÃO

### ANTES:
```json
{
  "primary": "qwen-portal/coder-model",
  "fallbacks": [
    "qwen-portal/vision-model",
    "openrouter/auto",
    "minimax-portal/MiniMax-M2.1",
    "google/gemini-3-pro-preview"
  ]
}
```

### DEPOIS:
```json
{
  "primary": "nvidia-nim/moonshotai/kimi-k2.5",
  "fallbacks": [
    "nvidia-nim/minimax/minimax-m2.1",
    "nvidia-nim/zai-org/glm-4.7",
    "nvidia-nim/deepseek-ai/deepseek-v3.2",
    "synthetic/hf:moonshotai/Kimi-K2-Thinking",
    "synthetic/hf:deepseek-ai/DeepSeek-V3",
    "synthetic/hf:zai-org/GLM-4.7",
    "minimax-portal/MiniMax-M2.1",
    "qwen-portal/coder-model"
  ]
}
```

---

## 🎯 BENEFÍCIOS

1. ✅ **Zero custos** com API (todos modelos gratuitos)
2. ✅ **Alta performance** (Kimi K2.5 é modelo de ponta)
3. ✅ **Grande contexto** (até 256K tokens)
4. ✅ **Fallback robusto** (8 modelos de reserva)
5. ✅ **Conforme vídeo** (configuração idêntica)

---

## 🔧 MANUTENÇÃO

**Se a API key da NVIDIA expirar:**

1. Acesse: https://build.nvidia.com/moonshotai/kimi-k2.5
2. Clique em "Generate API Key"
3. Atualize em `openclaw.json`:
   ```json
   "apiKey": "nvapi-NOVA_KEY_AQUI"
   ```
4. Reinicie: `openclaw gateway restart`

---

## 📞 SUPORTE

**Documentação:**
- NVIDIA NIM: https://build.nvidia.com/
- OpenClaw: https://docs.openclaw.ai

**Arquivo de configuração:**
`/home/severosa/.openclaw/openclaw.json`

---

**Última atualização:** 2026-02-22
**Status:** ✅ Operacional
