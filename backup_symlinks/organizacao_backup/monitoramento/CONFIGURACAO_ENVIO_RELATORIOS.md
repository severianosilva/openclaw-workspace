# Configuração de Envio de Relatórios Diários

Este documento descreve como configurar o envio automático de relatórios diários por WhatsApp e e-mail.

## Status Atual

O sistema de geração de relatórios diários está funcionando corretamente e os relatórios são salvos em:
`/home/severosa/organizacao/monitoramento/relatorios-diarios/`

## Envio por WhatsApp

### Configuração Necessária

Para habilitar o envio automático por WhatsApp, é necessário:

1. **Verificar configuração atual do WhatsApp no OpenClaw**:
   - O número `+5531982436396` já está configurado como permitido no arquivo `/home/severosa/.openclaw/openclaw.json`
   - O gateway do OpenClaw precisa estar funcionando corretamente

2. **Testar envio manual**:
   ```bash
   openclaw message send --channel whatsapp --target "+5531982436396" --message "Teste de envio"
   ```

3. **Configuração ideal (recomendada)**:
   - Usar a API do WhatsApp Business para envios automáticos
   - Ou configurar credenciais adicionais no OpenClaw se ainda não estiver funcionando

### Comandos Relevantes

- Script de envio: `/home/severosa/organizacao/monitoramento/enviar_relatorio_diario.sh`
- Local dos relatórios: `/home/severosa/organizacao/monitoramento/relatorios-diarios/`

## Envio por E-mail

### Configuração Necessária

Para habilitar o envio automático por e-mail, é necessário:

1. **Configurar credenciais SMTP**:
   - Servidor SMTP (ex: smtp.gmail.com)
   - Porta (ex: 587 para TLS)
   - Usuário (ex: seu_email@gmail.com)
   - Senha ou token de app

2. **Modelos disponíveis**:
   - Modelo de verificação de e-mails: `/home/severosa/organizacao/monitoramento/modelo_verificar_emails.py`
   - Este modelo contém instruções para configuração de acesso a e-mails

3. **Integração com o script de envio**:
   - Adicionar funcionalidade de envio por e-mail ao script `/home/severosa/organizacao/monitoramento/enviar_relatorio_diario.sh`

### Configuração para Gmail

Se for usar Gmail, será necessário:
- Habilitar IMAP no Gmail
- Criar um token de app (recomendado) ou usar senha do Gmail
- Configurar os parâmetros SMTP:
  - Servidor: smtp.gmail.com
  - Porta: 587
  - Criptografia: TLS

## Configuração Automática

O envio de relatórios está integrado ao cron job diário que roda às 8h da manhã:
```
0 8 * * * DISPLAY=:0 /home/severosa/organizacao/monitoramento/executar_monitoramento_diario.sh
```

## Próximos Passos

1. **Resolver problema de envio do OpenClaw** para habilitar envio automático por WhatsApp
2. **Configurar credenciais de e-mail** para habilitar envio automático por e-mail
3. **Testar o fluxo completo** de geração e envio de relatórios

## Testes

Para testar manualmente o envio de relatório:
```bash
bash /home/severosa/organizacao/monitoramento/enviar_relatorio_diario.sh
```