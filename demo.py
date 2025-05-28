#!/usr/bin/env python3
"""
Script de demonstração do sistema de mensagens dos bots.
Mostra como adicionar mensagens à fila e como elas seriam processadas.
"""

import json
import datetime
from bot_messages import add_pending_message, load_pending_messages, get_messages_to_send

def demo_message_system():
    """Demonstra o funcionamento do sistema de mensagens."""
    print("🎯 DEMONSTRAÇÃO - Sistema de Mensagens dos Bots")
    print("=" * 50)
    
    # Simula alguns grupos
    demo_groups = [
        {
            "chat_id": "-1001234567890",
            "title": "Grupo Demo 1",
            "type": "supergroup",
            "username": "grupo_demo_1",
            "added_date": datetime.datetime.now().isoformat(),
            "status": "active"
        },
        {
            "chat_id": "-1001234567891", 
            "title": "Grupo Demo 2",
            "type": "supergroup",
            "username": "grupo_demo_2",
            "added_date": datetime.datetime.now().isoformat(),
            "status": "active"
        }
    ]
    
    # Salva os grupos demo
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(demo_groups, f, ensure_ascii=False, indent=4)
    
    print("✅ Grupos demo criados:")
    for group in demo_groups:
        print(f"   - {group['title']} ({group['chat_id']})")
    
    print("\n📝 Adicionando mensagens de demonstração...")
    
    # Mensagem 1: Envio imediato para todos os grupos
    success1, msg_id1 = add_pending_message(
        message_text="🎉 Esta é uma mensagem de demonstração enviada para todos os grupos!",
        target_groups=[group['chat_id'] for group in demo_groups],
        send_now=True,
        title="Mensagem Demo - Todos os Grupos"
    )
    
    if success1:
        print(f"✅ Mensagem {msg_id1} adicionada (envio imediato)")
    
    # Mensagem 2: Envio para grupo específico
    success2, msg_id2 = add_pending_message(
        message_text="📱 Esta mensagem é específica para o Grupo Demo 1!",
        target_groups=[demo_groups[0]['chat_id']],
        send_now=True,
        title="Mensagem Demo - Grupo Específico"
    )
    
    if success2:
        print(f"✅ Mensagem {msg_id2} adicionada (grupo específico)")
    
    # Mensagem 3: Mensagem agendada (para 1 minuto no futuro)
    future_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    success3, msg_id3 = add_pending_message(
        message_text="⏰ Esta é uma mensagem agendada para 1 minuto no futuro!",
        target_groups=[group['chat_id'] for group in demo_groups],
        schedule_time=future_time.isoformat(),
        title="Mensagem Demo - Agendada"
    )
    
    if success3:
        print(f"✅ Mensagem {msg_id3} adicionada (agendada para {future_time.strftime('%H:%M:%S')})")
    
    # Mensagem 4: Com botões
    success4, msg_id4 = add_pending_message(
        message_text="🔗 Esta mensagem tem botões personalizados!",
        target_groups=[demo_groups[1]['chat_id']],
        send_now=True,
        buttons=[
            {"text": "📱 Canal Oficial", "url": "https://t.me/Kangaroo_bot_bot"},
            {"text": "💬 Suporte", "url": "https://t.me/Kangaroo_bot_bot"}
        ],
        title="Mensagem Demo - Com Botões"
    )
    
    if success4:
        print(f"✅ Mensagem {msg_id4} adicionada (com botões)")
    
    print("\n📋 Estado atual das mensagens pendentes:")
    
    # Carrega e exibe mensagens pendentes
    pending_data = load_pending_messages()
    messages = pending_data.get('messages', [])
    
    for message in messages:
        status = message.get('status', 'unknown')
        title = message.get('title', 'Sem título')
        msg_id = message.get('id', 'N/A')
        target_count = len(message.get('target_groups', []))
        
        print(f"   📄 ID {msg_id}: {title}")
        print(f"      Status: {status}")
        print(f"      Grupos alvo: {target_count}")
        
        if 'scheduled_time' in message:
            scheduled = message['scheduled_time']
            print(f"      Agendado para: {scheduled}")
        elif message.get('send_now'):
            print(f"      Envio: Imediato")
        
        print()
    
    print("🔍 Verificando mensagens prontas para envio...")
    
    # Verifica mensagens prontas para envio
    ready_messages = get_messages_to_send()
    
    if ready_messages:
        print(f"✅ {len(ready_messages)} mensagem(s) pronta(s) para envio:")
        for msg in ready_messages:
            print(f"   - ID {msg['id']}: {msg['title']}")
    else:
        print("ℹ️ Nenhuma mensagem pronta para envio no momento")
    
    print("\n" + "=" * 50)
    print("🎯 DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 50)
    print("\nPara ver o sistema em ação:")
    print("1. Configure seus tokens reais no arquivo .env")
    print("2. Inicie o bot principal: python unified_bot.py")
    print("3. Inicie o bot admin: python admin_bot.py")
    print("4. Ou use a GUI: python start_gui.py")
    print("\nAs mensagens demo serão processadas pelo bot principal quando ele estiver rodando.")

def show_config():
    """Mostra a configuração atual do bot."""
    print("\n⚙️ CONFIGURAÇÃO ATUAL DO BOT")
    print("=" * 30)
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"Texto de boas-vindas:")
        print(f"   {config.get('text', 'Não definido')}")
        
        buttons = config.get('buttons', [])
        print(f"\nBotões configurados: {len(buttons)}")
        for i, button in enumerate(buttons, 1):
            print(f"   {i}. {button.get('text', 'Sem texto')} -> {button.get('url', 'Sem URL')}")
        
        if not buttons:
            print("   Nenhum botão configurado")
            
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")

def main():
    """Função principal da demonstração."""
    demo_message_system()
    show_config()

if __name__ == "__main__":
    main()