#!/usr/bin/env python3
"""
Executa apenas o bot administrativo
"""

import os
import sys

def main():
    # Verifica se os tokens estão configurados
    if not os.getenv('TELEGRAM_ADMIN_BOT_TOKEN'):
        print("❌ TELEGRAM_ADMIN_BOT_TOKEN não configurado!")
        print("\n🔧 Configure as variáveis de ambiente:")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_do_bot_admin'")
        print("export ADMIN_IDS='123456789,987654321'")
        sys.exit(1)
    
    if not os.getenv('ADMIN_IDS'):
        print("❌ ADMIN_IDS não configurado!")
        print("\n🔧 Configure as variáveis de ambiente:")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_do_bot_admin'")
        print("export ADMIN_IDS='123456789,987654321'")
        sys.exit(1)
    
    # Importa e executa o bot administrativo
    from admin_bot import main as admin_bot
    admin_bot()

if __name__ == '__main__':
    main()