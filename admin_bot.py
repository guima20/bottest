#!/usr/bin/env python3
"""
Bot Administrativo para gerenciar o Bot Kangaroo

Este bot permite o controle e gerenciamento do bot principal (Kangaroo),
com funções para enviar mensagens, agendar envios, gerenciar grupos e
configurar comportamentos.
"""

import os
import json
import logging
import asyncio
import datetime
from dotenv import load_dotenv
from typing import Dict, List, Union, Any, Optional, Callable

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler, 
                          MessageHandler, ContextTypes, filters, ConversationHandler)

# Importa funções de gerenciamento de mensagens
from bot_messages import add_pending_message, load_pending_messages, get_messages_to_send

# Configuração de logging com formato timestamp e nível INFO
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Define constantes a partir das variáveis de ambiente
TELEGRAM_ADMIN_BOT_TOKEN = os.getenv('TELEGRAM_ADMIN_BOT_TOKEN', '7727769382:AAEvsuGUALNt5rDLjyOdHaTRKnJmu36ch5A')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Se não houver admin IDs configurados, adiciona um ID padrão para desenvolvimento
if not ADMIN_IDS:
    logger.warning("Nenhum ADMIN_ID configurado no .env. Usando ID de desenvolvimento.")
    ADMIN_IDS = [12345678]  # Substitua pelo seu ID

# Caminhos para arquivos de configuração
CONFIG_FILE = 'config.json'
GROUPS_FILE = 'groups.json'
PENDING_MESSAGES_FILE = 'pending_messages.json'

# Estados da conversa
WAITING_MESSAGE_TEXT, WAITING_SCHEDULE_TIME, WAITING_BUTTON_TEXT, WAITING_BUTTON_URL = range(4)

def is_admin(user_id: int) -> bool:
    """Verifica se o usuário é um administrador autorizado."""
    return user_id in ADMIN_IDS

# Funções de utilitário para lidar com arquivos
def load_json_file(filename: str, default=None) -> Any:
    """Carrega dados de um arquivo JSON."""
    default = default or {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            logger.warning(f"Arquivo {filename} não encontrado. Retornando valor padrão.")
            return default
    except Exception as e:
        logger.error(f"Erro ao carregar {filename}: {e}")
        return default

def save_json_file(filename: str, data: Any) -> bool:
    """Salva dados em um arquivo JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"Dados salvos com sucesso em {filename}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar {filename}: {e}")
        return False

def load_groups() -> List[Dict[str, Any]]:
    """Carrega a lista de grupos onde o bot está ativo."""
    return load_json_file(GROUPS_FILE, [])

def save_groups(groups: List[Dict[str, Any]]) -> bool:
    """Salva a lista de grupos onde o bot está ativo."""
    return save_json_file(GROUPS_FILE, groups)

def load_config() -> Dict[str, Any]:
    """Carrega a configuração do bot."""
    return load_json_file(CONFIG_FILE, {
        "text": "Bem-vindo ao Bot Kangaroo!",
        "buttons": [],
        "image": ""
    })

def save_config(config: Dict[str, Any]) -> bool:
    """Salva a configuração do bot."""
    return save_json_file(CONFIG_FILE, config)

# Decorador para verificar permissões de administrador
def admin_required(func: Callable) -> Callable:
    """Decorador que verifica se o usuário é administrador antes de executar o comando."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        user_id = update.effective_user.id
        
        if not is_admin(user_id):
            await update.message.reply_text(
                "⚠️ Você não tem permissão para usar este bot. "
                "Este bot é exclusivo para administradores."
            )
            return
        
        return await func(update, context)
    
    return wrapper

# Funções para envio de logs para Telegram
async def send_log(app: Application, message: str, alert: bool = False) -> None:
    """Envia mensagem de log para o canal de logs do Telegram."""
    if not TELEGRAM_CHAT_ID:
        return
    
    try:
        # Formata a mensagem com timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if alert:
            formatted_message = f"⚠️ ALERTA: {message}\n\n🕒 {timestamp}"
        else:
            formatted_message = f"ℹ️ LOG: {message}\n\n🕒 {timestamp}"
        
        await app.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=formatted_message,
            disable_notification=not alert
        )
    except Exception as e:
        logger.error(f"Erro ao enviar log para o Telegram: {e}")

@admin_required
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - exibe o painel principal com opções de administração."""
    user = update.effective_user
    
    # Carrega dados para exibir no painel
    groups = load_groups()
    config = load_config()
    
    # Estatísticas básicas
    num_groups = len(groups)
    welcome_text = config.get('text', 'Sem texto definido')
    welcome_text_preview = welcome_text[:30] + "..." if len(welcome_text) > 30 else welcome_text
    
    # Mensagem de boas-vindas com estatísticas
    message = f"🤖 *Painel de Administração - Bot Kangaroo* 🤖\n\n"
    message += f"Olá, *{user.first_name}*! Bem-vindo ao painel administrativo.\n\n"
    message += f"📊 *Estatísticas:*\n"
    message += f"- Grupos cadastrados: {num_groups}\n"
    message += f"- Mensagem de boas-vindas: _{welcome_text_preview}_\n\n"
    message += f"Selecione uma opção abaixo:"
    
    # Botões do menu principal
    keyboard = [
        [
            InlineKeyboardButton("💬 Enviar Mensagem", callback_data="send_message"),
            InlineKeyboardButton("📅 Agendar Mensagem", callback_data="schedule_message")
        ],
        [
            InlineKeyboardButton("📱 Gerenciar Grupos", callback_data="manage_groups"),
            InlineKeyboardButton("⚙️ Configurações", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📊 Ver Logs", callback_data="view_logs")
        ]
    ]
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

@admin_required
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help - exibe ajuda sobre os comandos disponíveis."""
    message = "🤖 *Bot Administrativo - Ajuda* 🤖\n\n"
    message += "*Comandos disponíveis:*\n\n"
    message += "/start - Exibe o painel principal\n"
    message += "/send - Inicia o processo de envio de mensagem\n"
    message += "/groups - Gerencia grupos cadastrados\n"
    message += "/config - Edita configurações do bot principal\n"
    message += "/logs - Visualiza logs recentes\n"
    message += "/help - Exibe esta mensagem de ajuda\n\n"
    message += "Para mais informações, consulte a documentação."
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown'
    )

@admin_required
async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /send - inicia o processo de envio de mensagem para grupos."""
    groups = load_groups()
    
    if not groups:
        await update.message.reply_text(
            "⚠️ Não há grupos cadastrados para enviar mensagens.\n"
            "Adicione o bot a pelo menos um grupo primeiro."
        )
        return
    
    # Botões para seleção de destino
    keyboard = [
        [
            InlineKeyboardButton("📱 Enviar para um grupo específico", callback_data="send_to_specific"),
            InlineKeyboardButton("📢 Enviar para todos os grupos", callback_data="send_to_all")
        ],
        [
            InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")
        ]
    ]
    
    await update.message.reply_text(
        "*💬 Enviar Nova Mensagem*\n\n"
        "Selecione uma opção de envio:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

@admin_required
async def groups_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /groups - gerencia os grupos cadastrados."""
    groups = load_groups()
    
    if not groups:
        message = "⚠️ Não há grupos cadastrados.\n\nO bot precisa ser adicionado a grupos para que eles apareçam aqui."
        keyboard = [[InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]]
    else:
        message = "*📱 Grupos Cadastrados*\n\n"
        
        for i, group in enumerate(groups, 1):
            # Usa chat_id se disponível, caso contrário usa id
            group_id = group.get('chat_id') or group.get('id', 'N/A')
            group_title = group.get('title', 'Grupo sem nome')
            group_members = group.get('member_count', 0)
            
            message += f"{i}. *{group_title}*\n"
            message += f"   ID: `{group_id}`\n"
            message += f"   Membros: {group_members}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("💰 Obter Link de Convite", callback_data="get_invite_links")],
            [InlineKeyboardButton("❌ Remover Grupo", callback_data="remove_group")],
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ]
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

@admin_required
async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /config - edita configurações do bot principal."""
    config = load_config()
    
    welcome_text = config.get('text', 'Sem texto definido')
    if len(welcome_text) > 100:
        welcome_text = welcome_text[:100] + "..."
        
    has_image = "Sim" if config.get('image', '') else "Não"
    buttons_count = len(config.get('buttons', []))
    
    message = "*⚙️ Configurações do Bot*\n\n"
    message += f"*Mensagem de Boas-vindas:*\n{welcome_text}\n\n"
    message += f"*Imagem configurada:* {has_image}\n"
    message += f"*Botões configurados:* {buttons_count}\n\n"
    message += "Selecione o que deseja editar:"
    
    keyboard = [
        [
            InlineKeyboardButton("📝 Editar Texto", callback_data="edit_text"),
            InlineKeyboardButton("📷 Editar Imagem", callback_data="edit_image")
        ],
        [
            InlineKeyboardButton("🔗 Editar Botões", callback_data="edit_buttons"),
            InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")
        ]
    ]
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

@admin_required
async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /logs - visualiza logs recentes do sistema."""
    log_entries = [
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sistema iniciado",
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Verificando mensagens pendentes",
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Administrador acessou o painel"
    ]
    
    message = "*📑 Logs Recentes do Sistema*\n\n"
    
    if log_entries:
        for entry in log_entries:
            message += f"`{entry}`\n"
    else:
        message += "Nenhum log disponível no momento."
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ]),
        parse_mode='Markdown'
    )

# Manipuladores de callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manipula callbacks dos botões inline."""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("⚠️ Você não tem permissão para usar este bot.")
        return
    
    data = query.data
    
    if data == "back_to_menu":
        await show_main_menu(query, context)
    elif data == "send_message":
        await handle_send_message(query, context)
    elif data == "schedule_message":
        await handle_schedule_message(query, context)
    elif data == "manage_groups":
        await handle_manage_groups(query, context)
    elif data == "settings":
        await handle_settings(query, context)
    elif data == "view_logs":
        await handle_view_logs(query, context)
    elif data == "send_to_all":
        context.user_data['send_to_all'] = True
        await query.edit_message_text(
            "📝 Digite a mensagem que deseja enviar para todos os grupos:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancelar", callback_data="back_to_menu")]
            ])
        )
        return WAITING_MESSAGE_TEXT
    elif data == "send_to_specific":
        await handle_send_to_specific(query, context)

async def show_main_menu(query, context):
    """Exibe o menu principal."""
    groups = load_groups()
    config = load_config()
    
    num_groups = len(groups)
    welcome_text = config.get('text', 'Sem texto definido')
    welcome_text_preview = welcome_text[:30] + "..." if len(welcome_text) > 30 else welcome_text
    
    message = f"🤖 *Painel de Administração - Bot Kangaroo* 🤖\n\n"
    message += f"📊 *Estatísticas:*\n"
    message += f"- Grupos cadastrados: {num_groups}\n"
    message += f"- Mensagem de boas-vindas: _{welcome_text_preview}_\n\n"
    message += f"Selecione uma opção abaixo:"
    
    keyboard = [
        [
            InlineKeyboardButton("💬 Enviar Mensagem", callback_data="send_message"),
            InlineKeyboardButton("📅 Agendar Mensagem", callback_data="schedule_message")
        ],
        [
            InlineKeyboardButton("📱 Gerenciar Grupos", callback_data="manage_groups"),
            InlineKeyboardButton("⚙️ Configurações", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📊 Ver Logs", callback_data="view_logs")
        ]
    ]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_send_message(query, context):
    """Manipula o envio de mensagens."""
    groups = load_groups()
    
    if not groups:
        await query.edit_message_text(
            "⚠️ Não há grupos cadastrados para enviar mensagens.\n"
            "Adicione o bot a pelo menos um grupo primeiro.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
            ])
        )
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📱 Enviar para um grupo específico", callback_data="send_to_specific"),
            InlineKeyboardButton("📢 Enviar para todos os grupos", callback_data="send_to_all")
        ],
        [
            InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")
        ]
    ]
    
    await query.edit_message_text(
        "*💬 Enviar Nova Mensagem*\n\n"
        "Selecione uma opção de envio:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_send_to_specific(query, context):
    """Manipula o envio para grupos específicos."""
    groups = load_groups()
    
    keyboard = []
    for group in groups:
        group_id = group.get('chat_id') or group.get('id', 'N/A')
        group_title = group.get('title', 'Grupo sem nome')
        keyboard.append([InlineKeyboardButton(
            f"📱 {group_title}", 
            callback_data=f"select_group_{group_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Voltar", callback_data="send_message")])
    
    await query.edit_message_text(
        "*📱 Selecionar Grupo*\n\n"
        "Escolha o grupo para enviar a mensagem:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_schedule_message(query, context):
    """Manipula o agendamento de mensagens."""
    await query.edit_message_text(
        "*📅 Agendar Mensagem*\n\n"
        "Esta funcionalidade permite agendar mensagens para envio futuro.\n"
        "Em desenvolvimento...",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ]),
        parse_mode='Markdown'
    )

async def handle_manage_groups(query, context):
    """Manipula o gerenciamento de grupos."""
    groups = load_groups()
    
    if not groups:
        message = "⚠️ Não há grupos cadastrados.\n\nO bot precisa ser adicionado a grupos para que eles apareçam aqui."
        keyboard = [[InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]]
    else:
        message = "*📱 Grupos Cadastrados*\n\n"
        
        for i, group in enumerate(groups, 1):
            group_id = group.get('chat_id') or group.get('id', 'N/A')
            group_title = group.get('title', 'Grupo sem nome')
            group_members = group.get('member_count', 0)
            
            message += f"{i}. *{group_title}*\n"
            message += f"   ID: `{group_id}`\n"
            message += f"   Membros: {group_members}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_settings(query, context):
    """Manipula as configurações do bot."""
    config = load_config()
    
    welcome_text = config.get('text', 'Sem texto definido')
    if len(welcome_text) > 100:
        welcome_text = welcome_text[:100] + "..."
        
    has_image = "Sim" if config.get('image', '') else "Não"
    buttons_count = len(config.get('buttons', []))
    
    message = "*⚙️ Configurações do Bot*\n\n"
    message += f"*Mensagem de Boas-vindas:*\n{welcome_text}\n\n"
    message += f"*Imagem configurada:* {has_image}\n"
    message += f"*Botões configurados:* {buttons_count}\n\n"
    message += "Selecione o que deseja editar:"
    
    keyboard = [
        [
            InlineKeyboardButton("📝 Editar Texto", callback_data="edit_text"),
            InlineKeyboardButton("📷 Editar Imagem", callback_data="edit_image")
        ],
        [
            InlineKeyboardButton("🔗 Editar Botões", callback_data="edit_buttons"),
            InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")
        ]
    ]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_view_logs(query, context):
    """Manipula a visualização de logs."""
    log_entries = [
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sistema iniciado",
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Verificando mensagens pendentes",
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Administrador acessou o painel"
    ]
    
    message = "*📑 Logs Recentes do Sistema*\n\n"
    
    if log_entries:
        for entry in log_entries:
            message += f"`{entry}`\n"
    else:
        message += "Nenhum log disponível no momento."
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ]),
        parse_mode='Markdown'
    )

# Manipuladores de mensagens de texto
async def handle_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Manipula o texto da mensagem a ser enviada."""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    message_text = update.message.text
    context.user_data['message_text'] = message_text
    
    # Se for para enviar para todos os grupos
    if context.user_data.get('send_to_all', False):
        groups = load_groups()
        target_groups = [group.get('chat_id') or group.get('id') for group in groups]
        
        # Adiciona a mensagem à lista de pendentes
        success, message_id = add_pending_message(
            message_text=message_text,
            target_groups=target_groups,
            send_now=True,
            title="Mensagem para todos os grupos"
        )
        
        if success:
            await update.message.reply_text(
                f"✅ Mensagem adicionada à fila de envio!\n"
                f"ID da mensagem: {message_id}\n"
                f"Será enviada para {len(target_groups)} grupos.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
                ])
            )
        else:
            await update.message.reply_text(
                "❌ Erro ao adicionar mensagem à fila de envio.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
                ])
            )
    
    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a conversa atual."""
    await update.message.reply_text(
        "❌ Operação cancelada.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="back_to_menu")]
        ])
    )
    return ConversationHandler.END

async def main() -> None:
    """Função principal para iniciar o bot administrativo."""
    # Inicializa o aplicativo
    app = Application.builder().token(TELEGRAM_ADMIN_BOT_TOKEN).build()
    
    # Adiciona manipuladores de comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("send", send_command))
    app.add_handler(CommandHandler("groups", groups_command))
    app.add_handler(CommandHandler("config", config_command))
    app.add_handler(CommandHandler("logs", logs_command))
    
    # Manipulador de conversação para envio de mensagens
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^send_to_all$")],
        states={
            WAITING_MESSAGE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    
    app.add_handler(conv_handler)
    
    # Manipulador de callbacks
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Inicia o polling
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())