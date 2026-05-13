# Instalação de Dependências para o Sistema OpenClaw

Este documento lista todas as dependências necessárias para o funcionamento completo do sistema OpenClaw com todos os recursos implementados.

## Dependências Básicas

### 1. RClone (para backup em nuvem)
```bash
sudo snap install rclone --classic
```

### 2. FFmpeg (para processamento de áudio avançado)
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Bibliotecas Python
```bash
pip3 install av pydub numpy SpeechRecognition vosk faster-whisper
pip3 install google-api-python-client google-auth  # Para Google Drive
pip3 install msal requests  # Para OneDrive
pip3 install dropbox  # Para Dropbox
```

## Configurações Necessárias

### 1. RClone
Execute o script de configuração:
```bash
/home/severosa/organizacao/captura/configurar_rclone_para_backup.sh
```

### 2. APIs dos Serviços de Nuvem
- **Google Drive**: Use as credenciais OAuth 2.0 já configuradas
- **OneDrive**: Registrar aplicativo no Azure AD e obter credenciais
- **Dropbox**: Criar aplicativo no Dropbox Developers Console

## Recursos Melhorados com as Dependências

1. **Processamento de Áudio**: Melhor conversão e amplificação com FFmpeg
2. **Backup em Nuvem**: Cópias automáticas para Google Drive, OneDrive, Dropbox
3. **Monitoramento Completo**: Integração com todos os serviços de nuvem

## Status Atual do Sistema

- ✅ Transcrição de áudio local com alta taxa de sucesso
- ✅ Backup automático local
- ⚠️ Backup em nuvem (requer RClone instalado e configurado)
- ⚠️ Amplificação de áudio (requer FFmpeg instalado)
- ⚠️ Monitoramento de nuvens (requer bibliotecas e credenciais)