#!/usr/bin/env python3
"""
🔧 BOT ADMINISTRATIVO COM INTERFACE INTERATIVA
Bot para gerenciar configurações do bot principal através de botões inline
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('admin_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações
ADMIN_BOT_TOKEN = os.getenv('TELEGRAM_ADMIN_BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
CONFIG_FILE = 'config.json'

def load_config() -> Dict[str, Any]:
    """Carrega configuração do arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Arquivo {CONFIG_FILE} não encontrado. Criando configuração padrão.")
        default_config = {
            "image": "https://picsum.photos/600/400",
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
    except json.JSONDecodeError:
        logger.error(f"Erro ao decodificar JSON do arquivo {CONFIG_FILE}")
        return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Salva configuração no arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info("Configuração salva com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {e}")
        return False

def is_admin(user_id: int) -> bool:
    """Verifica se o usuário é administrador."""
    return user_id in ADMIN_IDS

def get_main_menu_keyboard():
    """Cria o teclado do menu principal."""
    keyboard = [
        [InlineKeyboardButton("🔧 Painel Administrativo Interativo", callback_data="header")],
        [InlineKeyboardButton("📊 Status Atual", callback_data="status")],
        [
            InlineKeyboardButton("📝 Alterar Texto", callback_data="edit_text"),
            InlineKeyboardButton("🖼️ Alterar Imagem", callback_data="edit_image")
        ],
        [
            InlineKeyboardButton("🔘 Botão 1", callback_data="edit_button_1"),
            InlineKeyboardButton("🔘 Botão 2", callback_data="edit_button_2")
        ],
        [
            InlineKeyboardButton("🔘 Botão 3", callback_data="edit_button_3"),
            InlineKeyboardButton("🔘 Botão 4", callback_data="edit_button_4")
        ],
        [
            InlineKeyboardButton("📋 Ver Configuração", callback_data="show_config"),
            InlineKeyboardButton("🔄 Atualizar Menu", callback_data="refresh_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_status_text():
    """Gera texto do status atual."""
    config = load_config()
    
    # Verifica se imagem está configurada
    image_status = "✅ Configurada" if config.get('image') else "❌ Não configurada"
    
    # Verifica se texto está configurado
    text_status = "✅ Configurado" if config.get('text') else "❌ Não configurado"
    
    # Conta botões configurados
    buttons = config.get('buttons', [])
    buttons_count = len([b for b in buttons if b.get('text') and b.get('url')])
    
    status_text = f"""
📊 **Status Atual:**
🖼️ Imagem: {image_status}
📝 Texto: {text_status}
🔘 Botões: {buttons_count} configurados

Selecione uma opção abaixo:
"""
    return status_text

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Este bot é apenas para administradores.")
        return
    
    status_text = get_status_text()
    keyboard = get_main_menu_keyboard()
    
    await update.message.reply_text(
        status_text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para botões inline."""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Acesso negado!")
        return
    
    data = query.data
    
    if data == "header":
        await query.answer("🔧 Painel Administrativo Ativo!", show_alert=True)
        return
    
    elif data == "status":
        config = load_config()
        status_detail = f"""
📊 **Status Detalhado:**

🖼️ **Imagem:** {config.get('image', 'Não configurada')[:50]}...

📝 **Texto:** {config.get('text', 'Não configurado')[:100]}...

🔘 **Botões:**
"""
        buttons = config.get('buttons', [])
        for i, button in enumerate(buttons, 1):
            status_detail += f"  {i}. {button.get('text', 'N/A')[:30]}...\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="refresh_menu")]]
        await query.edit_message_text(
            status_detail,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif data == "edit_text":
        await query.edit_message_text(
            "📝 **Alterar Texto Principal**\n\nEnvie o novo texto que será exibido no bot principal:",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'text'
    
    elif data == "edit_image":
        await query.edit_message_text(
            "🖼️ **Alterar Imagem**\n\nVocê pode:\n• Enviar uma foto diretamente\n• Enviar a URL de uma imagem\n\n📤 Aguardando sua imagem...",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'image'
    
    elif data.startswith("edit_button_"):
        button_num = data.split("_")[-1]
        keyboard = [
            [InlineKeyboardButton(f"📝 Alterar Texto do Botão {button_num}", callback_data=f"button_text_{button_num}")],
            [InlineKeyboardButton(f"🔗 Alterar Link do Botão {button_num}", callback_data=f"button_url_{button_num}")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="refresh_menu")]
        ]
        await query.edit_message_text(
            f"🔘 **Configurar Botão {button_num}**\n\nEscolha o que deseja alterar:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif data.startswith("button_text_"):
        button_num = data.split("_")[-1]
        await query.edit_message_text(
            f"📝 **Alterar Texto do Botão {button_num}**\n\nEnvie o novo texto para o botão:",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = f'button_text_{button_num}'
    
    elif data.startswith("button_url_"):
        button_num = data.split("_")[-1]
        await query.edit_message_text(
            f"🔗 **Alterar Link do Botão {button_num}**\n\nEnvie o novo link para o botão:",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = f'button_url_{button_num}'
    
    elif data == "show_config":
        config = load_config()
        config_text = f"""
📋 **Configuração Atual:**

🖼️ **Imagem:** `{config.get('image', 'Não configurada')}`

📝 **Texto:** 
```
{config.get('text', 'Não configurado')}
```

🔘 **Botões:**
"""
        buttons = config.get('buttons', [])
        for i, button in enumerate(buttons, 1):
            config_text += f"  {i}. `{button.get('text', 'N/A')}` → `{button.get('url', 'N/A')}`\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="refresh_menu")]]
        await query.edit_message_text(
            config_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif data == "refresh_menu":
        status_text = get_status_text()
        keyboard = get_main_menu_keyboard()
        await query.edit_message_text(
            status_text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para fotos enviadas."""
    if not is_admin(update.effective_user.id):
        return
    
    waiting_for = context.user_data.get('waiting_for')
    if waiting_for != 'image':
        return
    
    try:
        # Pega a foto de maior resolução
        photo = update.message.photo[-1]
        file_id = photo.file_id
        
        # Baixa a foto
        file = await context.bot.get_file(file_id)
        
        # Cria diretório para imagens se não existir
        os.makedirs('images', exist_ok=True)
        
        # Salva a foto localmente
        photo_path = f"images/current_image.jpg"
        await file.download_to_drive(photo_path)
        
        # Atualiza a configuração com o caminho local
        config = load_config()
        config['image'] = photo_path
        
        if save_config(config):
            # Envia a foto de volta como confirmação
            await update.message.reply_photo(
                photo=file_id,
                caption="✅ **Imagem atualizada com sucesso!**\n\n📸 Esta é a nova imagem que será exibida no bot principal.\n💾 Foto salva localmente para compatibilidade.",
                parse_mode='Markdown'
            )
            
            # Aguarda um momento e volta ao menu
            await asyncio.sleep(1)
            status_text = get_status_text()
            keyboard = get_main_menu_keyboard()
            await update.message.reply_text(
                f"🔄 **Voltando ao menu principal...**\n\n{status_text}",
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
    
    except Exception as e:
        logger.error(f"Erro ao processar foto: {e}")
        await update.message.reply_text(
            "❌ **Erro ao processar a foto!**\n\nTente novamente ou use uma URL de imagem.",
            parse_mode='Markdown'
        )
    
    # Limpa o estado de espera
    context.user_data['waiting_for'] = None

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens de texto."""
    if not is_admin(update.effective_user.id):
        return
    
    waiting_for = context.user_data.get('waiting_for')
    if not waiting_for:
        return
    
    config = load_config()
    message_text = update.message.text
    success = False
    
    if waiting_for == 'text':
        config['text'] = message_text
        if save_config(config):
            await update.message.reply_text(
                f"✅ **Texto atualizado com sucesso!**\n\nNovo texto:\n```\n{message_text}\n```",
                parse_mode='Markdown'
            )
            success = True
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
    
    elif waiting_for == 'image':
        config['image'] = message_text
        if save_config(config):
            # Tenta mostrar a imagem se for uma URL válida
            try:
                await update.message.reply_photo(
                    photo=message_text,
                    caption="✅ **Imagem atualizada com sucesso!**\n\n📸 Esta é a nova imagem que será exibida no bot principal.",
                    parse_mode='Markdown'
                )
                success = True
            except:
                await update.message.reply_text(
                    f"✅ **URL da imagem salva!**\n\nNova URL: `{message_text}`\n\n⚠️ Não foi possível visualizar a imagem. Verifique se a URL está correta.",
                    parse_mode='Markdown'
                )
                success = True
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
    
    elif waiting_for.startswith('button_text_'):
        button_num = int(waiting_for.split('_')[-1]) - 1
        if 'buttons' not in config:
            config['buttons'] = [{"text": "", "url": ""} for _ in range(4)]
        
        while len(config['buttons']) <= button_num:
            config['buttons'].append({"text": "", "url": ""})
        
        config['buttons'][button_num]['text'] = message_text
        if save_config(config):
            await update.message.reply_text(
                f"✅ **Texto do Botão {button_num + 1} atualizado!**\n\nNovo texto: `{message_text}`",
                parse_mode='Markdown'
            )
            success = True
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
    
    elif waiting_for.startswith('button_url_'):
        button_num = int(waiting_for.split('_')[-1]) - 1
        if 'buttons' not in config:
            config['buttons'] = [{"text": "", "url": ""} for _ in range(4)]
        
        while len(config['buttons']) <= button_num:
            config['buttons'].append({"text": "", "url": ""})
        
        config['buttons'][button_num]['url'] = message_text
        if save_config(config):
            await update.message.reply_text(
                f"✅ **Link do Botão {button_num + 1} atualizado!**\n\nNovo link: `{message_text}`",
                parse_mode='Markdown'
            )
            success = True
        else:
            await update.message.reply_text("❌ Erro ao salvar configuração!")
    
    # Limpa o estado de espera
    context.user_data['waiting_for'] = None
    
    # Se a operação foi bem-sucedida, volta ao menu após um momento
    if success:
        await asyncio.sleep(1)
        status_text = get_status_text()
        keyboard = get_main_menu_keyboard()
        await update.message.reply_text(
            f"🔄 **Voltando ao menu principal...**\n\n{status_text}",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

def main():
    """Função principal do bot administrativo."""
    if not ADMIN_BOT_TOKEN:
        logger.error("Token do bot administrativo não encontrado! Configure TELEGRAM_ADMIN_BOT_TOKEN")
        return
    
    if not ADMIN_IDS:
        logger.warning("Nenhum ID de administrador configurado!")
    
    # Cria a aplicação
    application = Application.builder().token(ADMIN_BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Inicia o bot
    logger.info("Bot administrativo iniciado!")
    logger.info(f"Administradores configurados: {ADMIN_IDS}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()