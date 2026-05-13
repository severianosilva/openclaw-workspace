# Quick Start - Agentes Autônomos

## Como usar

```bash
# Executar uma requisição única
python main.py --request "Criar API de tarefas"

# Iniciar modo interativo
python main.py --start
```

## Exemplos de requisições

- "Criar API REST para blog"
- "Script para backup de arquivos"
- "Dashboard com React"
- "Bot para Telegram"

## Arquitetura

```
agents/
  planner.py   - Analisa requisição
  coder.py     - Gera código
  tester.py    - Testa código
workspace/     - Códigos gerados
memory/        - Histórico de tarefas
```