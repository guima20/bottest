#!/usr/bin/env python3
"""
Executa apenas o bot principal
"""

import os
import sys

def main():
    # Verifica se o token está configurado
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ TELEGRAM_BOT_TOKEN não configurado!")
        print("\n🔧 Configure a variável de ambiente:")
        print("export TELEGRAM_BOT_TOKEN='seu_token_do_bot_principal'")
        sys.exit(1)
    
    # Importa e executa o bot principal
    from telegram_bot import main as main_bot
    main_bot()

if __name__ == '__main__':
    main()