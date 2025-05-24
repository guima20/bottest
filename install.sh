#!/bin/bash

echo "🤖 INSTALADOR DOS BOTS DO TELEGRAM"
echo "=================================="

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale Python3 primeiro."
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"

# Instala dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Verifica se config.json existe
if [ ! -f "config.json" ]; then
    echo "📝 Criando arquivo de configuração padrão..."
    python3 -c "
import json
config = {
    'image': 'https://via.placeholder.com/600x400/0066cc/ffffff?text=Chips+Gratis',
    'text': '👋 Olá! REGISTRE-SE para receber CHIPS GRÁTIS até \$130 👇',
    'buttons': [
        {'text': '👉 Grab Your Free NOW', 'url': 'https://link1.com'},
        {'text': '👉 Discover More FreeChips and GameTips', 'url': 'https://link2.com'},
        {'text': '👉 Add To Group', 'url': 'https://link3.com'},
        {'text': '👉 Join RichGroup', 'url': 'https://link4.com'}
    ]
}
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
"
    echo "✅ Arquivo config.json criado!"
fi

# Torna scripts executáveis
chmod +x *.py

echo ""
echo "🎉 INSTALAÇÃO CONCLUÍDA!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Crie dois bots no @BotFather do Telegram"
echo "2. Configure as variáveis de ambiente:"
echo "   export TELEGRAM_BOT_TOKEN='seu_token_principal'"
echo "   export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_admin'"
echo "   export ADMIN_IDS='seu_id_telegram'"
echo ""
echo "3. Teste a configuração:"
echo "   python3 test_config.py"
echo ""
echo "4. Execute os bots:"
echo "   python3 run_bots.py"
echo ""
echo "📖 Leia o README_TELEGRAM_BOT.md para instruções detalhadas!"