#!/bin/bash

# 🛑 Script para parar Sistema Heylink
# Autor: OpenHands AI
# Data: 24/05/2025

echo "🛑 Parando Sistema Heylink..."
echo "================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parar processos Flask
echo -e "${YELLOW}🐍 Parando Flask...${NC}"
FLASK_PIDS=$(pgrep -f "python.*app.py")
if [ -n "$FLASK_PIDS" ]; then
    echo "$FLASK_PIDS" | xargs kill 2>/dev/null
    sleep 2
    # Force kill se necessário
    FLASK_PIDS=$(pgrep -f "python.*app.py")
    if [ -n "$FLASK_PIDS" ]; then
        echo "$FLASK_PIDS" | xargs kill -9 2>/dev/null
    fi
    echo -e "${GREEN}✅ Flask parado${NC}"
else
    echo -e "${YELLOW}⚠️  Flask não estava rodando${NC}"
fi

# Parar processos Cloudflare Tunnel
echo -e "${YELLOW}🌐 Parando Cloudflare Tunnel...${NC}"
TUNNEL_PIDS=$(pgrep -f "cloudflared.*tunnel")
if [ -n "$TUNNEL_PIDS" ]; then
    echo "$TUNNEL_PIDS" | xargs kill 2>/dev/null
    sleep 2
    # Force kill se necessário
    TUNNEL_PIDS=$(pgrep -f "cloudflared.*tunnel")
    if [ -n "$TUNNEL_PIDS" ]; then
        echo "$TUNNEL_PIDS" | xargs kill -9 2>/dev/null
    fi
    echo -e "${GREEN}✅ Cloudflare Tunnel parado${NC}"
else
    echo -e "${YELLOW}⚠️  Cloudflare Tunnel não estava rodando${NC}"
fi

# Parar servidor proxy (se estiver rodando)
echo -e "${YELLOW}🔄 Parando servidor proxy...${NC}"
PROXY_PIDS=$(pgrep -f "python.*proxy_server.py")
if [ -n "$PROXY_PIDS" ]; then
    echo "$PROXY_PIDS" | xargs kill 2>/dev/null
    sleep 2
    # Force kill se necessário
    PROXY_PIDS=$(pgrep -f "python.*proxy_server.py")
    if [ -n "$PROXY_PIDS" ]; then
        echo "$PROXY_PIDS" | xargs kill -9 2>/dev/null
    fi
    echo -e "${GREEN}✅ Servidor proxy parado${NC}"
else
    echo -e "${YELLOW}⚠️  Servidor proxy não estava rodando${NC}"
fi

# Verificar se ainda há processos rodando
echo -e "${YELLOW}🔍 Verificando processos restantes...${NC}"
REMAINING=$(pgrep -f "(python.*app.py|cloudflared.*tunnel|python.*proxy_server.py)")
if [ -n "$REMAINING" ]; then
    echo -e "${RED}⚠️  Alguns processos ainda estão rodando:${NC}"
    ps aux | grep -E "(python.*app.py|cloudflared.*tunnel|python.*proxy_server.py)" | grep -v grep
else
    echo -e "${GREEN}✅ Todos os processos foram parados${NC}"
fi

# Limpar arquivos temporários
echo -e "${YELLOW}🧹 Limpando arquivos temporários...${NC}"
[ -f "tunnel_url.txt" ] && rm tunnel_url.txt && echo -e "${GREEN}✅ tunnel_url.txt removido${NC}"

echo ""
echo -e "${GREEN}🎉 Sistema Heylink parado com sucesso!${NC}"
echo ""
echo -e "${YELLOW}📋 Para iniciar novamente:${NC}"
echo -e "   Cloudflare Tunnel: ${GREEN}./start_cloudflare.sh${NC}"
echo -e "   Acesso externo:    ${GREEN}./start_external.sh${NC}"
echo -e "   Local apenas:      ${GREEN}./run.sh${NC}"
echo ""