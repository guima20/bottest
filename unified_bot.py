#!/usr/bin/env python3
"""
Bot Kangaroo - Bot principal para interação com grupos do Telegram.
Processa mensagens agendadas pelo bot administrativo.
"""
import os
import json
import logging
import asyncio
import datetime
from typing import Dict, List, Any, Optional, Union

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, 
                         CallbackQueryHandler, ContextTypes, filters)
from telegram.error import TelegramError

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega o token do bot do ambiente ou usa o valor padrão
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7862546836:AAHtlgCVOdrI5saF0Ca4ruX1c56FyVHUQAE')

# Arquivos de configuração
CONFIG_FILE = 'config.json'
GROUPS_FILE = 'groups.json'
PENDING_MESSAGES_FILE = 'pending_messages.json'

# Intervalo de verificação de mensagens pendentes (em segundos)
CHECK_INTERVAL = 60

# Funções para manipulação de arquivos
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

def load_groups() -> List[Dict[str, Any]]:
    """Carrega a lista de grupos cadastrados."""
    data = load_json_file(GROUPS_FILE, [])
    return data if isinstance(data, list) else []

def save_groups(groups: List[Dict[str, Any]]) -> bool:
    """Salva a lista de grupos cadastrados."""
    return save_json_file(GROUPS_FILE, groups)

def normalize_group_id(group_id: Union[int, str]) -> str:
    """Normaliza o ID do grupo para formato de string."""
    return str(group_id)

def load_pending_messages() -> Dict[str, Any]:
    """Carrega as mensagens pendentes."""
    return load_json_file(PENDING_MESSAGES_FILE, {"last_id": 0, "messages": []})

def save_pending_messages(data: Dict[str, Any]) -> bool:
    """Salva as mensagens pendentes."""
    return save_json_file(PENDING_MESSAGES_FILE, data)

def mark_message_as_sent(message_id: int) -> bool:
    """Marca uma mensagem como enviada."""
    data = load_pending_messages()
    for message in data["messages"]:
        if message["id"] == message_id and message["status"] == "pending":
            message["status"] = "sent"
            message["sent_at"] = datetime.datetime.now().isoformat()
            save_pending_messages(data)
            return True
    return False

def get_messages_to_send() -> List[Dict[str, Any]]:
    """
    Retorna a lista de mensagens pendentes que devem ser enviadas agora.
    Inclui mensagens marcadas como 'send_now' e mensagens agendadas para o momento atual.
    """
    data = load_pending_messages()
    messages_to_send = []
    now = datetime.datetime.now()
    
    for message in data["messages"]:
        if message["status"] != "pending":
            continue
            
        # Verifica se a mensagem deve ser enviada imediatamente
        if message.get("send_now", False):
            messages_to_send.append(message)
            continue
            
        # Verifica se é hora de enviar uma mensagem agendada
        if "scheduled_time" in message:
            try:
                scheduled_time = datetime.datetime.fromisoformat(message["scheduled_time"])
                if now >= scheduled_time:
                    messages_to_send.append(message)
            except (ValueError, TypeError) as e:
                logger.error(f"Erro ao processar horário agendado: {e}")
                
    return messages_to_send

# Manipuladores de comandos e mensagens
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manipula o comando /start.
    Registra o grupo se for um grupo novo e envia mensagem de boas-vindas.
    """
    chat = update.effective_chat
    
    # Ignora mensagens que não são de grupos
    if chat.type not in ['group', 'supergroup']:
        await update.message.reply_text(
            "Este bot foi projetado para funcionar em grupos. "
            "Adicione-me a um grupo para começar!"
        )
        return
    
    # Registra o grupo se ainda não estiver registrado
    groups = load_groups()
    chat_id = normalize_group_id(chat.id)
    
    # Verifica se o grupo já está registrado
    group_exists = False
    for group in groups:
        if normalize_group_id(group.get('chat_id') or group.get('id', '')) == chat_id:
            group_exists = True
            # Atualiza informações do grupo
            group['title'] = chat.title
            group['type'] = chat.type
            group['username'] = chat.username
            group['last_updated'] = datetime.datetime.now().isoformat()
            break
    
    # Se o grupo não existir, adiciona à lista
    if not group_exists:
        new_group = {
            'chat_id': chat_id,
            'title': chat.title,
            'type': chat.type,
            'username': chat.username,
            'added_date': datetime.datetime.now().isoformat(),
            'last_updated': datetime.datetime.now().isoformat(),
            'status': 'active',
            'added_by': {
                'id': update.effective_user.id,
                'name': update.effective_user.full_name,
                'username': update.effective_user.username
            }
        }
        groups.append(new_group)
    
    # Salva a lista atualizada
    save_groups(groups)
    
    # Envia mensagem de boas-vindas com configuração atual
    config = load_config()
    welcome_text = config.get('text', 'Bem-vindo ao Bot Kangaroo!')
    
    # Prepara os botões inline
    buttons = config.get('buttons', [])
    keyboard = []
    row = []
    
    for i, button in enumerate(buttons):
        btn = InlineKeyboardButton(
            text=button.get('text', 'Botão'),
            url=button.get('url', 'https://t.me/Kangaroo_bot_bot')
        )
        
        # Cria uma nova linha a cada 2 botões
        if i % 2 == 0 and i > 0:
            keyboard.append(row)
            row = []
        
        row.append(btn)
    
    # Adiciona a última linha se houver botões restantes
    if row:
        keyboard.append(row)
    
    # Envia a mensagem com ou sem botões
    if keyboard:
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(welcome_text)
    
    logger.info(f"Grupo registrado/atualizado: {chat.title} ({chat_id})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe mensagem de ajuda."""
    await update.message.reply_text(
        "🤖 *Bot Kangaroo* 🤖\n\n"
        "Este bot gerencia mensagens e notificações para este grupo.\n\n"
        "*Comandos disponíveis:*\n"
        "/start - Registra o grupo e exibe mensagem de boas-vindas\n"
        "/help - Exibe esta mensagem de ajuda\n\n"
        "Para mais informações, entre em contato com o administrador.",
        parse_mode='Markdown'
    )

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manipula a entrada de novos membros no grupo."""
    chat = update.effective_chat
    new_members = update.message.new_chat_members
    
    # Verifica se o bot está entre os novos membros
    bot_added = False
    for member in new_members:
        if member.id == context.bot.id:
            bot_added = True
            break
    
    # Se o bot foi adicionado, registra o grupo e envia mensagem de boas-vindas
    if bot_added:
        # Simula o comando /start
        await start_command(update, context)

async def process_pending_messages(app: Application) -> None:
    """
    Processa mensagens pendentes periodicamente.
    Verifica mensagens agendadas e as envia quando chegar o momento.
    """
    while True:
        try:
            logger.info("Verificando mensagens pendentes...")
            messages = get_messages_to_send()
            
            if messages:
                logger.info(f"Encontradas {len(messages)} mensagens para enviar")
                
                for message in messages:
                    message_id = message["id"]
                    message_text = message["text"]
                    target_groups = message["target_groups"]
                    buttons = message.get("buttons", [])
                    
                    # Prepara os botões inline
                    keyboard = []
                    row = []
                    
                    for i, button in enumerate(buttons):
                        # Verifica o tipo de botão (URL ou callback)
                        if "url" in button:
                            btn = InlineKeyboardButton(
                                text=button.get('text', 'Botão'),
                                url=button.get('url')
                            )
                        elif "callback_data" in button:
                            btn = InlineKeyboardButton(
                                text=button.get('text', 'Botão'),
                                callback_data=button.get('callback_data')
                            )
                        else:
                            continue
                        
                        # Cria uma nova linha a cada 2 botões
                        if i % 2 == 0 and i > 0:
                            keyboard.append(row)
                            row = []
                        
                        row.append(btn)
                    
                    # Adiciona a última linha se houver botões restantes
                    if row:
                        keyboard.append(row)
                    
                    # Prepara o markup de teclado se houver botões
                    markup = InlineKeyboardMarkup(keyboard) if keyboard else None
                    
                    # Envia a mensagem para cada grupo alvo
                    for group_id in target_groups:
                        try:
                            await app.bot.send_message(
                                chat_id=group_id,
                                text=message_text,
                                reply_markup=markup,
                                parse_mode='Markdown'
                            )
                            logger.info(f"Mensagem {message_id} enviada para o grupo {group_id}")
                        except Exception as e:
                            logger.error(f"Erro ao enviar mensagem para o grupo {group_id}: {e}")
                    
                    # Marca a mensagem como enviada
                    mark_message_as_sent(message_id)
            
            # Aguarda o intervalo definido antes da próxima verificação
            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Erro ao processar mensagens pendentes: {e}")
            await asyncio.sleep(CHECK_INTERVAL)

async def main() -> None:
    """Função principal para iniciar o bot."""
    # Inicializa o aplicativo
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona manipuladores de comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Manipulador para novos membros
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    
    # Inicia o processamento de mensagens pendentes em segundo plano
    asyncio.create_task(process_pending_messages(app))
    
    # Inicia o polling
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())