#!/usr/bin/env python3
"""
Script para executar ambos os bots em produção
Bot Principal: 7862546836:AAHtlgCVOdrI5saF0Ca4ruX1c56FyVHUQAE
Bot Admin: 7727769382:AAEvsuGUALNt5rDLjyOdHaTRKnJmu36ch5A
"""

import os
import sys
import threading
import time
import logging
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def set_environment_variables():
    """Define as variáveis de ambiente com os tokens dos bots."""
    os.environ['TELEGRAM_BOT_TOKEN'] = '7862546836:AAHtlgCVOdrI5saF0Ca4ruX1c56FyVHUQAE'
    os.environ['TELEGRAM_ADMIN_BOT_TOKEN'] = '7727769382:AAEvsuGUALNt5rDLjyOdHaTRKnJmu36ch5A'
    os.environ['ADMIN_IDS'] = '123456789'  # Substitua pelo seu ID real
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'INFO'
    
    logger.info("✅ Variáveis de ambiente configuradas")

def run_main_bot():
    """Executa o bot principal."""
    try:
        logger.info("🤖 Iniciando Bot Principal...")
        import telegram_bot
        telegram_bot.main()
    except Exception as e:
        logger.error(f"❌ Erro no bot principal: {e}")

def run_admin_bot():
    """Executa o bot administrativo."""
    try:
        logger.info("🔧 Iniciando Bot Administrativo...")
        import admin_bot
        admin_bot.main()
    except Exception as e:
        logger.error(f"❌ Erro no bot administrativo: {e}")

def main():
    """Função principal que executa ambos os bots."""
    print("🚀 INICIANDO SISTEMA DE BOTS DO TELEGRAM")
    print("=" * 50)
    print("🤖 Bot Principal: Responde aos usuários")
    print("🔧 Bot Admin: Interface de configuração")
    print("=" * 50)
    
    # Configura as variáveis de ambiente
    set_environment_variables()
    
    # Cria threads para executar os bots simultaneamente
    main_bot_thread = threading.Thread(target=run_main_bot, name="MainBot")
    admin_bot_thread = threading.Thread(target=run_admin_bot, name="AdminBot")
    
    # Marca as threads como daemon para que terminem quando o programa principal terminar
    main_bot_thread.daemon = True
    admin_bot_thread.daemon = True
    
    try:
        # Inicia as threads
        main_bot_thread.start()
        time.sleep(2)  # Pequena pausa entre os bots
        admin_bot_thread.start()
        
        logger.info("✅ Ambos os bots foram iniciados com sucesso!")
        print("\n🎉 BOTS EXECUTANDO COM SUCESSO!")
        print("📱 Teste o bot principal enviando /start")
        print("🔧 Use o bot admin para configurar")
        print("⏹️  Pressione Ctrl+C para parar\n")
        
        # Mantém o programa principal rodando
        while True:
            time.sleep(1)
            
            # Verifica se as threads ainda estão vivas
            if not main_bot_thread.is_alive():
                logger.error("❌ Bot principal parou de funcionar!")
                break
            if not admin_bot_thread.is_alive():
                logger.error("❌ Bot administrativo parou de funcionar!")
                break
                
    except KeyboardInterrupt:
        logger.info("🛑 Parando os bots...")
        print("\n🛑 Bots interrompidos pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
    finally:
        print("👋 Sistema finalizado!")

if __name__ == '__main__':
    main()