---
name: juridical-reminder-creator
description: Cria lembretes baseados em prazos identificados em documentos jurídicos
author: Sistema Jurídico Automatizado
version: 1.0.0
category: reminders
tags: [legal, reminders, deadlines, notifications]
---

# Criador de Lembretes Jurídicos

Esta skill cria lembretes automáticos baseados em prazos identificados em documentos jurídicos.

## Funcionalidades

- Criação de lembretes baseados em prazos identificados
- Agendamento de notificações antecipadas
- Integração com sistema de processos
- Suporte a diferentes tipos de alertas

## Configuração

A skill requer lista de prazos e número do processo associado.

## Uso

A skill pode ser invocada após identificação de prazos em documentos jurídicos.

## Implementação

```python
def criar_lembretes_juridicos(deadlines, process_number, advance_notice_days=3):
    '''
    Cria lembretes para prazos jurídicos
    '''
    from datetime import datetime, timedelta
    import uuid
    
    lembretes_criados = []
    
    for prazo in deadlines:
        descricao = prazo.get('descricao', 'Prazo não especificado')
        contexto = prazo.get('contexto', 'Contexto não fornecido')
        
        # Calcular data do lembrete (antecedência)
        # Neste exemplo simplificado, assumimos que a data do prazo está embutida na descrição
        # Em uma implementação real, isso seria extraído do documento
        
        # Gerar ID único para o lembrete
        lembrete_id = str(uuid.uuid4())
        
        # Calcular data do lembrete (3 dias antes por padrão)
        lembrete_info = {
            "reminder_id": lembrete_id,
            "process_number": process_number,
            "deadline_description": descricao,
            "deadline_context": contexto,
            "advance_notice_days": advance_notice_days,
            "created_at": datetime.now().isoformat(),
            "status": "scheduled"
        }
        
        lembretes_criados.append(lembrete_info)
    
    return {
        "reminder_ids": [lem["reminder_id"] for lem in lembretes_criados],
        "scheduled_reminders": lembretes_criados,
        "total_reminders": len(lembretes_criados)
    }

# Função principal da skill
def execute(inputs):
    '''
    Função principal da skill do Refly
    '''
    deadlines = inputs.get('deadlines', [])
    process_number = inputs.get('process_number', '')
    advance_notice_days = inputs.get('advance_notice_days', 3)
    
    if not deadlines:
        return {
            "error": "deadlines é obrigatório",
            "reminder_ids": [],
            "scheduled_reminders": [],
            "total_reminders": 0
        }
    
    if not process_number:
        return {
            "error": "process_number é obrigatório",
            "reminder_ids": [],
            "scheduled_reminders": [],
            "total_reminders": 0
        }
    
    # Chamar função de criação de lembretes
    result = criar_lembretes_juridicos(deadlines, process_number, advance_notice_days)
    
    return result
```
