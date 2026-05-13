#!/usr/bin/env python3
"""
Sistema de integração com o Discord para o sistema jurídico automatizado
"""

import os
import json
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
import subprocess
import sys

class SistemaJuridicoDiscord(commands.Cog):
    """
    Cog para integração do sistema jurídico automatizado com o Discord
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.pasta_advocacia = os.path.expanduser("~/organizacao/advocacia")
        self.pasta_servidor_publico = os.path.expanduser("~/organizacao/servidor-publico")
        self.pasta_controle = os.path.expanduser("~/organizacao/controle-prazos")
    
    @commands.command(name='status')
    async def status_sistema(self, ctx):
        """
        Mostra o status do sistema jurídico automatizado
        """
        try:
            embed = discord.Embed(
                title="📊 Status do Sistema Jurídico Automatizado",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )
            
            # Contar processos
            total_processos = self.contar_processos()
            embed.add_field(name="Processos Ativos", value=str(total_processos), inline=True)
            
            # Contar lembretes para hoje
            lembretes_hoje = len(self.obter_lembretes_hoje())
            embed.add_field(name="Lembretes para Hoje", value=str(lembretes_hoje), inline=True)
            
            # Contar novas anotações
            anotacoes_recentes = len(self.obter_anotacoes_recentes())
            embed.add_field(name="Anotações Recentes", value=str(anotacoes_recentes), inline=True)
            
            embed.set_footer(text=f"Solicitado por {ctx.author.name}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Erro ao obter status: {str(e)}")
    
    @commands.command(name='processos')
    async def listar_processos(self, ctx, tipo: str = "todos"):
        """
        Lista os processos do sistema
        """
        try:
            processos = self.obter_lista_processos(tipo)
            
            embed = discord.Embed(
                title=f"📋 Processos ({tipo})",
                color=0x00aaff,
                timestamp=datetime.utcnow()
            )
            
            if processos:
                for i, processo in enumerate(processos[:10]):  # Limitar a 10 por mensagem
                    embed.add_field(
                        name=f"Processo {i+1}",
                        value=processo,
                        inline=False
                    )
            else:
                embed.add_field(
                    name="Nenhum processo encontrado",
                    value=f"Não há processos do tipo '{tipo}'",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Erro ao listar processos: {str(e)}")
    
    @commands.command(name='lembretes')
    async def listar_lembretes(self, ctx, dias: int = 1):
        """
        Lista os lembretes para os próximos dias
        """
        try:
            lembretes = self.obter_lembretes_proximos(dias)
            
            embed = discord.Embed(
                title=f"⏰ Lembretes ({dias} dia{'s' if dias > 1 else ''})",
                color=0xffaa00,
                timestamp=datetime.utcnow()
            )
            
            if lembretes:
                for i, lembrete in enumerate(lembretes[:10]):  # Limitar a 10 por mensagem
                    embed.add_field(
                        name=f"Lembrete {i+1}",
                        value=f"**{lembrete['descricao']}**\nData: {lembrete['data']}\nProcesso: {lembrete['processo']}",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="Nenhum lembrete encontrado",
                    value=f"Não há lembretes para os próximos {dias} dia{'s' if dias > 1 else ''}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Erro ao listar lembretes: {str(e)}")
    
    def contar_processos(self):
        """Conta o total de processos ativos"""
        total = 0
        for pasta_base in [self.pasta_advocacia, self.pasta_servidor_publico]:
            if os.path.exists(pasta_base):
                for pasta_nome in os.listdir(pasta_base):
                    processo_path = os.path.join(pasta_base, pasta_nome)
                    if os.path.isdir(processo_path):
                        total += 1
        return total
    
    def obter_lembretes_hoje(self):
        """Obtém lembretes para hoje"""
        # Importar função do sistema de lembretes
        try:
            sys.path.append(self.pasta_controle)
            from sistema_lembretes import verificar_lembretes_hoje
            return verificar_lembretes_hoje()
        except ImportError:
            return []
    
    def obter_anotacoes_recentes(self, dias=1):
        """Obtém anotações recentes"""
        anotacoes = []
        data_limite = datetime.now() - timedelta(days=dias)
        
        for pasta_base in [self.pasta_advocacia, self.pasta_servidor_publico]:
            if os.path.exists(pasta_base):
                for pasta_nome in os.listdir(pasta_base):
                    processo_path = os.path.join(pasta_base, pasta_nome)
                    if os.path.isdir(processo_path):
                        anotacoes_dir = os.path.join(processo_path, "anotacoes")
                        if os.path.exists(anotacoes_dir):
                            for anotacao_nome in os.listdir(anotacoes_dir):
                                anotacao_path = os.path.join(anotacoes_dir, anotacao_nome)
                                data_modificacao = datetime.fromtimestamp(os.path.getmtime(anotacao_path))
                                if data_modificacao >= data_limite:
                                    anotacoes.append({
                                        "processo": pasta_nome,
                                        "anotacao": anotacao_nome,
                                        "data": data_modificacao.strftime("%d/%m/%Y %H:%M")
                                    })
        
        return anotacoes
    
    def obter_lista_processos(self, tipo="todos"):
        """Obtém lista de processos"""
        processos = []
        
        pastas_base = []
        if tipo.lower() in ["advocacia", "todos"]:
            pastas_base.append(self.pasta_advocacia)
        if tipo.lower() in ["servidor", "publico", "todos"]:
            pastas_base.append(self.pasta_servidor_publico)
        
        for pasta_base in pastas_base:
            if os.path.exists(pasta_base):
                for pasta_nome in os.listdir(pasta_base):
                    processo_path = os.path.join(pasta_base, pasta_nome)
                    if os.path.isdir(processo_path):
                        processos.append(pasta_nome)
        
        return processos
    
    def obter_lembretes_proximos(self, dias=1):
        """Obtém lembretes para os próximos dias"""
        try:
            sys.path.append(self.pasta_controle)
            from sistema_lembretes import verificar_lembretes_futuros
            return verificar_lembretes_futuros(dias)
        except ImportError:
            return []

def setup(bot):
    """Configura o cog no bot do Discord"""
    bot.add_cog(SistemaJuridicoDiscord(bot))

# Função para iniciar o bot do Discord
def iniciar_bot_discord(token):
    """
    Inicia o bot do Discord com integração ao sistema jurídico
    """
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f'{bot.user} conectado ao Discord!')
        print(f'Bot está em {len(bot.guilds)} servidores')
        print(f'Pronto para integrar com o sistema jurídico automatizado')
    
    # Adiciona o cog de integração jurídica
    setup(bot)
    
    # Inicia o bot
    bot.run(token)

if __name__ == "__main__":
    print("Configuração para integração com o Discord")
    print("Para usar, siga estes passos:")
    print("1. Crie um bot no Discord Developer Portal")
    print("2. Adicione o token do bot abaixo:")
    print("3. Execute: python integracao_discord.py <token_do_bot>")
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
        iniciar_bot_discord(token)