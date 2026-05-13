# Guia de Instalação - OpenClaw Browser Extension

## Verificação Rápida

A extensão do OpenClaw Browser Relay **NÃO** está configurada no seu sistema atualmente.

## Como Instalar

### Opção 1: Chrome Web Store (Recomendado)

1. **Abra o Chrome**
2. **Acesse a Chrome Web Store:**
   ```
   https://chrome.google.com/webstore
   ```
3. **Busque por:**
   - "OpenClaw Browser Relay"
   - Ou "OpenClaw"
4. **Clique em "Usar no Chrome"**
5. **Adicione a extensão**
6. **Fixe a extensão na barra de ferramentas** (clique no ícone de puzzle → fixe o OpenClaw)

### Opção 2: Instalação Manual (Developer Mode)

Se não encontrar na loja:

1. **Baixe a extensão:**
   ```bash
   # Verificar se existe no npm
   npm list -g openclaw-browser-extension
   ```

2. **Ou acesse o repositório oficial:**
   - GitHub: https://github.com/openclaw/browser-extension
   - Clone e instale manualmente

3. **No Chrome:**
   - Vá em `chrome://extensions/`
   - Ative o "Modo do desenvolvedor"
   - Clique em "Carregar sem compactação"
   - Selecione a pasta da extensão

### Opção 3: Usar o Browser Sandbox do OpenClaw

O OpenClaw tem um browser integrado que não requer extensão:

```bash
# Iniciar browser sandbox
openclaw browser start
```

**Limitação:** Browser isolado, requer login manual no Instagram.

## Depois de Instalar

1. **Clique no ícone da extensão** na barra do Chrome
2. **Abra uma aba** com o site que quer acessar (ex: Instagram)
3. **Clique na extensão novamente** para ativar (badge deve ficar verde/ON)
4. **Me avise** que está pronto!

## Verificar se Está Funcionando

Depois de instalada e ativada, execute:

```bash
openclaw browser status
```

Deve mostrar:
- Status: Connected
- Profile: chrome
- Tab: [URL da aba ativa]

## Alternativa Rápida ⚡

Se quiser agilizar **agora**:

1. **Assista o vídeo no Instagram**
2. **Grave a tela do celular** ou **extraia o áudio**
3. **Me envie aqui no WhatsApp**
4. **Eu transcrevo e analiso imediatamente!**

Esta é a forma mais rápida sem precisar configurar extensão.

---

**Precisa de ajuda?** Me avise qual opção quer usar!
