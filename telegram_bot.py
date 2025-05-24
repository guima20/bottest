#!/usr/bin/env python3
"""
Bot do Telegram - Bot Principal
Responde ao comando /start enviando imagem, texto e botões configuráveis
"""

import json
import logging
import os
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Carrega variáveis de ambiente do arquivo .env
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    pass

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurações
CONFIG_FILE = 'config.json'
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def load_config() -> Dict[str, Any]:
    """Carrega a configuração do arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info("Configuração carregada com sucesso")
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo {CONFIG_FILE} não encontrado")
        return create_default_config()
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return create_default_config()
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar config: {e}")
        return create_default_config()

def create_default_config() -> Dict[str, Any]:
    """Cria uma configuração padrão"""
    default_config = {
        "image": "https://via.placeholder.com/600x400/0066cc/ffffff?text=Chips+Gratis",
        "text": "👋 Olá! REGISTRE-SE para receber CHIPS GRÁTIS até $130 👇",
        "buttons": [
            {"text": "👉 Grab Your Free NOW", "url": "https://link1.com"},
            {"text": "👉 Discover More FreeChips and GameTips", "url": "https://link2.com"},
            {"text": "👉 Add To Group", "url": "https://link3.com"},
            {"text": "👉 Join RichGroup", "url": "https://link4.com"}
        ]
    }
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        logger.info("Configuração padrão criada")
    except Exception as e:
        logger.error(f"Erro ao criar configuração padrão: {e}")
    
    return default_config

def create_inline_keyboard(config: Dict[str, Any]) -> InlineKeyboardMarkup:
    """Cria o teclado inline com os botões configurados"""
    keyboard = []
    
    # Adiciona os 4 botões principais
    for button in config.get('buttons', []):
        keyboard.append([InlineKeyboardButton(
            text=button.get('text', 'Botão'),
            url=button.get('url', 'https://telegram.org')
        )])
    
    # Adiciona o botão Refresh
    keyboard.append([InlineKeyboardButton(
        text="🔄 Refresh",
        callback_data="refresh"
    )])
    
    return InlineKeyboardMarkup(keyboard)

async def send_main_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a mensagem principal com imagem, texto e botões"""
    try:
        config = load_config()
        
        # Cria o teclado inline
        reply_markup = create_inline_keyboard(config)
        
        # Envia a imagem
        image = config.get('image', '')
        if image:
            try:
                # Suporta tanto URLs quanto file_ids do Telegram
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image
                )
                logger.info(f"Imagem enviada para chat {update.effective_chat.id}")
            except Exception as e:
                logger.error(f"Erro ao enviar imagem: {e}")
                await update.message.reply_text("❌ Erro ao carregar imagem")
        
        # Envia o texto com os botões
        text = config.get('text', 'Mensagem padrão')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        logger.info(f"Mensagem principal enviada para chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem principal: {e}")
        await update.message.reply_text("❌ Erro interno do bot")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /start"""
    logger.info(f"Comando /start recebido de {update.effective_user.id}")
    await send_main_message(update, context)

async def refresh_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o botão Refresh"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Refresh solicitado por {update.effective_user.id}")
    
    try:
        config = load_config()
        
        # Cria o teclado inline
        reply_markup = create_inline_keyboard(config)
        
        # Envia a imagem novamente
        image_url = config.get('image', '')
        if image_url:
            try:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_url
                )
            except Exception as e:
                logger.error(f"Erro ao reenviar imagem: {e}")
        
        # Envia o texto com os botões novamente
        text = config.get('text', 'Mensagem padrão')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        logger.info(f"Mensagem refresh enviada para chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Erro ao fazer refresh: {e}")
        await query.edit_message_text("❌ Erro ao atualizar mensagem")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /help"""
    help_text = """
🤖 **Bot de Chips Grátis**

**Comandos disponíveis:**
• /start - Inicia o bot e mostra a mensagem principal
• /help - Mostra esta mensagem de ajuda

**Como usar:**
1. Digite /start para ver a mensagem principal
2. Clique nos botões para acessar os links
3. Use o botão 🔄 Refresh para recarregar a mensagem

Desenvolvido com ❤️ usando Python
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Função principal do bot"""
    if not BOT_TOKEN:
        logger.error("Token do bot não encontrado! Configure a variável TELEGRAM_BOT_TOKEN")
        return
    
    # Cria a aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(refresh_handler, pattern="refresh"))
    
    # Inicia o bot
    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()