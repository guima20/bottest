#!/bin/bash

echo "🌐 Iniciando Heylink com Cloudflare Tunnel..."
echo "================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar se cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}⚠️  Cloudflared não encontrado. Instalando...${NC}"
    
    # Detectar sistema operacional
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            # Ubuntu/Debian
            wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
            sudo dpkg -i cloudflared-linux-amd64.deb
            rm cloudflared-linux-amd64.deb
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL/Fedora
            wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm
            sudo rpm -i cloudflared-linux-amd64.rpm
            rm cloudflared-linux-amd64.rpm
        else
            echo -e "${RED}❌ Sistema não suportado para instalação automática${NC}"
            echo "Instale manualmente: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
            exit 1
        fi
    else
        echo -e "${RED}❌ Sistema não suportado para instalação automática${NC}"
        echo "Instale manualmente: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Cloudflared instalado com sucesso!${NC}"
else
    echo -e "${GREEN}✅ Cloudflared já está instalado${NC}"
fi

# Verificar versão
CLOUDFLARED_VERSION=$(cloudflared --version 2>/dev/null | head -n1)
echo -e "${BLUE}📦 Versão: $CLOUDFLARED_VERSION${NC}"

# Verificar se Flask está rodando
echo -e "${YELLOW}🔍 Verificando se Flask está rodando...${NC}"
if curl -s http://localhost:8000 > /dev/null; then
    echo -e "${GREEN}✅ Flask já está rodando na porta 8000${NC}"
    FLASK_RUNNING=true
else
    echo -e "${YELLOW}🚀 Iniciando Flask...${NC}"
    
    # Ativar ambiente virtual se existir
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
    fi
    
    # Iniciar Flask em background
    python app.py &
    FLASK_PID=$!
    FLASK_RUNNING=false
    
    # Aguardar Flask iniciar
    echo -e "${YELLOW}⏳ Aguardando Flask inicializar...${NC}"
    for i in {1..10}; do
        if curl -s http://localhost:8000 > /dev/null; then
            echo -e "${GREEN}✅ Flask iniciado com sucesso!${NC}"
            FLASK_RUNNING=true
            break
        fi
        sleep 1
        echo -n "."
    done
    
    if [ "$FLASK_RUNNING" = false ]; then
        echo -e "${RED}❌ Erro ao iniciar Flask${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}📡 Criando túnel Cloudflare...${NC}"
echo -e "${YELLOW}⚠️  Aguarde alguns segundos para o túnel ser criado...${NC}"
echo ""

# Iniciar túnel Cloudflare em background para capturar URL
cloudflared tunnel --url http://localhost:8000 > cloudflare.log 2>&1 &
TUNNEL_PID=$!

# Aguardar URL do túnel
echo -e "${YELLOW}⏳ Aguardando URL do túnel...${NC}"
for i in {1..30}; do
    if [ -f "cloudflare.log" ]; then
        TUNNEL_URL=$(grep -o 'https://[^[:space:]]*\.trycloudflare\.com' cloudflare.log | head -1)
        if [ -n "$TUNNEL_URL" ]; then
            break
        fi
    fi
    sleep 1
    echo -n "."
done

echo ""
if [ -n "$TUNNEL_URL" ]; then
    echo -e "${GREEN}🎉 Túnel criado com sucesso!${NC}"
    echo ""
    echo "================================================"
    echo -e "${BLUE}📱 URLs de Acesso:${NC}"
    echo -e "   Local:      ${YELLOW}http://localhost:8000${NC}"
    echo -e "   Público:    ${GREEN}$TUNNEL_URL${NC}"
    echo -e "   Admin:      ${GREEN}$TUNNEL_URL/admin${NC}"
    echo ""
    echo -e "${BLUE}🔑 Credenciais Admin:${NC}"
    echo -e "   Usuário: ${YELLOW}admin${NC}"
    echo -e "   Senha:   ${YELLOW}admin123${NC}"
    echo ""
    echo -e "${BLUE}📱 Para Telegram Mini App:${NC}"
    echo -e "   Configure no @BotFather:"
    echo -e "   ${YELLOW}/newapp${NC}"
    echo -e "   URL: ${GREEN}$TUNNEL_URL${NC}"
    echo ""
    echo -e "${BLUE}📋 Comandos úteis:${NC}"
    echo -e "   Ver logs Flask:      ${YELLOW}tail -f flask.log${NC}"
    echo -e "   Ver logs Cloudflare: ${YELLOW}tail -f cloudflare.log${NC}"
    echo -e "   Parar sistema:       ${YELLOW}./stop_system.sh${NC}"
    echo "================================================"
    echo ""
    
    # Salvar URL em arquivo
    echo "$TUNNEL_URL" > tunnel_url.txt
    echo -e "${GREEN}💾 URL salva em: tunnel_url.txt${NC}"
    echo ""
    echo -e "${YELLOW}✅ Sistema rodando! Pressione Ctrl+C para parar${NC}"
    
    # Aguardar sinal de interrupção
    trap "echo -e '\n${YELLOW}🛑 Parando sistema...${NC}'; kill $TUNNEL_PID 2>/dev/null; [ ! -z '$FLASK_PID' ] && kill $FLASK_PID 2>/dev/null; exit 0" INT TERM
    
    # Manter script rodando
    wait $TUNNEL_PID
else
    echo -e "${RED}❌ Erro: Não foi possível obter URL do túnel${NC}"
    echo -e "${YELLOW}📋 Verifique os logs: tail cloudflare.log${NC}"
    kill $TUNNEL_PID 2>/dev/null
    [ ! -z "$FLASK_PID" ] && kill $FLASK_PID 2>/dev/null
    exit 1
fi