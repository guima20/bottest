#!/bin/bash

# Script para iniciar o Bot Unificado do Telegram
# Combina funcionalidades do bot principal e administrativo

echo "🚀 INICIANDO BOT UNIFICADO DO TELEGRAM..."

# Verifica se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Crie o arquivo .env com as configurações necessárias."
    exit 1
fi

# Verifica se o arquivo config.json existe
if [ ! -f "config.json" ]; then
    echo "❌ Arquivo config.json não encontrado!"
    echo "📝 Crie o arquivo config.json com a configuração inicial."
    exit 1
fi

# Para qualquer instância anterior
echo "🧹 Parando instâncias anteriores..."
pkill -f "python.*bot" 2>/dev/null || true
sleep 2

# Verifica se o Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    exit 1
fi

# Verifica se as dependências estão instaladas
python3 -c "import telegram" 2>/dev/null || {
    echo "❌ Biblioteca python-telegram-bot não encontrada!"
    echo "📦 Instale com: pip install python-telegram-bot"
    exit 1
}

# Inicia o bot unificado
echo "🚀 Iniciando bot unificado..."
python3 unified_bot.py > unified_bot.log 2>&1 &
BOT_PID=$!

# Aguarda um pouco para verificar se iniciou corretamente
sleep 3

# Verifica se o processo está rodando
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Bot unificado iniciado com sucesso!"
    echo "📋 PID: $BOT_PID"
    echo "📄 Logs: unified_bot.log"
    echo ""
    echo "🔧 COMANDOS DISPONÍVEIS:"
    echo "   👥 Para usuários:"
    echo "      /start - Inicia o bot e mostra a mensagem principal"
    echo ""
    echo "   🔐 Para administradores:"
    echo "      /set_image <url> - Alterar imagem"
    echo "      /set_text <texto> - Alterar texto"
    echo "      /set_button <1-4> <texto> <url> - Alterar botão"
    echo "      /show_config - Mostrar configuração atual"
    echo "      /admin_help - Ajuda administrativa"
    echo ""
    echo "📊 Para monitorar: tail -f unified_bot.log"
    echo "🛑 Para parar: pkill -f unified_bot"
else
    echo "❌ Falha ao iniciar o bot!"
    echo "📄 Verifique os logs em unified_bot.log"
    exit 1
fi