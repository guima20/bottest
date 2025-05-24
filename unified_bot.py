#!/usr/bin/env python3
"""
Bot Unificado do Telegram - Principal + Admin
Combina as funcionalidades dos dois bots em um só para evitar conflitos de API
"""

import json
import logging
import os
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    logger.warning("Arquivo .env não encontrado")

# Configurações
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
CONFIG_FILE = 'config.json'

def load_config() -> Dict[str, Any]:
    """Carrega configuração do arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo {CONFIG_FILE} não encontrado")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Salva configuração no arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        logger.info("Configuração salva com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {e}")
        return False

def is_admin(user_id: int) -> bool:
    """Verifica se o usuário é administrador."""
    return user_id in ADMIN_IDS

async def send_main_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a mensagem principal com imagem, texto e botões."""
    config = load_config()
    
    if not config:
        await update.message.reply_text("❌ Erro ao carregar configuração!")
        return
    
    try:
        # Envia a imagem
        image_url = config.get('image', '')
        if image_url:
            await update.message.reply_photo(photo=image_url)
        
        # Prepara os botões
        keyboard = []
        buttons = config.get('buttons', [])
        
        # Adiciona os botões configurados
        for button in buttons:
            keyboard.append([InlineKeyboardButton(
                text=button.get('text', 'Botão'),
                url=button.get('url', 'https://example.com')
            )])
        
        # Adiciona o botão Refresh
        keyboard.append([InlineKeyboardButton(
            text="🔄 Refresh",
            callback_data="refresh"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Envia o texto com os botões
        text = config.get('text', 'Mensagem não configurada')
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        logger.info(f"Mensagem principal enviada para {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem principal: {e}")
        await update.message.reply_text("❌ Erro ao enviar mensagem!")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start."""
    await send_main_message(update, context)

async def refresh_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o botão Refresh."""
    query = update.callback_query
    await query.answer()
    
    # Remove a mensagem anterior
    await query.delete_message()
    
    # Reenvia a mensagem principal
    # Simula um update de mensagem para reutilizar a função
    class FakeUpdate:
        def __init__(self, user_id, chat_id):
            self.effective_user = type('obj', (object,), {'id': user_id})()
            self.message = type('obj', (object,), {
                'reply_photo': lambda photo: context.bot.send_photo(chat_id=chat_id, photo=photo),
                'reply_text': lambda text, reply_markup=None, parse_mode=None: context.bot.send_message(
                    chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode
                )
            })()
    
    fake_update = FakeUpdate(query.from_user.id, query.message.chat_id)
    await send_main_message(fake_update, context)

# ==================== COMANDOS ADMINISTRATIVOS ====================

async def admin_set_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para alterar a imagem (apenas admins)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Apenas administradores podem usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Uso: /set_image <url_ou_file_id>")
        return
    
    new_image = ' '.join(context.args)
    config = load_config()
    config['image'] = new_image
    
    if save_config(config):
        await update.message.reply_text(f"✅ Imagem atualizada!\n📷 Nova imagem: {new_image}")
        logger.info(f"Admin {update.effective_user.id} alterou a imagem para: {new_image}")
    else:
        await update.message.reply_text("❌ Erro ao salvar configuração!")

async def admin_set_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para alterar o texto (apenas admins)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Apenas administradores podem usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Uso: /set_text <novo_texto>")
        return
    
    new_text = ' '.join(context.args)
    config = load_config()
    config['text'] = new_text
    
    if save_config(config):
        await update.message.reply_text(f"✅ Texto atualizado!\n📝 Novo texto: {new_text}")
        logger.info(f"Admin {update.effective_user.id} alterou o texto para: {new_text}")
    else:
        await update.message.reply_text("❌ Erro ao salvar configuração!")

async def admin_set_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para alterar um botão (apenas admins)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Apenas administradores podem usar este comando.")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text("❌ Uso: /set_button <1-4> <texto> <url>")
        return
    
    try:
        button_num = int(context.args[0])
        if button_num < 1 or button_num > 4:
            await update.message.reply_text("❌ Número do botão deve ser entre 1 e 4!")
            return
        
        button_text = context.args[1]
        button_url = context.args[2]
        
        config = load_config()
        if 'buttons' not in config:
            config['buttons'] = []
        
        # Garante que há pelo menos 4 botões
        while len(config['buttons']) < 4:
            config['buttons'].append({"text": "Botão", "url": "https://example.com"})
        
        # Atualiza o botão especificado (índice 0-based)
        config['buttons'][button_num - 1] = {
            "text": button_text,
            "url": button_url
        }
        
        if save_config(config):
            await update.message.reply_text(
                f"✅ Botão {button_num} atualizado!\n"
                f"🔘 Texto: {button_text}\n"
                f"🔗 URL: {button_url}"
            )
            logger.info(f"Admin {update.effective_user.id} alterou o botão {button_num}")
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
            
    except ValueError:
        await update.message.reply_text("❌ Número do botão inválido!")

async def admin_show_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para mostrar a configuração atual (apenas admins)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Apenas administradores podem usar este comando.")
        return
    
    config = load_config()
    if not config:
        await update.message.reply_text("❌ Erro ao carregar configuração!")
        return
    
    message = "📋 **CONFIGURAÇÃO ATUAL**\n\n"
    
    # Imagem
    image = config.get('image', 'Não configurada')
    message += f"📷 **Imagem:** {image}\n\n"
    
    # Texto
    text = config.get('text', 'Não configurado')
    message += f"📝 **Texto:** {text}\n\n"
    
    # Botões
    buttons = config.get('buttons', [])
    message += "🔘 **Botões:**\n"
    for i, button in enumerate(buttons, 1):
        message += f"  {i}. {button.get('text', 'N/A')} → {button.get('url', 'N/A')}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de ajuda para administradores."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Apenas administradores podem usar este comando.")
        return
    
    help_text = """
🔧 **COMANDOS ADMINISTRATIVOS**

📷 `/set_image <url>` - Alterar imagem
📝 `/set_text <texto>` - Alterar texto
🔘 `/set_button <1-4> <texto> <url>` - Alterar botão
📋 `/show_config` - Mostrar configuração atual
❓ `/admin_help` - Esta ajuda

**Exemplo de uso:**
`/set_button 1 "🎁 OFERTA ESPECIAL" "https://meusite.com"`
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Função principal do bot."""
    if not BOT_TOKEN:
        logger.error("Token do bot não encontrado! Configure a variável TELEGRAM_BOT_TOKEN")
        return
    
    if not ADMIN_IDS:
        logger.warning("Nenhum ID de administrador configurado!")
    
    # Cria a aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers do bot principal
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(refresh_handler, pattern="refresh"))
    
    # Handlers administrativos
    application.add_handler(CommandHandler("set_image", admin_set_image))
    application.add_handler(CommandHandler("set_text", admin_set_text))
    application.add_handler(CommandHandler("set_button", admin_set_button))
    application.add_handler(CommandHandler("show_config", admin_show_config))
    application.add_handler(CommandHandler("admin_help", admin_help))
    
    # Inicia o bot
    logger.info("Bot unificado iniciado!")
    logger.info(f"Administradores configurados: {ADMIN_IDS}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()