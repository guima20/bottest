#!/bin/bash

# 🚀 Script para iniciar o Sistema Heylink com acesso externo HTTPS
# Autor: OpenHands AI
# Data: 2025-05-24

echo "🚀 Iniciando Sistema Heylink..."
echo "📍 Diretório: $(pwd)"

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se Flask está instalado
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install flask requests
fi

# Parar processos anteriores se existirem
echo "🛑 Parando processos anteriores..."
pkill -f "python app.py" 2>/dev/null || true
pkill -f "python proxy_server.py" 2>/dev/null || true

# Aguardar um momento para os processos terminarem
sleep 2

# Iniciar aplicação Flask na porta 8000
echo "🌐 Iniciando aplicação Flask na porta 8000..."
python app.py &
FLASK_PID=$!

# Aguardar Flask inicializar
sleep 3

# Verificar se Flask está rodando
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "❌ Erro: Flask não conseguiu iniciar na porta 8000"
    exit 1
fi

echo "✅ Flask rodando na porta 8000"

# Iniciar proxy para acesso externo
echo "🔗 Iniciando proxy para acesso externo..."
python proxy_server.py &
PROXY_PID=$!

# Aguardar proxy inicializar
sleep 3

# Verificar se proxy está rodando
PROXY_PORT=$(netstat -tlnp 2>/dev/null | grep python | grep -E ":(9000|9001|8080|8081)" | head -1 | sed 's/.*:\([0-9]*\).*/\1/')

if [ -z "$PROXY_PORT" ]; then
    echo "❌ Erro: Proxy não conseguiu iniciar"
    kill $FLASK_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Proxy rodando na porta $PROXY_PORT"

# Informações de acesso
echo ""
echo "🎉 Sistema Heylink iniciado com sucesso!"
echo ""
echo "📱 Acesso Local:"
echo "   http://localhost:8000"
echo "   http://localhost:$PROXY_PORT"
echo ""
echo "🌍 Acesso Externo HTTPS:"
echo "   https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev (porta 12000)"
echo "   https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev (porta 12001)"
echo ""
echo "🔧 Painel Administrativo:"
echo "   http://localhost:$PROXY_PORT/admin"
echo "   Senha: admin123"
echo ""
echo "📊 Status dos Processos:"
echo "   Flask PID: $FLASK_PID"
echo "   Proxy PID: $PROXY_PID"
echo ""
echo "🛑 Para parar o sistema:"
echo "   kill $FLASK_PID $PROXY_PID"
echo "   ou execute: ./stop_system.sh"
echo ""

# Criar script de parada
cat > stop_system.sh << 'EOF'
#!/bin/bash
echo "🛑 Parando Sistema Heylink..."
pkill -f "python app.py"
pkill -f "python proxy_server.py"
echo "✅ Sistema parado!"
EOF

chmod +x stop_system.sh

# Manter o script rodando para monitorar
echo "🔍 Monitorando sistema... (Ctrl+C para parar)"
echo ""

# Função para cleanup ao sair
cleanup() {
    echo ""
    echo "🛑 Parando sistema..."
    kill $FLASK_PID $PROXY_PID 2>/dev/null || true
    echo "✅ Sistema parado!"
    exit 0
}

# Capturar sinais de interrupção
trap cleanup SIGINT SIGTERM

# Loop de monitoramento
while true; do
    # Verificar se Flask ainda está rodando
    if ! kill -0 $FLASK_PID 2>/dev/null; then
        echo "❌ Flask parou de funcionar!"
        break
    fi
    
    # Verificar se Proxy ainda está rodando
    if ! kill -0 $PROXY_PID 2>/dev/null; then
        echo "❌ Proxy parou de funcionar!"
        break
    fi
    
    sleep 10
done

cleanup