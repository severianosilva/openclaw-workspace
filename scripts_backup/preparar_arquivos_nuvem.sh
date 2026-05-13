#!/bin/bash
# Prepara arquivos para transferência manual (sem rclone)
# Cria listas e compacta arquivos grandes

echo "=========================================="
echo "  PREPARAÇÃO PARA NUVEM (Sem rclone)"
echo "=========================================="
echo ""

# Criar diretório de staging
STAGING_DIR="$HOME/organizacao/staging_nuvem"
mkdir -p "$STAGING_DIR"
echo "📁 Diretório de staging: $STAGING_DIR"
echo ""

# 1. Analisar o que precisa ser movido
echo "🔍 ANALISANDO ARQUIVOS..."
echo ""

# Listar backups grandes
BACKUP_DIR="$HOME/organizacao/backup"
echo "📦 BACKUPS (>100MB, >7 dias):"
if [ -d "$BACKUP_DIR" ]; then
    find "$BACKUP_DIR" -name "*.tar.gz" -size +100M -mtime +7 -exec ls -lh {} \; | tee "$STAGING_DIR/lista_backups.txt"
    echo "  $(wc -l < "$STAGING_DIR/lista_backups.txt" 2>/dev/null || echo 0) arquivos encontrados"
else
    echo "  Diretório não encontrado"
fi
echo ""

# Listar mídia antiga
MEDIA_DIR="$HOME/.openclaw/media/inbound"
echo "🎵 MÍDIA (>30 dias):"
if [ -d "$MEDIA_DIR" ]; then
    find "$MEDIA_DIR" -type f -mtime +30 > "$STAGING_DIR/lista_midia.txt" 2>/dev/null
    TOTAL_MIDIA=$(wc -l < "$STAGING_DIR/lista_midia.txt" 2>/dev/null || echo 0)
    echo "  $TOTAL_MIDIA arquivos encontrados"
    du -sh "$MEDIA_DIR" 2>/dev/null | awk '{print "  Total: " $1}'
else
    echo "  Diretório não encontrado"
fi
echo ""

# Relatórios antigos
RELAT_DIR="$HOME/organizacao/monitoramento/relatorios-diarios"
echo "📝 RELATÓRIOS (>90 dias):"
if [ -d "$RELAT_DIR" ]; then
    find "$RELAT_DIR" -name "*.md" -type f -mtime +90 > "$STAGING_DIR/lista_relatorios.txt" 2>/dev/null
    TOTAL_REL=$(wc -l < "$STAGING_DIR/lista_relatorios.txt" 2>/dev/null || echo 0)
    echo "  $TOTAL_REL arquivos encontrados"
else
    echo "  Diretório não encontrado"
fi
echo ""

# 2. Compactar backups para transferência mais fácil
echo "🗜️  COMPACTANDO BACKUPS..."
BACKUP_TAR="$STAGING_DIR/backups_antigos.tar.gz"
if [ -s "$STAGING_DIR/lista_backups.txt" ]; then
    tar -czf "$BACKUP_TAR" -T "$STAGING_DIR/lista_backups.txt" 2>/dev/null && \
    echo "  ✅ Criado: backups_antigos.tar.gz ($(du -sh "$BACKUP_TAR" | cut -f1))" || \
    echo "  ⚠️ Erro ao compactar"
else
    echo "  Nada para compactar"
fi
echo ""

# 3. Compactar mídia antiga
echo "🗜️  COMPACTANDO MÍDIA..."
MEDIA_TAR="$STAGING_DIR/midia_antiga.tar.gz"
if [ -s "$STAGING_DIR/lista_midia.txt" ] && [ "$TOTAL_MIDIA" -gt 0 ]; then
    tar -czf "$MEDIA_TAR" -T "$STAGING_DIR/lista_midia.txt" 2>/dev/null && \
    echo "  ✅ Criado: midia_antiga.tar.gz ($(du -sh "$MEDIA_TAR" | cut -f1))" || \
    echo "  ⚠️ Erro ao compactar"
else
    echo "  Nada para compactar"
fi
echo ""

# 4. Criar instruções para transferência manual
echo "📋 CRIANDO GUIA DE TRANSFERÊNCIA..."
cat > "$STAGING_DIR/INSTRUCOES_TRANSFERENCIA.md" << 'EOF'
# Instruções para Transferência Manual

## Arquivos Preparados

### 📦 Backups Antigos
- Arquivo: `backups_antigos.tar.gz`
- Transferir para: Google Drive > OpenClaw_Backup > Backups
- Pode ser excluído do local após confirmação

### 🎵 Mídia Antiga
- Arquivo: `midia_antiga.tar.gz`
- Transferir para: Google Drive > OpenClaw_Backup > Media_Historico
- Áudios antigos do WhatsApp/Telegram

### 📝 Relatórios Antigos
- Lista em: `lista_relatorios.txt`
- Transferir para: Google Drive > OpenClaw_Backup > Relatorios

## Como Transferir Manualmente

### Opção 1: Via Navegador (Fácil)
1. Acesse: https://drive.google.com
2. Crie pasta: OpenClaw_Backup
3. Arraste os arquivos .tar.gz
4. Aguarde upload

### Opção 2: Via rclone (Quando instalar)
```bash
# Instalar rclone
sudo apt install rclone

# Configurar
rclone config

# Transferir automaticamente
~/organizacao/scripts/transferir_nuvem.sh
```

### Opção 3: Microsoft OneDrive
1. Acesse: https://onedrive.live.com
2. Upload direto

## Após Transferência

1. ✅ Verifique se arquivos estão na nuvem
2. ✅ Baixe um arquivo de teste para confirmar
3. ✅ Só então exclua os arquivos locais
4. ✅ Libere espaço no computador

## Espaço a ser Liberado

Veja o relatório em: `relatorio_espaco.txt`
EOF

echo "  ✅ Guia criado: INSTRUCOES_TRANSFERENCIA.md"
echo ""

# 5. Relatório de espaço
echo "📊 GERANDO RELATÓRIO DE ESPAÇO..."
cat > "$STAGING_DIR/relatorio_espaco.txt" << EOF
RELATÓRIO DE LIMPEZA - $(date '+%Y-%m-%d %H:%M:%S')
==========================================

ESPAÇO ATUAL:
$(df -h ~ | head -2)

MAIORES PASTAS:
$(du -sh ~/organizacao/*/ 2>/dev/null | sort -rh | head -5)

ARQUIVOS PREPARADOS PARA NUVEM:

1. BACKUPS ANTIGOS:
$(ls -lh "$BACKUP_TAR" 2>/dev/null || echo "   Nenhum")

2. MÍDIA ANTIGA:
$(ls -lh "$MEDIA_TAR" 2>/dev/null || echo "   Nenhum")

3. RELATÓRIOS:
   $(wc -l < "$STAGING_DIR/lista_relatorios.txt" 2>/dev/null || echo 0) arquivos

ESPAÇO QUE SERÁ LIBERADO:
$(du -sh "$STAGING_DIR" 2>/dev/null | awk '{print $1}' || echo "0 bytes")

PRÓXIMOS PASSOS:
1. Transfira os arquivos .tar.gz para Google Drive
2. Verifique se upload foi bem-sucedido
3. Exclua arquivos locais antigos
4. Instale rclone para automação futura

EOF

echo "  ✅ Relatório criado: relatorio_espaco.txt"
echo ""

# Resumo final
echo "=========================================="
echo "  RESUMO DA PREPARAÇÃO"
echo "=========================================="
echo ""
echo "📁 Diretório: $STAGING_DIR"
echo ""
ls -lh "$STAGING_DIR"
echo ""
echo "✅ PRONTO! Arquivos preparados para transferência."
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Acesse: $STAGING_DIR"
echo "2. Leia: INSTRUCOES_TRANSFERENCIA.md"
echo "3. Envie para nuvem (Google Drive, OneDrive, etc.)"
echo "4. Libere espaço local"
echo ""
echo "💡 Quando instalar rclone, use:"
echo "   ~/organizacao/scripts/transferir_nuvem.sh"
echo "=========================================="
