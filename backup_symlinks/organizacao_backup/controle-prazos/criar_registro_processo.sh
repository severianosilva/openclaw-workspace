#!/bin/bash

# Script para criar registro de novo processo
echo "=== Criação de Registro de Processo ==="
echo
echo "Digite o número do processo ou nome do cliente:"
read processo_nome

# Criar pasta para o novo processo
mkdir -p "$HOME/organizacao/advocacia/ativos/$processo_nome"
mkdir -p "$HOME/organizacao/advocacia/ativos/$processo_nome/documentos"
mkdir -p "$HOME/organizacao/advocacia/ativos/$processo_nome/andamentos"
mkdir -p "$HOME/organizacao/advocacia/ativos/$processo_nome/anotacoes"

# Copiar modelos de anotações
mkdir -p "$HOME/organizacao/controle-prazos/modelos-anotacoes"
cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-analise-inicial.md" "$HOME/organizacao/advocacia/ativos/$processo_nome/anotacoes/analise_inicial.md" 2>/dev/null
cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-estrategia-defesa.md" "$HOME/organizacao/advocacia/ativos/$processo_nome/anotacoes/estrategia_defesa.md" 2>/dev/null
cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-pesquisa-juridica.md" "$HOME/organizacao/advocacia/ativos/$processo_nome/anotacoes/notas_pesquisa_juridica.md" 2>/dev/null
cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-rascunho-peca.md" "$HOME/organizacao/advocacia/ativos/$processo_nome/anotacoes/rascunhos_peca.md" 2>/dev/null

# Copiar modelo para o novo processo
cp "$HOME/organizacao/controle-prazos/modelo-controle-processos.md" "$HOME/organizacao/advocacia/ativos/$processo_nome/controle-processo.md"

echo
echo "Registro criado em: $HOME/organizacao/advocacia/ativos/$processo_nome/"
echo "Arquivo de controle criado: controle-processo.md"
echo "Pastas adicionais criadas: documentos, andamentos e anotacoes"
echo "Modelos de anotações criados na pasta 'anotacoes'"

# Se for processo de servidor público, perguntar
echo
echo "Este processo é relacionado à sua função como servidor público? (s/n)"
read servidor_resp

if [ "$servidor_resp" = "s" ] || [ "$servidor_resp" = "S" ]; then
    mkdir -p "$HOME/organizacao/servidor-publico/ativos/$processo_nome"
    mkdir -p "$HOME/organizacao/servidor-publico/ativos/$processo_nome/documentos"
    mkdir -p "$HOME/organizacao/servidor-publico/ativos/$processo_nome/andamentos"
    mkdir -p "$HOME/organizacao/servidor-publico/ativos/$processo_nome/anotacoes"
    cp "$HOME/organizacao/controle-prazos/modelo-controle-processos.md" "$HOME/organizacao/servidor-publico/ativos/$processo_nome/controle-processo.md"
    cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-analise-inicial.md" "$HOME/organizacao/servidor-publico/ativos/$processo_nome/anotacoes/analise_inicial.md" 2>/dev/null
    cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-estrategia-defesa.md" "$HOME/organizacao/servidor-publico/ativos/$processo_nome/anotacoes/estrategia_defesa.md" 2>/dev/null
    cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-pesquisa-juridica.md" "$HOME/organizacao/servidor-publico/ativos/$processo_nome/anotacoes/notas_pesquisa_juridica.md" 2>/dev/null
    cp "$HOME/organizacao/controle-prazos/modelos-anotacoes/modelo-rascunho-peca.md" "$HOME/organizacao/servidor-publico/ativos/$processo_nome/anotacoes/rascunhos_peca.md" 2>/dev/null
    echo "Registro também criado em: $HOME/organizacao/servidor-publico/ativos/$processo_nome/"
    echo "Pastas adicionais criadas: documentos, andamentos e anotacoes"
fi

echo
echo "=== Processo registrado com sucesso! ==="