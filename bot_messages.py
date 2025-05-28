#!/usr/bin/env python3
"""
Módulo para gerenciar a comunicação entre o bot administrativo e o bot principal.
Permite que o bot administrativo defina mensagens que serão enviadas pelo bot principal.
"""
import json
import os
import logging
import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Arquivo de mensagens pendentes
PENDING_MESSAGES_FILE = 'pending_messages.json'

def load_pending_messages() -> Dict[str, Any]:
    """Carrega as mensagens pendentes do arquivo."""
    if os.path.exists(PENDING_MESSAGES_FILE):
        try:
            with open(PENDING_MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar mensagens pendentes: {e}")
            return {"last_id": 0, "messages": []}
    return {"last_id": 0, "messages": []}

def save_pending_messages(messages_data: Dict[str, Any]) -> bool:
    """Salva as mensagens pendentes no arquivo."""
    try:
        with open(PENDING_MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar mensagens pendentes: {e}")
        return False

def add_pending_message(
    message_text: str, 
    target_groups: List[str], 
    send_now: bool = False, 
    schedule_time: Optional[str] = None,
    buttons: Optional[List[Dict[str, str]]] = None,
    title: str = "Mensagem do Administrador"
) -> Tuple[bool, int]:
    """
    Adiciona uma nova mensagem à lista de mensagens pendentes.
    
    Args:
        message_text: Texto da mensagem
        target_groups: Lista de IDs dos grupos alvos
        send_now: Se True, a mensagem será marcada para envio imediato
        schedule_time: Data e hora para envio programado (formato ISO)
        buttons: Lista de botões para adicionar à mensagem (opcional)
        title: Título descritivo da mensagem
        
    Returns:
        Tupla (sucesso, id_da_mensagem)
    """
    try:
        # Carrega mensagens pendentes
        messages_data = load_pending_messages()
        
        # Incrementa o último ID
        last_id = messages_data.get("last_id", 0) + 1
        messages_data["last_id"] = last_id
        
        # Cria a nova mensagem
        new_message = {
            "id": last_id,
            "text": message_text,
            "target_groups": target_groups,
            "created_at": datetime.datetime.now().isoformat(),
            "status": "pending",
            "title": title,
        }
        
        # Adiciona informações de agendamento
        if send_now:
            new_message["send_now"] = True
        elif schedule_time:
            new_message["scheduled_time"] = schedule_time
        
        # Adiciona botões se fornecidos
        if buttons:
            new_message["buttons"] = buttons
        
        # Adiciona à lista de mensagens
        messages_data["messages"].append(new_message)
        
        # Salva as alterações
        if save_pending_messages(messages_data):
            logger.info(f"Mensagem {last_id} adicionada com sucesso")
            return True, last_id
        else:
            logger.error("Falha ao salvar mensagens pendentes")
            return False, 0
            
    except Exception as e:
        logger.error(f"Erro ao adicionar mensagem pendente: {e}")
        return False, 0

def mark_message_as_sent(message_id: int) -> bool:
    """Marca uma mensagem como enviada."""
    try:
        # Carrega mensagens pendentes
        messages_data = load_pending_messages()
        
        # Procura a mensagem pelo ID
        for message in messages_data["messages"]:
            if message["id"] == message_id and message["status"] == "pending":
                # Atualiza o status e adiciona timestamp de envio
                message["status"] = "sent"
                message["sent_at"] = datetime.datetime.now().isoformat()
                
                # Salva as alterações
                if save_pending_messages(messages_data):
                    logger.info(f"Mensagem {message_id} marcada como enviada")
                    return True
                else:
                    logger.error(f"Falha ao salvar status da mensagem {message_id}")
                    return False
        
        logger.warning(f"Mensagem {message_id} não encontrada ou já enviada")
        return False
            
    except Exception as e:
        logger.error(f"Erro ao marcar mensagem como enviada: {e}")
        return False

def get_messages_to_send() -> List[Dict[str, Any]]:
    """
    Retorna a lista de mensagens pendentes que devem ser enviadas agora.
    Inclui mensagens marcadas como 'send_now' e mensagens agendadas para o momento atual.
    """
    try:
        # Carrega mensagens pendentes
        messages_data = load_pending_messages()
        messages_to_send = []
        now = datetime.datetime.now()
        
        # Filtra mensagens pendentes
        for message in messages_data["messages"]:
            # Ignora mensagens já enviadas
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
            
    except Exception as e:
        logger.error(f"Erro ao obter mensagens para enviar: {e}")
        return []