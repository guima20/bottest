#!/usr/bin/env python3
"""
Executor para ambos os bots do Telegram
Executa o bot principal e o bot administrativo simultaneamente
"""

import asyncio
import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

# Tenta carregar variáveis de ambiente de arquivo .env
try:
    from load_env import load_env_file
    load_env_file()
except ImportError:
    pass

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_main_bot():
    """Executa o bot principal"""
    try:
        from telegram_bot import main as main_bot_main
        logger.info("Iniciando bot principal...")
        main_bot_main()
    except Exception as e:
        logger.error(f"Erro no bot principal: {e}")

def run_admin_bot():
    """Executa o bot administrativo"""
    try:
        from admin_bot import main as admin_bot_main
        logger.info("Iniciando bot administrativo...")
        admin_bot_main()
    except Exception as e:
        logger.error(f"Erro no bot administrativo: {e}")

def signal_handler(signum, frame):
    """Handler para sinais de interrupção"""
    logger.info("Recebido sinal de interrupção. Parando bots...")
    sys.exit(0)

def main():
    """Função principal que executa ambos os bots"""
    # Verifica se os tokens estão configurados
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        print("\n🔧 Configure as variáveis de ambiente:")
        print("export TELEGRAM_BOT_TOKEN='seu_token_do_bot_principal'")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_do_bot_admin'")
        print("export ADMIN_IDS='123456789,987654321'  # IDs dos admins separados por vírgula")
        return
    
    if not os.getenv('TELEGRAM_ADMIN_BOT_TOKEN'):
        logger.error("❌ TELEGRAM_ADMIN_BOT_TOKEN não configurado!")
        print("\n🔧 Configure as variáveis de ambiente:")
        print("export TELEGRAM_BOT_TOKEN='seu_token_do_bot_principal'")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_do_bot_admin'")
        print("export ADMIN_IDS='123456789,987654321'  # IDs dos admins separados por vírgula")
        return
    
    if not os.getenv('ADMIN_IDS'):
        logger.error("❌ ADMIN_IDS não configurado!")
        print("\n🔧 Configure as variáveis de ambiente:")
        print("export TELEGRAM_BOT_TOKEN='seu_token_do_bot_principal'")
        print("export TELEGRAM_ADMIN_BOT_TOKEN='seu_token_do_bot_admin'")
        print("export ADMIN_IDS='123456789,987654321'  # IDs dos admins separados por vírgula")
        return
    
    # Configura handler para sinais
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Iniciando sistema de bots do Telegram...")
    
    # Executa ambos os bots em threads separadas
    with ThreadPoolExecutor(max_workers=2) as executor:
        try:
            # Submete ambos os bots para execução
            main_bot_future = executor.submit(run_main_bot)
            admin_bot_future = executor.submit(run_admin_bot)
            
            logger.info("✅ Ambos os bots foram iniciados!")
            logger.info("📱 Bot principal: responde a /start")
            logger.info("🔧 Bot administrativo: comandos de configuração")
            logger.info("⏹️  Pressione Ctrl+C para parar")
            
            # Aguarda ambos os bots
            main_bot_future.result()
            admin_bot_future.result()
            
        except KeyboardInterrupt:
            logger.info("🛑 Interrupção recebida. Parando bots...")
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
        finally:
            logger.info("🔚 Bots finalizados")

if __name__ == '__main__':
    main()