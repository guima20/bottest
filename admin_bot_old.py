#!/usr/bin/env python3
"""
Bot do Telegram - Bot Administrativo
Permite configurar o bot principal através de comandos
"""

import json
import logging
import os
import re
from typing import Dict, Any, List

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurações
CONFIG_FILE = 'config.json'
ADMIN_BOT_TOKEN = os.getenv('TELEGRAM_ADMIN_BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip().isdigit()]

def is_admin(user_id: int) -> bool:
    """Verifica se o usuário é administrador"""
    return user_id in ADMIN_IDS

def load_config() -> Dict[str, Any]:
    """Carrega a configuração do arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo {CONFIG_FILE} não encontrado")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar config: {e}")
        return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Salva a configuração no arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        logger.info("Configuração salva com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {e}")
        return False

async def admin_required(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Decorator para verificar se o usuário é admin"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Acesso negado! Você não é um administrador.")
        logger.warning(f"Tentativa de acesso não autorizado de {update.effective_user.id}")
        return False
    return True

async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /start do bot admin"""
    if not await admin_required(update, context):
        return
    
    welcome_text = """
🔧 **Bot Administrativo**

**Comandos disponíveis:**

📸 **Gerenciar Imagem:**
• `/set_image [url ou file_id]` - Define nova imagem

📝 **Gerenciar Texto:**
• `/set_text [texto]` - Define novo texto principal

🔘 **Gerenciar Botões:**
• `/set_button [1-4] [texto] [url]` - Atualiza botão específico

📋 **Visualizar:**
• `/show_config` - Mostra configuração atual
• `/help` - Mostra esta mensagem

**Exemplo de uso:**
```
/set_image https://exemplo.com/imagem.jpg
/set_text Novo texto promocional!
/set_button 1 Novo Botão https://novolink.com
```
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def set_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Define nova imagem"""
    if not await admin_required(update, context):
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: `/set_image [url ou file_id]`\n\n"
            "Exemplo: `/set_image https://exemplo.com/imagem.jpg`",
            parse_mode='Markdown'
        )
        return
    
    new_image = ' '.join(context.args)
    
    # Validação básica de URL
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...ou ip
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(new_image) and not new_image.startswith('AgAC'):  # File ID básico
        await update.message.reply_text("❌ URL inválida ou File ID inválido!")
        return
    
    config = load_config()
    config['image'] = new_image
    
    if save_config(config):
        await update.message.reply_text(f"✅ Imagem atualizada com sucesso!\n\n📸 Nova imagem: `{new_image}`", parse_mode='Markdown')
        logger.info(f"Imagem atualizada por admin {update.effective_user.id}")
    else:
        await update.message.reply_text("❌ Erro ao salvar configuração!")

async def set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Define novo texto"""
    if not await admin_required(update, context):
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: `/set_text [texto]`\n\n"
            "Exemplo: `/set_text Novo texto promocional!`",
            parse_mode='Markdown'
        )
        return
    
    new_text = ' '.join(context.args)
    
    if len(new_text) > 4096:  # Limite do Telegram
        await update.message.reply_text("❌ Texto muito longo! Máximo 4096 caracteres.")
        return
    
    config = load_config()
    config['text'] = new_text
    
    if save_config(config):
        await update.message.reply_text(f"✅ Texto atualizado com sucesso!\n\n📝 Novo texto: `{new_text}`", parse_mode='Markdown')
        logger.info(f"Texto atualizado por admin {update.effective_user.id}")
    else:
        await update.message.reply_text("❌ Erro ao salvar configuração!")

async def set_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Define novo botão"""
    if not await admin_required(update, context):
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Uso: `/set_button [1-4] [texto] [url]`\n\n"
            "Exemplo: `/set_button 1 Novo Botão https://novolink.com`",
            parse_mode='Markdown'
        )
        return
    
    try:
        button_num = int(context.args[0])
        if button_num < 1 or button_num > 4:
            raise ValueError()
    except ValueError:
        await update.message.reply_text("❌ Número do botão deve ser entre 1 e 4!")
        return
    
    button_text = context.args[1]
    button_url = context.args[2]
    
    # Validação de URL
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...ou ip
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(button_url):
        await update.message.reply_text("❌ URL inválida!")
        return
    
    config = load_config()
    
    # Garante que existe a lista de botões
    if 'buttons' not in config:
        config['buttons'] = [
            {"text": "Botão 1", "url": "https://telegram.org"},
            {"text": "Botão 2", "url": "https://telegram.org"},
            {"text": "Botão 3", "url": "https://telegram.org"},
            {"text": "Botão 4", "url": "https://telegram.org"}
        ]
    
    # Garante que temos 4 botões
    while len(config['buttons']) < 4:
        config['buttons'].append({"text": f"Botão {len(config['buttons']) + 1}", "url": "https://telegram.org"})
    
    # Atualiza o botão específico
    config['buttons'][button_num - 1] = {
        "text": button_text,
        "url": button_url
    }
    
    if save_config(config):
        await update.message.reply_text(
            f"✅ Botão {button_num} atualizado com sucesso!\n\n"
            f"🔘 Texto: `{button_text}`\n"
            f"🔗 URL: `{button_url}`",
            parse_mode='Markdown'
        )
        logger.info(f"Botão {button_num} atualizado por admin {update.effective_user.id}")
    else:
        await update.message.reply_text("❌ Erro ao salvar configuração!")

async def show_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra a configuração atual"""
    if not await admin_required(update, context):
        return
    
    config = load_config()
    
    if not config:
        await update.message.reply_text("❌ Nenhuma configuração encontrada!")
        return
    
    config_text = "📋 **Configuração Atual:**\n\n"
    
    # Imagem
    config_text += f"📸 **Imagem:** `{config.get('image', 'Não definida')}`\n\n"
    
    # Texto
    text = config.get('text', 'Não definido')
    if len(text) > 100:
        text = text[:100] + "..."
    config_text += f"📝 **Texto:** `{text}`\n\n"
    
    # Botões
    config_text += "🔘 **Botões:**\n"
    buttons = config.get('buttons', [])
    for i, button in enumerate(buttons, 1):
        if i <= 4:  # Mostra apenas os primeiros 4
            config_text += f"{i}. `{button.get('text', 'Sem texto')}` → `{button.get('url', 'Sem URL')}`\n"
    
    await update.message.reply_text(config_text, parse_mode='Markdown')

async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra ajuda do bot admin"""
    if not await admin_required(update, context):
        return
    
    await start_admin(update, context)

def main() -> None:
    """Função principal do bot administrativo"""
    if not ADMIN_BOT_TOKEN:
        logger.error("Token do bot admin não encontrado! Configure a variável TELEGRAM_ADMIN_BOT_TOKEN")
        return
    
    if not ADMIN_IDS:
        logger.error("IDs de admin não encontrados! Configure a variável ADMIN_IDS")
        return
    
    # Cria a aplicação
    application = Application.builder().token(ADMIN_BOT_TOKEN).build()
    
    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start_admin))
    application.add_handler(CommandHandler("help", help_admin))
    application.add_handler(CommandHandler("set_image", set_image))
    application.add_handler(CommandHandler("set_text", set_text))
    application.add_handler(CommandHandler("set_button", set_button))
    application.add_handler(CommandHandler("show_config", show_config))
    
    # Inicia o bot
    logger.info(f"Bot administrativo iniciado! Admins: {ADMIN_IDS}")
    logger.info("Pressione Ctrl+C para parar.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()