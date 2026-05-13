#!/bin/bash
# Script de Gerenciamento de Modelos de IA
# Troca automática quando atinge limites

SCRIPT_DIR="/home/severosa/organizacao/configuracao"
PYTHON_SCRIPT="$SCRIPT_DIR/gerencia_modelos_ia.py"

echo "============================================================"
echo "GERENCIADOR DE MODELOS DE IA - OPENCLAW"
echo "============================================================"
echo ""

case "$1" in
    status)
        echo "📊 STATUS ATUAL DOS MODELOS"
        echo ""
        python3 "$PYTHON_SCRIPT" status
        ;;
    
    uso)
        MODELO="${2:-auto}"
        echo "📝 Registrando uso do modelo: $MODELO"
        python3 "$PYTHON_SCRIPT" uso "$MODELO"
        ;;
    
    trocar)
        MOTIVO="${2:-manual}"
        echo "🔄 Trocando modelo (motivo: $MOTIVO)..."
        python3 "$PYTHON_SCRIPT" trocar "$MOTIVO"
        ;;
    
    limite)
        MODELO="$2"
        NOVO_LIMITE="$3"
        if [ -z "$MODELO" ] || [ -z "$NOVO_LIMITE" ]; then
            echo "Uso: $0 limite <modelo> <novo_limite>"
            exit 1
        fi
        echo "⚙️  Configurando limite: $MODELO = $NOVO_LIMITE"
        python3 "$PYTHON_SCRIPT" limite "$MODELO" "$NOVO_LIMITE"
        ;;
    
    reset)
        echo "🔄 Resetando contagens..."
        python3 "$PYTHON_SCRIPT" reset
        ;;
    
    auto)
        echo "🤖 MODO AUTOMÁTICO ATIVADO"
        echo "Verificando limites e trocando modelos se necessário..."
        python3 "$PYTHON_SCRIPT" status
        python3 "$PYTHON_SCRIPT" verificar
        ;;
    
    ajuda|help|--help|-h|"")
        echo "Uso: $0 <comando> [opções]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  status                    - Mostrar status de todos os modelos"
        echo "  uso [modelo]              - Registrar uso (padrão: modelo atual)"
        echo "  trocar [motivo]           - Trocar modelo manualmente"
        echo "  limite <modelo> <limite>  - Configurar limite de uso"
        echo "  reset                     - Resetar todas as contagens"
        echo "  auto                      - Verificar e trocar automaticamente"
        echo "  ajuda                     - Mostrar esta ajuda"
        echo ""
        echo "Exemplos:"
        echo "  $0 status"
        echo "  $0 uso qwen-portal/coder-model"
        echo "  $0 trocar limite_atingido"
        echo "  $0 limite openrouter/auto 500"
        echo "  $0 reset"
        echo ""
        echo "============================================================"
        ;;
    
    *)
        echo "❌ Comando desconhecido: $1"
        echo "Use '$0 ajuda' para ver comandos disponíveis"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
