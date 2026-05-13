# Guia de Instalação - Chrome Browser Extension

## ✅ Extensão Já Está Instalada!

A extensão do OpenClaw Browser Relay foi instalada em:
```
/home/severosa/.openclaw/extensions/chrome-browser-relay/
```

## 📋 Como Carregar no Chrome

### Passo 1: Abrir Chrome
Abra o navegador Google Chrome no seu computador.

### Passo 2: Acessar Extensões
Na barra de endereço do Chrome, digite:
```
chrome://extensions/
```

### Passo 3: Ativar Modo do Desenvolvedor
No canto superior direito da página, ative a chave:
```
✅ Modo do desenvolvedor
```

### Passo 4: Carregar Extensão
1. Clique em **"Carregar sem compactação"** (ou "Load unpacked")
2. Navegue até a pasta:
   ```
   /home/severosa/.openclaw/extensions/chrome-browser-relay/
   ```
3. Selecione a pasta e clique em **"Selecionar"** (ou "Open")

### Passo 5: Fixar a Extensão
1. Clique no ícone de **quebra-cabeça** na barra de ferramentas do Chrome
2. Encontre "OpenClaw Browser Relay"
3. Clique no **pin** para fixar na barra

### Passo 6: Ativar em uma Aba
1. Abra uma aba no Chrome (pode ser qualquer site)
2. Clique no ícone da extensão OpenClaw
3. O badge deve mostrar **"ON"** quando estiver ativa

## 🎯 Como Usar

Depois de instalada e ativada:

**No OpenClaw, use:**
```bash
openclaw browser --profile chrome tabs
```

**Ou nas ferramentas do agente:**
- `browser` com `profile="chrome"`

## ⚠️ Importante

- A extensão controla **apenas a aba onde você clicou no ícone**
- Para mudar de aba, clique no ícone da extensão na nova aba
- O badge **"ON"** indica que a extensão está ativa naquela aba
- Badge **"!"** significa que o relay não está rodando

## 🔧 Se Der Problema

1. **Extensão não aparece:**
   - Verifique se carregou a pasta correta
   - Recarregue em `chrome://extensions/`

2. **Badge mostra "!" (erro):**
   - Reinicie o gateway: `openclaw gateway restart`
   - Verifique se o relay está rodando

3. **Não consegue controlar a aba:**
   - Certifique-se de que clicou no ícone para ativar (badge "ON")
   - Tente recarregar a extensão

## 📞 Precisa de Ajuda?

Me avise se tiver dificuldades na instalação!

---

**Caminho da extensão:** `/home/severosa/.openclaw/extensions/chrome-browser-relay/`
**Status:** ✅ Pronta para instalar
