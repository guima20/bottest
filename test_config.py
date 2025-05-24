#!/usr/bin/env python3
"""
Script de teste para verificar a configuração dos bots
"""

import json
import os
import sys
from pathlib import Path

# Carrega variáveis do arquivo .env se existir
def load_env():
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

def test_config_file():
    """Testa se o arquivo de configuração está válido"""
    print("🔍 Testando arquivo config.json...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verifica campos obrigatórios
        required_fields = ['image', 'text', 'buttons']
        for field in required_fields:
            if field not in config:
                print(f"❌ Campo '{field}' não encontrado no config.json")
                return False
        
        # Verifica botões
        buttons = config.get('buttons', [])
        if len(buttons) != 4:
            print(f"❌ Esperado 4 botões, encontrado {len(buttons)}")
            return False
        
        for i, button in enumerate(buttons, 1):
            if 'text' not in button or 'url' not in button:
                print(f"❌ Botão {i} está mal formatado")
                return False
        
        print("✅ Arquivo config.json está válido")
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo config.json não encontrado")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erro no JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_environment():
    """Testa se as variáveis de ambiente estão configuradas"""
    print("\n🔍 Testando variáveis de ambiente...")
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_ADMIN_BOT_TOKEN',
        'ADMIN_IDS'
    ]
    
    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"❌ Variável {var} não configurada")
            all_ok = False
        else:
            # Mostra apenas os primeiros e últimos caracteres do token
            if 'TOKEN' in var:
                masked = value[:10] + '...' + value[-10:] if len(value) > 20 else value
                print(f"✅ {var}: {masked}")
            else:
                print(f"✅ {var}: {value}")
    
    return all_ok

def test_imports():
    """Testa se as dependências estão instaladas"""
    print("\n🔍 Testando dependências...")
    
    try:
        import telegram
        print(f"✅ python-telegram-bot: {telegram.__version__}")
    except ImportError:
        print("❌ python-telegram-bot não instalado")
        print("   Execute: pip install python-telegram-bot")
        return False
    
    try:
        import json
        print("✅ json: módulo padrão")
    except ImportError:
        print("❌ json não disponível")
        return False
    
    return True

def show_config():
    """Mostra a configuração atual"""
    print("\n📋 Configuração atual:")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📸 Imagem: {config.get('image', 'Não definida')}")
        
        text = config.get('text', 'Não definido')
        if len(text) > 50:
            text = text[:50] + "..."
        print(f"📝 Texto: {text}")
        
        print("🔘 Botões:")
        for i, button in enumerate(config.get('buttons', []), 1):
            print(f"   {i}. {button.get('text', 'Sem texto')} → {button.get('url', 'Sem URL')}")
    
    except Exception as e:
        print(f"❌ Erro ao ler configuração: {e}")

def main():
    """Função principal do teste"""
    print("🧪 TESTE DE CONFIGURAÇÃO DOS BOTS DO TELEGRAM")
    print("=" * 50)
    
    # Testa imports
    if not test_imports():
        print("\n❌ Falha nos imports. Instale as dependências primeiro.")
        sys.exit(1)
    
    # Testa arquivo de configuração
    if not test_config_file():
        print("\n❌ Falha na configuração. Verifique o arquivo config.json.")
        sys.exit(1)
    
    # Testa variáveis de ambiente
    if not test_environment():
        print("\n❌ Falha nas variáveis de ambiente.")
        print("\n🔧 Configure as variáveis:")
        print("export TELEGRAM_BOT_TOKEN='seu_token_aqui'")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_admin_aqui'")
        print("export ADMIN_IDS='123456789,987654321'")
        sys.exit(1)
    
    # Mostra configuração
    show_config()
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("🚀 Você pode executar os bots com:")
    print("   python run_bots.py")
    print("   ou")
    print("   python run_main_bot.py")
    print("   python run_admin_bot.py")

if __name__ == '__main__':
    main()