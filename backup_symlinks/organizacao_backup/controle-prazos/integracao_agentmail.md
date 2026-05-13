# Integração com AgentMail

Este documento descreve como integrar o sistema jurídico automatizado com o AgentMail usando o email attention_agent@agentmail.to.

## Visão Geral

O email attention_agent@agentmail.to pode ser usado para receber notificações e alertas do sistema jurídico automatizado. Esta integração permite:

- Receber notificações de prazos processuais
- Receber alertas de novos documentos
- Receber resumos diários/semanais de atividades
- Encaminhar informações relevantes para o Discord

## Configuração

### 1. Configuração do Email

O sistema jurídico automatizado já tem suporte para envio de emails. Para configurar o AgentMail:

1. Edite o script de configuração de email:
   ```bash
   ./configurar_email.sh
   ```

2. Configure o email de destino como `attention_agent@agentmail.to`

### 2. Integração com o Discord

Após configurar o email, você pode usar serviços de automação como:

- **Zapier**: Crie um zap que monitora o email e posta no Discord
- **Integromat**: Crie um scenario que faz a integração
- **Make**: Crie uma integração que lê o email e envia para o Discord

### 3. Configuração do Fluxo de Trabalho

#### Opção 1: Email → Discord (via serviço de automação)
1. O sistema jurídico envia notificações para `attention_agent@agentmail.to`
2. Serviço de automação (Zapier, Integromat) monitora o email
3. Quando recebe mensagem, o serviço posta no canal do Discord

#### Opção 2: Sistema direto → Discord (via bot)
1. Use o script `integracao_discord.py` para rodar um bot diretamente
2. O sistema pode enviar informações diretamente ao bot

## Comandos do Bot no Discord

Depois que o bot estiver rodando, os seguintes comandos estarão disponíveis:

- `!status` - Mostra o status do sistema jurídico automatizado
- `!processos [tipo]` - Lista os processos (tipos: advocacia, servidor, todos)
- `!lembretes [dias]` - Lista os lembretes para os próximos dias

## Configuração do Bot

Para configurar o bot do Discord:

1. Execute o script de configuração:
   ```bash
   ./configurar_discord.sh
   ```

2. Siga as instruções para criar o bot no Discord Developer Portal

3. Execute o bot:
   ```bash
   python3 integracao_discord.py SEU_TOKEN_DO_BOT
   ```

## Benefícios da Integração

- **Centralização de informações**: Todas as notificações em um só lugar
- **Notificações em tempo real**: Alertas imediatos sobre prazos e atividades
- **Colaboração**: Equipes podem acompanhar o status dos processos
- **Histórico**: Registros de todas as atividades em um canal organizado

## Segurança

- O token do bot deve ser mantido em segredo
- Use permissões mínimas necessárias no Discord
- Monitore o tráfego de dados entre os sistemas
- Revogue tokens periodicamente

## Troubleshooting

Se encontrar problemas:

1. Verifique se o token do bot está correto
2. Confirme que as permissões do bot estão configuradas corretamente
3. Verifique se o email attention_agent@agentmail.to está recebendo mensagens
4. Consulte os logs do sistema jurídico automatizado