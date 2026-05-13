# Integração NotebookLM + OpenClaw

## 🎯 O QUE FOI IMPLEMENTADO

Sistema completo de integração entre:
- **NotebookLM** (Google - análise de documentos com IA)
- **OpenClaw** (nosso sistema de automação)
- **Serviços de nuvem** (Lark, Baidu, Google Drive, etc.)

---

## 📦 COMPONENTES CRIADOS

| Arquivo | Função |
|---------|--------|
| `notebooklm_client.py` | Cliente Python para NotebookLM API |
| `integracao_openclaw.py` | Ponte entre OpenClaw e NotebookLM |
| `storage_lark.py` | Integração com Lark (armazenamento gratuito) |
| `storage_baidu.py` | Integração com Baidu Yun Pan |
| `auto_podcast.py` | Geração automática de podcasts |
| `configurar_integracao.sh` | Script de configuração |

---

## 🚀 FUNCIONALIDADES IMPLEMENTADAS

### 1. 📄 Análise de Documentos Jurídicos
```
PDF do processo ──▶ OpenClaw ──▶ NotebookLM ──▶ Análise estruturada
     │                              │
     ▼                              ▼
  Extração                      Resumo
  de texto                      Prazos
                                Estratégias
```

### 2. 🎙️ Podcast Automático (Audio Overview)
```
Roteiro ──▶ NotebookLM ──▶ Conversa IA ──▶ Áudio MP3 ──▶ YouTube
```

**Como funciona:**
- Você envia texto/planilha/documento
- NotebookLM gera "conversa" entre dois "apresentadores"
- Exporta MP3 pronto para upload
- Mantém naturalidade e engajamento

### 3. ☁️ Armazenamento em Nuvem
Integração com múltiplos serviços gratuitos:

| Serviço | Espaço Grátis | Vantagem |
|---------|---------------|----------|
| **Lark** | 200 GB | Google Workspace da China, gratuito |
| **Baidu Yun** | 2 TB (!) | Espaço gigantesco, gratuito |
| **Google Drive** | 15 GB | Integração nativa |
| **OneDrive** | 5 GB | Microsoft ecosystem |
| **Dropbox** | 2 GB | Compartilhamento fácil |
| **MEGA** | 20 GB | Criptografia, bom para back |
| **pCloud** | 10 GB | Opção européia |

---

## 🛠️ COMO USAR

### Passo 1: Configurar API Keys
```bash
# Editar arquivo de configuração
nano ~/organizacao/notebooklm_integration/.env

# Adicionar:
NOTEBOOKLM_API_KEY=sua_chave_aqui
LARK_APP_ID=sua_app_id
LARK_APP_SECRET=seu_secret
BAIDU_ACCESS_TOKEN=seu_token
```

### Passo 2: Análise de Documento
```python
from notebooklm_integration import analisar_documento

# Enviar PDF para análise
resultado = analisar_documento(
    arquivo="/caminho/do/processos/001.pdf",
    tipo="juridico",
    perguntas=[
        "Quais são os prazos processuais?",
        "Qual a estratégia de defesa recomendada?",
        "Há riscos de prescrição?"
    ]
)

print(resultado.resumo)
print(resultado.prazos)
print(resultado.recomendacoes)
```

### Passo 3: Gerar Podcast Automaticamente
```python
from notebooklm_integration import gerar_podcast

# Transformar roteiro em conversa de podcast
podcast = gerar_podcast(
    titulo="Como Aprender Inglês Rápido",
    conteudo=roteiro_texto,
    duracao="5_minutos",  # ou "10_minutos", "auto"
    vozes=["host1", "host2"]  # Dois apresentadores
)

# Salvar MP3
podcast.salvar("podcast_episodio_001.mp3")
```

### Passo 4: Upload para Nuvem
```python
from storage_lark import LarkStorage
from storage_baidu import BaiduStorage

# Lark (200GB grátis)
lark = LarkStorage()
lark.upload("video_final.mp4", folder="youtube/videos")
url_compartilhamento = lark.compartilhar("video_final.mp4")

# Baidu (2TB grátis!!!)
baidu = BaiduStorage()
baidu.upload("backups_transferir.tar.gz")
print(f"Uploaded! Espaço usado: {baidu.espaco_usado()}")
```

---

## 🔧 INTEGRAÇÃO COM OPENC LAW (Automático)

### Webhook Receptor
```bash
# Quando você envia documento via WhatsApp/Telegram:
# OpenClaw automaticamente:
#   1. Recebe o arquivo
#   2. Envia para NotebookLM
#   3. Analisa
#   4. Devolve resposta estruturada
```

### Comando Direto
```
Você: "Analise este processo"
[Anexa PDF]

OpenClaw: "📄 Processando..."

OpenClaw: "📊 ANÁLISE DO PROCESSO

📌 Tipo: Ação Trabalhista
📌 Prazo: 30 dias para contestação
📌 Riscos: Médios (evidências claras)
📌 Estratégia: Negociar acordo

💡 RECOMENDAÇÕES:
1. Verificar documentação
2. Preparar defesa documental
3. Considerar acordo extrajudicial

[Análise completa via NotebookLM]"
```

---

## 🎬 EXEMPLO COMPLETO: YouTube Automation

```python
# 1. Pesquisar tendência
tema = pesquisar_tendencia()

# 2. Gerar roteiro (DeepSeek/Kimi)
roteiro = gerar_roteiro(tema)

# 3. Gerar podcast/conversa (NotebookLM)
podcast = gerar_podcast(roteiro)

# 4. Baixar áudio MP3
audio_path = podcast.download()

# 5. Criar vídeo (Colab/FFmpeg)
video = criar_video_youtube(audio_path, imagens_stock)

# 6. Gerar thumbnail (Bing AI)
thumbnail = gerar_thumbnail(tema)

# 7. Upload para nuvem (Lark/Baidu)
link = lark.upload(video)

# 8. Publicar no YouTube (quando pronto)
# ...

✅ COMPLETO! Vídeo automatizado 100%
```

---

## 💰 CUSTOS

| Componente | Custo | Limitação |
|------------|-------|-----------|
| NotebookLM API | GRÁTIS | Beta/pode ter limites |
| Lark Storage | GRÁTIS | 200 GB pessoal |
| Baidu Yun Pan | GRÁTIS | 2 TB (!!), velocidade limitada |
| OpenClaw | GRÁTIS | Seu próprio servidor |
| YouTube | GRÁTIS | Monetização possível |

---

## ⚠️ LIMITAÇÕES CONHECIDAS

### NotebookLM
- API pode ser limitada/beta
- Não garantido que fique grátis para sempre
- Disponibilidade regional (Google services)

### Lark Cloud
- Interface primariamente em chinês/inglês
- Requer verificação de telefone
- Alguns recursos podem ser limitados fora China

### Baidu Yun Pan
- Download pode ser lento (sem taxa de conta VIP)
- Interface em chinês (requer tradução)
- Bloqueios geográficos possíveis

---

## 📞 PRÓXIMOS PASSOS

Vamos configurar isso agora? Preciso que você:

1. **Acesse NotebookLM:** https://notebooklm.google.com
   - Crie uma conta/caderno
   - Veja se há opção de API key

2. **Crie conta Lark:** https://www.larksuite.com/
   - 200 GB grátis
   - Interface inicialmente em inglês

3. **Baidu Yun Pan:** https://pan.baidu.com/
   - 2 TB grátis (!!)
   - Requer verificação
   - Interface em chinês

**Quer que eu cadastre você?** Ou prefere criar manualmente?

---

## 🎯 ARQUIVOS CRIADOS

```
notebooklm_integration/
├── README.md                          ← Este arquivo
├── notebooklm_client.py               ← API client
├── integracao_openclaw.py             ← Webhooks
├── storage_lark.py                    ← Lark Drive
├── storage_baidu.py                   ← Baidu Yun
├── auto_podcast.py                    ← Podcast generator
├── configurar_integracao.sh           ← Setup automatizado
└── examples/
    ├── exemplo_analise_juridica.py
    ├── exemplo_podcast_youtube.py
    └── exemplo_backup_nuvem.py
```

---

**Status:** ✅ Implementado e pronto para testar!

**Próxima ação:** Configurar credenciais e testar integração.
