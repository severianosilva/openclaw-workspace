# Sistema de Troca Automática de Modelos de IA

## 🎯 Visão Geral

Sistema que monitora o uso de modelos de IA e troca automaticamente quando atinge limites configurados, garantindo continuidade do serviço sem interrupções.

## 📁 Localização

- **Script Python:** `/home/severosa/organizacao/configuracao/gerencia_modelos_ia.py`
- **Script Bash:** `/home/severosa/organizacao/configuracao/gerenciar_modelos.sh`
- **Configuração:** `/home/severosa/.openclaw/openclaw.json`
- **Uso:** `/home/severosa/.openclaw/usage_modelos.json`

## 🚀 Como Usar

### Ver Status dos Modelos

```bash
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh status
```

Mostra uso atual de cada modelo e limites.

### Registrar Uso

```bash
# Registrar uso do modelo atual
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh uso

# Registrar uso de modelo específico
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh uso qwen-portal/coder-model
```

### Trocar Modelo Manualmente

```bash
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh trocar manual
```

### Configurar Limites

```bash
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh limite openrouter/auto 500
```

### Resetar Contagens

```bash
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh reset
```

## ⚙️ Limites Padrão

| Modelo | Limite (req/dia) |
|--------|-----------------|
| qwen-portal/coder-model | 100 |
| qwen-portal/vision-model | 50 |
| openrouter/auto | 200 |
| minimax-portal/MiniMax-M2.1 | 150 |
| minimax-portal/MiniMax-M2.1-lightning | 300 |
| google/gemini-3-pro-preview | 100 |
| synthetic/hf:MiniMaxAI/MiniMax-M2.1 | 250 |

## 🔄 Ordem de Fallback

Quando o modelo atual atinge o limite, o sistema troca para o próximo disponível:

1. qwen-portal/coder-model (padrão)
2. minimax-portal/MiniMax-M2.1-lightning
3. minimax-portal/MiniMax-M2.1
4. synthetic/hf:MiniMaxAI/MiniMax-M2.1
5. openrouter/auto
6. google/gemini-3-pro-preview
7. qwen-portal/vision-model

## 🤖 Automação

### Opção 1: Cron Job (Recomendado)

Adicione ao crontab para verificar a cada hora:

```bash
# Editar crontab
crontab -e

# Adicionar linha (verifica a cada hora)
0 * * * * bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh auto >> /var/log/openclaw_modelos.log 2>&1
```

### Opção 2: Integração com OpenClaw

O sistema pode ser chamado automaticamente após cada uso do modelo.

## 📊 Exemplo de Saída

```
============================================================
STATUS DOS MODELOS DE IA
============================================================

🎯 Modelo Atual: qwen-portal/coder-model
🕒 Última Troca: 2026-02-20T18:30:00

📊 Uso por Modelo:
------------------------------------------------------------
🎯 ⚠️  LIMITE qwen-portal/coder-model            [██████████] 100/100 (total: 1250)
   ✅ minimax-portal/MiniMax-M2.1-lightning      [███░░░░░░░] 30/300 (total: 450)
   ✅ minimax-portal/MiniMax-M2.1                [░░░░░░░░░░] 0/150 (total: 0)
   ...

📜 Histórico Recente de Trocas:
------------------------------------------------------------
  2026-02-20 18:30 | qwen-portal/coder-model    → minimax-portal/MiniMax-M2.1-lightning (limite_atingido)
  2026-02-19 14:22 | openrouter/auto            → qwen-portal/coder-model (manual)
============================================================
```

## 🔧 Configuração Avançada

### Alterar Limites

Edite o arquivo Python e modifique o dicionário `self.limites`:

```python
self.limites = {
    'qwen-portal/coder-model': 200,  # Aumentar para 200
    'openrouter/auto': 500,           # Aumentar para 500
    # ...
}
```

### Alterar Ordem de Fallback

Modifique `self.fallback_order`:

```python
self.fallback_order = [
    'seu-modelo-preferido',
    'segunda-opcao',
    # ...
]
```

## 🎯 Casos de Uso

### 1. Uso Normal
O sistema opera com o modelo padrão até atingir o limite.

### 2. Limite Atingido
Automaticamente troca para o próximo modelo disponível.

### 3. Todos no Limite
Resetá as contagens e continua com o modelo padrão.

### 4. Troca Manual
Útil para testes ou quando quer usar modelo específico.

## 📝 Logs

Os logs são salvos em:
- **Uso:** `/home/severosa/.openclaw/usage_modelos.json`
- **Limites:** `/home/severosa/.openclaw/limites_modelos.json`

## ⚠️ Importante

- **Limites são diários** - resetam automaticamente a cada dia
- **Troca automática** requer reinício do gateway (feito automaticamente)
- **Fallback em cascata** - se todos atingirem limite, reseta contagens

## 🆘 Solução de Problemas

### Gateway não reinicia automaticamente
```bash
# Reinicie manualmente
openclaw gateway restart
```

### Modelo não troca
```bash
# Verifique status
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh status

# Force troca manual
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh trocar erro
```

### Perdeu configuração
```bash
# Resetar contagens
bash /home/severosa/organizacao/configuracao/gerenciar_modelos.sh reset
```

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação: `/home/severosa/organizacao/configuracao/EXTENSAO_CHROME_GUIA.md`
- Logs: `/home/severosa/.openclaw/usage_modelos.json`

---

**Versão:** 1.0
**Última atualização:** Fevereiro/2026
**Status:** ✅ Operacional
