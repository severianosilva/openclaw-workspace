#!/bin/bash
# Instalar 10 skills essenciais para sistema jurídico

echo "🔧 Instalando skills essenciais para advocacia..."
echo "================================================"

# Criar diretório de skills se não existir
mkdir -p ~/.openclaw/skills

# Lista de skills essenciais (prioridade alta para advocacia)
SKILLS=(
    "pdf-analyzer"           # Análise automática de PDFs jurídicos
    "document-extractor"     # Extração de texto e metadados
    "contract-analyzer"      # Análise de contratos
    "web-research-assistant" # Pesquisa jurídica na web
    "jurisprudence-search"   # Busca de jurisprudência
    "legal-precedents"       # Análise de precedentes
    "browser-automation"     # Automação de consultas
    "deadline-manager"       # Gerenciamento de prazos
    "knowledge-base"         # Base de conhecimento jurídico
    "ocr-processor"          # OCR para documentos
)

echo "📝 Skills a serem instalados:"
for i in "${!SKILLS[@]}"; do
    echo "  $((i+1)). ${SKILLS[$i]}"
done

echo ""
echo "⚠️  IMPORTANTE:"
echo "Existem 3 formas de instalar:"
echo ""
echo "1. Via ClawHub CLI (recomendado):"
echo "   clawhub install <nome-do-skill>"
echo ""
echo "2. Via npx (sem instalar globalmente):"
echo "   npx clawhub@latest install <nome-do-skill>"
echo ""
echo "3. Manual (download direto):"
echo "   git clone https://github.com/openclaw/skills"
echo "   Copiar pasta para ~/.openclaw/skills/"
echo ""
echo "❓ Você tem o ClawHub CLI instalado? (sim/não)"
echo ""
echo "Para instalar o ClawHub:"
echo "   npm install -g @openclaw/clawhub"
echo "ou"
echo "   npm install -g clawhub"
