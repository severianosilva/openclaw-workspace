#!/bin/bash
###############################################################################
# Demonstração do Sistema de Automação YouTube
# Executa pesquisa de tendências e geração de roteiro
###############################################################################

echo "======================================================================"
echo "  SISTEMA DE AUTOMAÇÃO YOUTUBE 2026"
echo "  Demonstração Completa"
echo "======================================================================"
echo ""

# Definir nicho de exemplo
NICHO="financas"
TITULO_EXEMPLO="Como Começar a Investir com Pouco Dinheiro"

echo "📋 CONFIGURAÇÃO DA DEMONSTRAÇÃO"
echo "  Nicho: $NICHO"
echo "  Título de exemplo: $TITULO_EXEMPLO"
echo ""

# Passo 1: Pesquisa de Tendências
echo "======================================================================"
echo "  PASSO 1: PESQUISA DE TENDÊNCIAS"
echo "======================================================================"
echo ""

cd ~/organizacao/youtube
python3 pesquisa_tendencias_youtube.py $NICHO

echo ""
echo "⏳ Aguarde 2 segundos..."
sleep 2
echo ""

# Passo 2: Gerar Roteiro
echo "======================================================================"
echo "  PASSO 2: GERAR ROTEIRO OTIMIZADO"
echo "======================================================================"
echo ""

python3 gerar_roteiro_youtube.py "$TITULO_EXEMPLO" $NICHO

echo ""
echo "⏳ Aguarde 2 segundos..."
sleep 2
echo ""

# Passo 3: Mostrar Resultados
echo "======================================================================"
echo "  PASSO 3: RESULTADOS GERADOS"
echo "======================================================================"
echo ""

echo "📁 ARQUIVOS CRIADOS:"
echo ""

# Listar arquivos de pesquisa
echo "  📊 Relatórios de Pesquisa:"
ls -lh ~/organizacao/youtube/pesquisa/*.json 2>/dev/null | head -3 | while read line; do
    echo "     $line"
done

echo ""
echo "  📝 Roteiros Gerados:"
ls -lh ~/organizacao/youtube/roteiros/*.json 2>/dev/null | head -3 | while read line; do
    echo "     $line"
done

echo ""
echo "======================================================================"
echo "  PRÓXIMOS PASSOS"
echo "======================================================================"
echo ""
echo "1. Review o relatório de pesquisa:"
echo "   cat ~/organizacao/youtube/pesquisa/relatorio_*.json | python3 -m json.tool"
echo ""
echo "2. Review o roteiro completo:"
echo "   cat ~/organizacao/youtube/roteiros/roteiro_*.json | python3 -m json.tool"
echo ""
echo "3. Produza o vídeo:"
echo "   - Use o roteiro como guia"
echo "   - Grave áudio (ou use TTS)"
echo "   - Edite no DaVinci Resolve"
echo "   - Crie thumbnail no Canva"
echo ""
echo "4. Publique com metadata otimizada:"
echo "   - Use título, tags e descrição do roteiro"
echo "   - Agende no YouTube Studio"
echo ""
echo "======================================================================"
echo "  SISTEMA PRONTO PARA USO!"
echo "======================================================================"
echo ""
echo "📖 Guia completo: ~/organizacao/youtube/GUIA_COMPLETO_YOUTUBE.md"
echo "📚 Pesquisa completa: ~/organizacao/youtube/research_youtube_growth_2025.md"
echo ""
