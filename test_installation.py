#!/usr/bin/env python3
"""
Script de teste para verificar se a instalação está funcionando corretamente.
"""

import sys
import os
import json

def test_imports():
    """Testa se todas as dependências estão instaladas."""
    print("🔍 Testando importações...")
    
    try:
        import telegram
        print("✅ python-telegram-bot: OK")
    except ImportError:
        print("❌ python-telegram-bot: ERRO")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv: OK")
    except ImportError:
        print("❌ python-dotenv: ERRO")
        return False
    
    try:
        import tkinter
        print("✅ tkinter: OK")
    except ImportError:
        print("❌ tkinter: ERRO (pode não estar disponível em alguns sistemas)")
        return False
    
    return True

def test_files():
    """Testa se todos os arquivos necessários existem."""
    print("\n📁 Testando arquivos...")
    
    required_files = [
        'unified_bot.py',
        'admin_bot.py',
        'bot_messages.py',
        'gui_manager.py',
        'config.json',
        'groups.json',
        'pending_messages.json',
        '.env',
        'requirements.txt'
    ]
    
    all_files_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: OK")
        else:
            print(f"❌ {file}: ERRO - Arquivo não encontrado")
            all_files_exist = False
    
    return all_files_exist

def test_json_files():
    """Testa se os arquivos JSON são válidos."""
    print("\n📄 Testando arquivos JSON...")
    
    json_files = ['config.json', 'groups.json', 'pending_messages.json']
    all_valid = True
    
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ {file}: JSON válido")
        except json.JSONDecodeError as e:
            print(f"❌ {file}: JSON inválido - {e}")
            all_valid = False
        except FileNotFoundError:
            print(f"❌ {file}: Arquivo não encontrado")
            all_valid = False
    
    return all_valid

def test_env_file():
    """Testa se o arquivo .env tem as variáveis necessárias."""
    print("\n🔧 Testando arquivo .env...")
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_ADMIN_BOT_TOKEN',
        'ADMIN_IDS'
    ]
    
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
        
        all_vars_present = True
        for var in required_vars:
            if var in env_content:
                print(f"✅ {var}: Presente")
            else:
                print(f"❌ {var}: Ausente")
                all_vars_present = False
        
        return all_vars_present
        
    except FileNotFoundError:
        print("❌ Arquivo .env não encontrado")
        return False

def test_bot_modules():
    """Testa se os módulos dos bots podem ser importados."""
    print("\n🤖 Testando módulos dos bots...")
    
    try:
        import bot_messages
        print("✅ bot_messages: Importado com sucesso")
    except ImportError as e:
        print(f"❌ bot_messages: Erro na importação - {e}")
        return False
    
    # Testa funções principais
    try:
        from bot_messages import load_pending_messages, add_pending_message
        print("✅ Funções do bot_messages: OK")
    except ImportError as e:
        print(f"❌ Funções do bot_messages: Erro - {e}")
        return False
    
    return True

def main():
    """Função principal do teste."""
    print("🧪 TESTE DE INSTALAÇÃO - Sistema de Bots Telegram Kangaroo")
    print("=" * 60)
    
    # Executa todos os testes
    tests = [
        ("Importações", test_imports),
        ("Arquivos", test_files),
        ("Arquivos JSON", test_json_files),
        ("Arquivo .env", test_env_file),
        ("Módulos dos Bots", test_bot_modules)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro durante o teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O sistema está pronto para uso.")
        print("\nPara iniciar:")
        print("1. Configure seus tokens no arquivo .env")
        print("2. Execute: python start_gui.py")
    else:
        print(f"\n⚠️ {total - passed} TESTE(S) FALHARAM!")
        print("Verifique os erros acima antes de continuar.")
        print("\nPara resolver:")
        print("1. Instale as dependências: pip install -r requirements.txt")
        print("2. Verifique se todos os arquivos estão presentes")
        print("3. Configure o arquivo .env corretamente")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)