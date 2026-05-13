# 🎬 GOOGLE COLAB - Processamento de Vídeo em Nuvem

## 📋 O QUE É ISSO

Notebook Python que roda **100% na nuvem do Google** (grátis) para:
- ✅ Transformar áudio em vídeo completo
- ✅ Adicionar imagens/vídeos de stock
- ✅ Inserir legendas automáticas
- ✅ Gerar thumbnail
- ✅ Exportar pronto para YouTube

**Custo:** R$ 0,00 (Google Colab Free Tier)
**Requisitos:** Apenas conta Google (Gmail)

---

## 🚀 COMO USAR (PASSO A PASSO)

### **PASSO 1: ABRIR GOOGLE COLAB**
1. Acesse: https://colab.research.google.com/
2. Clique em **"Novo Notebook"**
3. Pronto! Ambiente Python criado na nuvem

### **PASSO 2: COPIAR CÓDIGO**
1. Abra o arquivo: `notebook_producao_video.ipynb` (ou copie do `.py`)
2. Cole célula por célula no Colab
3. OU: Faça upload do `.ipynb` direto no Colab

### **PASSO 3: EXECUTAR**
1. Clique em **"Play"** em cada célula (ou Runtime > Run all)
2. Faça upload do seu áudio quando solicitado
3. Aguarde processamento (2-5 minutos)
4. Baixe vídeo pronto!

---

## 📁 ARQUIVOS DISPONÍVEIS

| Arquivo | Função |
|---------|--------|
| `notebook_producao_video.ipynb` | Notebook completo (upload direto no Colab) |
| `producao_video_colab.py` | Script Python (copiar/colar) |
| `configuracao_colab.md` | Guia detalhado de configuração |

---

## ⚙️ RECURSOS INCLUÍDOS

### ✅ Processamento Automático
- [x] Upload de áudio (MP3/WAV/OGG)
- [x] Download de imagens/vídeos de stock (Pexels, Pixabay)
- [x] Montagem automática de cenas
- [x] Legendas sincronizadas (se tiver transcript)
- [x] Transições profissionais
- [x] Música de fundo (opcional, sem copyright)

### ✅ Personalização
- [x] Escolher estilo (tutorial, documentário, vlog)
- [x] Cores e fontes da thumbnail
- [x] Duração de cada cena
- [x] Tipo de transição

### ✅ Exportação
- [x] MP4 H.264 (YouTube ready)
- [x] 1080p ou 720p
- [x] Compressão otimizada
- [x] Download direto para seu PC

---

## 💡 EXEMPLO DE USO

```python
# No Colab, depois de rodar as células:

1. Upload do áudio:
   → Clique em "Escolher arquivos"
   → Selecione: narracao_aprender_ingles_2026.mp3

2. Configure:
   → Tema: "Educação/Idiomas"
   → Duração: 10 minutos
   → Estilo: "Tutorial com texto na tela"

3. Execute:
   → Clique em "Gerar Vídeo"
   → Aguarde 3-5 minutos

4. Baixe:
   → Vídeo pronto em MP4
   → Thumbnail em PNG
   → Legendas em SRT (opcional)
```

---

## 🔧 LIMITAÇÕES DO FREE TIER

| Recurso | Limite |
|---------|--------|
| Sessão máxima | 12 horas (depois desconecta) |
| GPU disponível | T4 ou K80 (grátis) |
| RAM | ~12-16 GB |
| Armazenamento | ~80 GB (temporário) |
| Uso diário | Variável (Google limita uso excessivo) |

**Importante:** Arquivos são temporários! Sempre baixe o vídeo antes de fechar.

---

## 🎯 FLUXO COMPLETO INTEGRADO

```
LOCAL (Seu PC)
    ↓
1. Gerar roteiro (Python script)
2. Gerar áudio (TTS OpenClaw)
    ↓
UPLOAD PARA COLAB
    ↓
3. Processar vídeo (Colab Notebook)
4. Gerar thumbnail (Bing AI via API)
    ↓
DOWNLOAD
    ↓
5. Vídeo pronto (MP4)
6. Thumbnail (PNG)
    ↓
UPLOAD YOUTUBE
    ↓
7. Publicar com metadata
```

---

## 📊 COMPARAÇÃO: LOCAL vs CLOUD

| Aspecto | Local (WSL) | Cloud (Colab) |
|---------|-------------|---------------|
| Custo | Grátis | Grátis |
| Armazenamento | Limitado pelo HD | 80GB por sessão |
| Processamento | Depende do seu PC | GPU Tesla T4 |
| Velocidade | Variável | Rápido (GPU) |
| Disponibilidade | 24/7 | 12h por sessão |
| Configuração | Já pronto | Copiar código |

**Recomendação:** Use **híbrido**:
- Roteiro + Áudio: Local (OpenClaw)
- Vídeo + Thumbnail: Cloud (Colab)

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### "Sessão desconectou"
- Normal após 12h ou inatividade
- Reconecte e reexecute as células
- Sempre baixe arquivos antes de fechar

### "Sem GPU disponível"
- Tente novamente em alguns minutos
- Runtime > Change runtime type > GPU
- Free tier tem fila às vezes

### "Erro ao baixar vídeo"
- Verifique espaço no seu PC
- Tente formato diferente (720p vs 1080p)
- Reinicie o runtime

---

## 📞 PRÓXIMOS PASSOS

1. **Abra o Colab:** https://colab.research.google.com/
2. **Copie o notebook** deste diretório
3. **Teste com o áudio** já gerado: `narracao_aprender_ingles_2026.mp3`
4. **Me avise** se funcionar ou se precisar de ajustes!

---

**Arquivo principal:** `notebook_producao_video.ipynb`
**Script alternativo:** `producao_video_colab.py`
