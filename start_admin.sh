#!/bin/bash

echo "🔧 INICIANDO BOT ADMINISTRATIVO..."

# Carrega variáveis de ambiente
source .env

# Para instâncias anteriores
echo "🧹 Parando instâncias anteriores..."
pkill -f admin_bot.py 2>/dev/null || true

# Aguarda um momento
sleep 2

# Inicia o bot administrativo
echo "🚀 Iniciando bot administrativo..."
nohup python3 admin_bot.py > admin_bot.log 2>&1 &

# Pega o PID
ADMIN_PID=$!

echo "✅ Bot administrativo iniciado com sucesso!"
echo "📋 PID: $ADMIN_PID"
echo "📄 Logs: admin_bot.log"
echo ""
echo "🔧 COMANDOS DISPONÍVEIS:"
echo "   🔐 Para administradores:"
echo "      /start - Interface administrativa com botões"
echo ""
echo "📊 Para monitorar: tail -f admin_bot.log"
echo "🛑 Para parar: pkill -f admin_bot"