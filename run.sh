#!/bin/bash

# Script para executar o Heylink

echo "🚀 Iniciando Heylink..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p static/uploads

# Executar aplicação
echo "🌐 Iniciando servidor..."
echo "📱 Acesse: http://localhost:12000"
echo "🔐 Painel Admin: http://localhost:12000/admin (senha: admin123)"
echo ""
echo "Para parar o servidor, pressione Ctrl+C"
echo ""

python app.py