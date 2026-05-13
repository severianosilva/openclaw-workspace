# Agentes Autônomos para Desenvolvimento

Sistema de agentes autônomos que criam, testam e mantêm código de forma independente.

## Arquitetura

```
├── agents/           # Agentes especializados
│   ├── planner/      # Planejador de tarefas
│   ├── coder/        # Escritor de código
│   ├── tester/       # Testador automatizado
│   └── deployer/     # Deploy automático
├── workspace/        # Diretório de trabalho dos agentes
├── memory/           # Memória compartilhada entre agentes
└── config/           # Configurações do sistema
```

## Como Funciona

1. **Planner Agent** - Recebe requisição, decompõe em tarefas
2. **Coder Agent** - Gera código para cada tarefa
3. **Tester Agent** - Executa testes automatizados
4. **Deployer Agent** - Implanta aplicação em produção

## Uso

```bash
# Iniciar sistema
python main.py --start

# Enviar requisição
python main.py --request "Criar API REST para gerenciamento de tarefas"
```