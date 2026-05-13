// Script para manter a conexão do OpenClaw ativa evitando inatividade
// Este script pode ser usado como um bookmarklet ou injectado em uma página HTML

(function() {
    // Função para enviar uma requisição de "heartbeat" para manter a conexão ativa
    async function manterConexaoAtiva() {
        try {
            // Verificar se ainda estamos conectados ao gateway WebSocket
            if (window.gatewaySocket && window.gatewaySocket.readyState === WebSocket.OPEN) {
                // Enviar uma mensagem de "ping" para manter a conexão ativa
                const pingMessage = {
                    type: "ping",
                    timestamp: Date.now()
                };
                window.gatewaySocket.send(JSON.stringify(pingMessage));
                console.log("Ping enviado para manter conexão ativa:", new Date().toISOString());
            } else {
                console.log("WebSocket não está aberto, tentando reconectar...");
                // Aqui você pode implementar lógica de reconexão se necessário
            }
        } catch (error) {
            console.error("Erro ao tentar manter conexão ativa:", error);
        }
    }

    // Função para verificar periodicamente o estado da conexão
    function iniciarManutencaoConexao() {
        // Executar imediatamente
        manterConexaoAtiva();
        
        // Executar a cada 5 minutos (300000 ms) para manter a conexão ativa
        setInterval(manterConexaoAtiva, 300000); // 5 minutos
    }

    // Iniciar a manutenção da conexão
    iniciarManutencaoConexao();

    // Também adicionar um listener para quando a página ganha foco novamente
    window.addEventListener('focus', function() {
        manterConexaoAtiva();
    });

    // Adicionar um listener para quando o usuário interage com a página
    ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, function() {
            manterConexaoAtiva();
        }, { passive: true });
    });

    console.log("Sistema de manutenção de conexão ativado. A conexão será mantida ativa a cada 5 minutos.");
})();