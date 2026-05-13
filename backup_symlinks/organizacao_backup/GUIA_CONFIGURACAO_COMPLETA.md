# Guia de Configuração Completa do Sistema de Análise Processual

## 📋 Resumo

Este guia configura o sistema para receber PDFs de **TRÊS formas diferentes**:
1. ✅ **WhatsApp/Telegram** (upload direto)
2. ✅ **Google Drive** (pasta monitorada)
3. ✅ **Upload manual** (linha de comando)

---

## 🚀 CONFIGURAÇÃO RÁPIDA (3 PASSOS)

### PASSO 1: Configurar Credenciais Google Drive

```bash
# Executar script de configuração
chmod +x ~/organizacao/configurar_credenciais_google.sh
~/organizacao/configurar_credenciais_google.sh
```

**Serão solicitados:**
- Client ID (do Google Cloud Console)
- Client Secret (do Google Cloud Console)
- Project ID (opcional)

#### Como obter esses valores:

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto ou selecione existente
3. Vá em **"APIs e Serviços" > "Credenciais"**
4. Clique em **"+ Criar Credenciais" > "ID do Cliente OAuth"**
5. Configure a tela de consentimento:
   - Tipo: **Externo**
   - Preencha: Nome do app, email de suporte
   - Escopos: Adicione "Google Drive API" > `.../auth/drive.readonly`
   - Publique o app (ou deixe em teste e adicione seu email como usuário de teste)

6. Crie as credenciais:
   - Tipo: **Aplicativo de computador**
   - Nome: `OpenClaw-Legal-System`

7. Copie **Client ID** e **Client Secret** e cole no script

---

### PASSO 2: Autenticar (Primeira vez)

```bash
cd ~/organizacao/controle-prazos
source ~/.openclaw/credentials/google_env.sh
python3 autenticar_google_drive.py
```

Isso abrirá um navegador. Faça login com sua conta Google e autorize o aplicativo.

---

### PASSO 3: Testar o Sistema

#### Opção A: Google Drive
```bash
# Coloque um PDF em: Processos-Juridicos/PDFs-Brutos
# No Google Drive, depois execute:
python3 integracao_google_drive_analise.py
```

#### Opção B: Upload Manual
```bash
# Copie o PDF para o servidor:
scp seu_arquivo.pdf severosa@IP_DO_SERVIDOR:~/processos/

# Depois analise:
cd ~/organizacao/controle-prazos
python3 ocr_analise_juridica.py ~/processos/seu_arquivo.pdf ~/organizacao/advocacia/ativos/TESTE/
```

---

## 📁 Estrutura de Pastas Esperada no Google Drive

```
Processos-Juridicos/
├── PDFs-Brutos/          ← Coloque PDFs aqui (serão analisados)
├── PDFs-Processados/     ← PDFs analisados são movidos aqui
└── Relatorios/          ← Relatórios gerados (opcional)
```

---

## 🔧 Configuração de Recebimento por WhatsApp/Telegram

Para receber PDFs diretamente pelos apps:

1. **O arquivo CHEGA automaticamente** em:
   ```
   /home/severosa/.openclaw/media/inbound/
   ```

2. **O sistema DEVE detectar** e processar o PDF

3. **Se não processar automaticamente**, use o comando:
   ```bash
   cd ~/organizacao/controle-prazos
   python3 processar_pdf_recebido.py
   ```

---

## 🛠️ Solução de Problemas

### Erro: "Credenciais não encontradas"
```bash
# Verifique se as variáveis estão carregadas:
echo $GOOGLE_CLIENT_ID

# Se vazio, recarregue:
source ~/.openclaw/credentials/google_env.sh
```

### Erro: "Token expirado"
```bash
# Delete o token antigo e reautentique:
rm ~/.openclaw/credentials/token_drive.pickle
python3 autenticar_google_drive.py
```

### Erro: "Acesso negado à pasta"
- Verifique se a pasta `Processos-Juridicos` é de sua propriedade
- Ou crie uma nova pasta e atualize o script

---

## 📋 STATUS ATUAL (Verificar)

Execute este diagnóstico:

```bash
bash ~/organizacao/diagnostico_sistema.sh
```

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] Credenciais Google criadas no Cloud Console
- [ ] Script `configurar_credenciais_google.sh` executado
- [ ] Arquivo `google_credentials.json` criado
- [ ] Autenticação OAuth2 realizada
- [ ] Token `token_drive.pickle` gerado
- [ ] Pasta `Processos-Juridicos/PDFs-Brutos` existe no Drive
- [ ] Teste com PDF real realizado
- [ ] S de WhatsApp/Telegram funcionando

---

**Pronto para começar?** Execute o Passo 1 agora: `~/organizacao/configurar_credenciais_google.sh`
