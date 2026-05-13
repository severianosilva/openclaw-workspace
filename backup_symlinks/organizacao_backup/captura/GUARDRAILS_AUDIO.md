# GUARDRAILS PARA TRANSCRIÇÃO DE ÁUDIO GRATUITA

## Propósito
Este documento estabelece os princípios e limites para o uso do sistema de transcrição de áudio recebido via WhatsApp usando métodos gratuitos.

## Configuração
1. Execute o script de configuração gratuito:
   ```bash
   ~/organizacao/captura/configurar_transcricao_audio.sh
   ```

2. Escolha a opção de instalação (Whisper local, Google STT ou ambos)

## Funcionamento
- Os arquivos de áudio recebidos via WhatsApp são automaticamente detectados
- O sistema tenta transcrever cada novo arquivo de áudio usando métodos gratuitos:
  - Primeiro tenta com Whisper local (se instalado)
  - Depois tenta com Google STT gratuito (com limites diários)
  - Usa conversão de formatos com PyAV para suportar diversos tipos de áudio (OGG, MP3, etc.)
  - Implementa análise de volume para identificar se o áudio precisa de amplificação
  - Usa múltiplos idiomas portugueses (pt-BR, pt-PT, pt) para melhor detecção com Google STT
  - Novo script otimizado transcricao_qwen_ajudada.py com melhor detecção de fala e análise de volume
- As transcrições são salvas em `~/organizacao/captura/transcricoes/`
- Os arquivos originais são movidos para `~/organizacao/captura/transcricoes/audios_processados/`

## Limitações e Considerações
- O Whisper local requer instalação prévia e recursos computacionais
- O Google STT gratuito tem limites diários de uso
- A qualidade da transcrição depende da qualidade do áudio e da clareza da fala
- Arquivos de áudio muito grandes podem ter limites técnicos
- A transcrição local pode levar mais tempo inicialmente
- O sistema agora suporta formatos como OGG/Opus graças à conversão com PyAV
- A amplificação depende da instalação do FFmpeg (senão usa apenas análise de volume)
- O novo script otimizado transcricao_qwen_ajudada.py melhora significativamente a taxa de sucesso na detecção de fala

## Privacidade e Segurança
- Nenhuma chave de API necessária para o modo gratuito
- As transcrições são processadas localmente ou com serviços online seguros
- As transcrições são armazenadas localmente e não são compartilhadas externamente
- Revise regularmente os arquivos de transcrição para garantir confidencialidade

## Manutenção
- O sistema faz parte do monitoramento diário automatizado
- Verifique regularmente o diretório de transcrições para garantir funcionamento adequado
- Em caso de falhas, verifique a instalação das dependências (PyAV, numpy, SpeechRecognition, FFmpeg opcional)

## Monitoramento
- O processamento de áudio é integrado ao relatório diário em `~/organizacao/monitoramento/relatorios-diarios/`
- Qualquer erro no processamento de áudio será registrado no relatório diário