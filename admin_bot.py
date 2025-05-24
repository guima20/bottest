#!/usr/bin/env python3
"""
Bot Administrativo do Telegram - Interface Interativa
Permite alterar configurações do bot principal via interface amigável.
"""

import json
import logging
import os
import re
from typing import Dict, Any, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, PhotoSize
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurações
CONFIG_FILE = 'config.json'
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '123456789').split(',')]

# Estados da conversa
WAITING_FOR_TEXT = "waiting_for_text"
WAITING_FOR_BUTTON_TEXT = "waiting_for_button_text"
WAITING_FOR_BUTTON_URL = "waiting_for_button_url"
WAITING_FOR_IMAGE = "waiting_for_image"

def load_config() -> Dict[str, Any]:
    """Carrega configuração do arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Arquivo {CONFIG_FILE} não encontrado. Criando configuração padrão.")
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
        save_config(default_config)
        return default_config
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Salva configuração no arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        logger.info("Configuração salva com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {e}")
        return False

def is_admin(user_id: int) -> bool:
    """Verifica se o usuário é administrador."""
    return user_id in ADMIN_IDS

def validate_url(url: str) -> bool:
    """Valida se a URL está em formato correto."""
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def get_main_menu_keyboard():
    """Cria o teclado do menu principal."""
    keyboard = [
        [
            InlineKeyboardButton("📝 Alterar Texto", callback_data="change_text"),
            InlineKeyboardButton("📸 Alterar Imagem", callback_data="change_image")
        ],
        [
            InlineKeyboardButton("🔘 Botão 1", callback_data="change_button_1"),
            InlineKeyboardButton("🔘 Botão 2", callback_data="change_button_2")
        ],
        [
            InlineKeyboardButton("🔘 Botão 3", callback_data="change_button_3"),
            InlineKeyboardButton("🔘 Botão 4", callback_data="change_button_4")
        ],
        [
            InlineKeyboardButton("📋 Ver Configuração", callback_data="show_config"),
            InlineKeyboardButton("🔄 Atualizar Menu", callback_data="refresh_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_button_menu_keyboard(button_num: int):
    """Cria o teclado para editar um botão específico."""
    keyboard = [
        [
            InlineKeyboardButton("✏️ Alterar Texto", callback_data=f"edit_button_text_{button_num}"),
            InlineKeyboardButton("🔗 Alterar URL", callback_data=f"edit_button_url_{button_num}")
        ],
        [
            InlineKeyboardButton("🏠 Voltar ao Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Mostra painel administrativo interativo."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Você não é um administrador.")
        logger.warning(f"Tentativa de acesso não autorizado: {update.effective_user.id}")
        return

    config = load_config()
    
    welcome_text = f"""
🔧 **Painel Administrativo Interativo**

Olá, administrador! Use os botões abaixo para gerenciar o bot de forma fácil e intuitiva.

📊 **Status Atual:**
📸 Imagem: {'✅ Configurada' if config.get('image') else '❌ Não configurada'}
📝 Texto: {'✅ Configurado' if config.get('text') else '❌ Não configurado'}
🔘 Botões: {len(config.get('buttons', []))} configurados

💡 **Dicas:**
• Use os botões para navegar facilmente
• Para imagens: envie uma foto diretamente no chat
• Todas as alterações são salvas automaticamente
    """
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manipula callbacks dos botões inline."""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Acesso negado!")
        return

    data = query.data
    
    if data == "main_menu" or data == "refresh_menu":
        config = load_config()
        welcome_text = f"""
🔧 **Painel Administrativo Interativo**

📊 **Status Atual:**
📸 Imagem: {'✅ Configurada' if config.get('image') else '❌ Não configurada'}
📝 Texto: {'✅ Configurado' if config.get('text') else '❌ Não configurado'}
🔘 Botões: {len(config.get('buttons', []))} configurados

Selecione uma opção abaixo:
        """
        await query.edit_message_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=get_main_menu_keyboard()
        )
    
    elif data == "show_config":
        config = load_config()
        config_text = "📋 **Configuração Atual:**\n\n"
        config_text += f"📸 **Imagem:** {config.get('image', 'Não definida')}\n\n"
        config_text += f"📝 **Texto:** {config.get('text', 'Não definido')[:100]}{'...' if len(config.get('text', '')) > 100 else ''}\n\n"
        config_text += "🔘 **Botões:**\n"
        
        for i, button in enumerate(config.get('buttons', []), 1):
            config_text += f"   {i}. {button.get('text', 'Sem texto')} → {button.get('url', 'Sem URL')}\n"
        
        keyboard = [[InlineKeyboardButton("🏠 Voltar ao Menu", callback_data="main_menu")]]
        await query.edit_message_text(
            config_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "change_text":
        context.user_data['state'] = WAITING_FOR_TEXT
        keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")]]
        await query.edit_message_text(
            "📝 **Alterar Texto Principal**\n\n"
            "Digite o novo texto que será exibido no bot principal:\n\n"
            "💡 *Dica: Use emojis para tornar mais atrativo!*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "change_image":
        context.user_data['state'] = WAITING_FOR_IMAGE
        keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")]]
        await query.edit_message_text(
            "📸 **Alterar Imagem**\n\n"
            "Você pode:\n"
            "• Enviar uma foto diretamente no chat\n"
            "• Ou digitar uma URL de imagem\n\n"
            "💡 *A imagem será usada no comando /start do bot principal*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data.startswith("change_button_"):
        button_num = int(data.split("_")[-1])
        config = load_config()
        button = config.get('buttons', [{}])[button_num - 1] if len(config.get('buttons', [])) >= button_num else {}
        
        button_text = f"""
🔘 **Configurar Botão {button_num}**

**Configuração Atual:**
📝 Texto: {button.get('text', 'Não definido')}
🔗 URL: {button.get('url', 'Não definida')}

Selecione o que deseja alterar:
        """
        
        await query.edit_message_text(
            button_text,
            parse_mode='Markdown',
            reply_markup=get_button_menu_keyboard(button_num)
        )
    
    elif data.startswith("edit_button_text_"):
        button_num = int(data.split("_")[-1])
        context.user_data['state'] = WAITING_FOR_BUTTON_TEXT
        context.user_data['button_num'] = button_num
        
        keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data=f"change_button_{button_num}")]]
        await query.edit_message_text(
            f"✏️ **Alterar Texto do Botão {button_num}**\n\n"
            "Digite o novo texto para o botão:\n\n"
            "💡 *Exemplo: 🎁 OFERTA ESPECIAL*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data.startswith("edit_button_url_"):
        button_num = int(data.split("_")[-1])
        context.user_data['state'] = WAITING_FOR_BUTTON_URL
        context.user_data['button_num'] = button_num
        
        keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data=f"change_button_{button_num}")]]
        await query.edit_message_text(
            f"🔗 **Alterar URL do Botão {button_num}**\n\n"
            "Digite a nova URL para o botão:\n\n"
            "💡 *Exemplo: https://exemplo.com*\n"
            "⚠️ *A URL deve começar com http:// ou https://*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manipula mensagens de texto e fotos."""
    if not is_admin(update.effective_user.id):
        return

    state = context.user_data.get('state')
    
    if state == WAITING_FOR_TEXT:
        new_text = update.message.text
        if len(new_text) > 1000:
            await update.message.reply_text("❌ Texto muito longo! Máximo 1000 caracteres.")
            return
        
        config = load_config()
        config['text'] = new_text
        
        if save_config(config):
            await update.message.reply_text(
                f"✅ **Texto atualizado com sucesso!**\n\n"
                f"📝 Novo texto: {new_text[:100]}{'...' if len(new_text) > 100 else ''}",
                parse_mode='Markdown',
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração.")
        
        context.user_data.clear()
    
    elif state == WAITING_FOR_IMAGE:
        if update.message.photo:
            # Usuário enviou uma foto
            photo = update.message.photo[-1]  # Pega a maior resolução
            file_id = photo.file_id
            
            config = load_config()
            config['image'] = file_id  # Salva o file_id da foto
            
            if save_config(config):
                await update.message.reply_text(
                    "✅ **Imagem atualizada com sucesso!**\n\n"
                    "📸 A nova imagem foi salva e será usada no bot principal.",
                    parse_mode='Markdown',
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await update.message.reply_text("❌ Erro ao salvar configuração.")
        
        elif update.message.text:
            # Usuário enviou uma URL
            image_url = update.message.text.strip()
            
            if not validate_url(image_url):
                await update.message.reply_text("❌ URL inválida! Use uma URL válida (http:// ou https://)")
                return
            
            config = load_config()
            config['image'] = image_url
            
            if save_config(config):
                await update.message.reply_text(
                    f"✅ **Imagem atualizada com sucesso!**\n\n"
                    f"📸 Nova imagem: {image_url}",
                    parse_mode='Markdown',
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await update.message.reply_text("❌ Erro ao salvar configuração.")
        
        context.user_data.clear()
    
    elif state == WAITING_FOR_BUTTON_TEXT:
        button_num = context.user_data.get('button_num')
        new_text = update.message.text
        
        config = load_config()
        if 'buttons' not in config:
            config['buttons'] = [{"text": "", "url": ""} for _ in range(4)]
        
        # Garante que o botão existe
        while len(config['buttons']) < button_num:
            config['buttons'].append({"text": "", "url": ""})
        
        config['buttons'][button_num - 1]['text'] = new_text
        
        if save_config(config):
            await update.message.reply_text(
                f"✅ **Texto do Botão {button_num} atualizado!**\n\n"
                f"📝 Novo texto: {new_text}",
                parse_mode='Markdown',
                reply_markup=get_button_menu_keyboard(button_num)
            )
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração.")
        
        context.user_data.clear()
    
    elif state == WAITING_FOR_BUTTON_URL:
        button_num = context.user_data.get('button_num')
        new_url = update.message.text.strip()
        
        if not validate_url(new_url):
            await update.message.reply_text("❌ URL inválida! Use uma URL válida (http:// ou https://)")
            return
        
        config = load_config()
        if 'buttons' not in config:
            config['buttons'] = [{"text": "", "url": ""} for _ in range(4)]
        
        # Garante que o botão existe
        while len(config['buttons']) < button_num:
            config['buttons'].append({"text": "", "url": ""})
        
        config['buttons'][button_num - 1]['url'] = new_url
        
        if save_config(config):
            await update.message.reply_text(
                f"✅ **URL do Botão {button_num} atualizada!**\n\n"
                f"🔗 Nova URL: {new_url}",
                parse_mode='Markdown',
                reply_markup=get_button_menu_keyboard(button_num)
            )
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração.")
        
        context.user_data.clear()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra ajuda."""
    help_text = """
🔧 **Bot Administrativo Interativo**

**Como usar:**
1. Use `/start` para abrir o painel principal
2. Clique nos botões para navegar
3. Para imagens: envie fotos diretamente no chat
4. Para textos: digite normalmente quando solicitado

**Funcionalidades:**
• 📝 Alterar texto principal do bot
• 📸 Alterar imagem (foto ou URL)
• 🔘 Configurar 4 botões personalizados
• 📋 Visualizar configuração atual
• 🔄 Interface totalmente interativa

**Dicas:**
• Use emojis para tornar mais atrativo
• URLs devem começar com http:// ou https://
• Fotos enviadas são salvas automaticamente
• Todas as alterações são aplicadas imediatamente

Digite `/start` para começar!
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Função principal do bot administrativo."""
    # Token do bot administrativo
    token = os.getenv('TELEGRAM_ADMIN_BOT_TOKEN')
    if not token:
        logger.error("Token do bot administrativo não encontrado! Configure TELEGRAM_ADMIN_BOT_TOKEN")
        return

    # Cria a aplicação
    application = Application.builder().token(token).build()

    # Adiciona handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    # Inicia o bot
    logger.info("Bot administrativo interativo iniciado!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()