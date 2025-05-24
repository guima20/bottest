#!/usr/bin/env python3
"""
Teste das funções administrativas do bot unificado
"""

import json
import os

# Carrega variáveis de ambiente
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    pass

CONFIG_FILE = 'config.json'

def load_config():
    """Carrega configuração do arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo {CONFIG_FILE} não encontrado")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return {}

def save_config(config):
    """Salva configuração no arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("✅ Configuração salva com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False

def test_admin_commands():
    """Simula os comandos administrativos"""
    print("🧪 TESTANDO COMANDOS ADMINISTRATIVOS DO BOT UNIFICADO...")
    
    # 1. Mostra configuração atual
    print("\n1️⃣ Configuração atual:")
    config = load_config()
    print(f"📷 Imagem: {config.get('image', 'N/A')}")
    print(f"📝 Texto: {config.get('text', 'N/A')[:50]}...")
    buttons = config.get('buttons', [])
    for i, button in enumerate(buttons, 1):
        print(f"🔘 Botão {i}: {button.get('text', 'N/A')} → {button.get('url', 'N/A')}")
    
    # 2. Simula /set_text
    print("\n2️⃣ Simulando comando /set_text...")
    original_text = config.get('text', '')
    new_text = "🎉 TEXTO ALTERADO VIA BOT UNIFICADO! 🎉"
    config['text'] = new_text
    
    if save_config(config):
        print(f"✅ Comando /set_text executado: {new_text}")
    else:
        print("❌ Falha no comando /set_text")
    
    # 3. Simula /set_button
    print("\n3️⃣ Simulando comando /set_button 1...")
    if 'buttons' not in config:
        config['buttons'] = []
    
    while len(config['buttons']) < 4:
        config['buttons'].append({"text": "Botão", "url": "https://example.com"})
    
    original_button = config['buttons'][0].copy()
    config['buttons'][0] = {
        "text": "🚀 BOTÃO ALTERADO VIA UNIFICADO",
        "url": "https://novo-link-unificado.com"
    }
    
    if save_config(config):
        print(f"✅ Comando /set_button executado: {config['buttons'][0]['text']}")
    else:
        print("❌ Falha no comando /set_button")
    
    # 4. Simula /set_image
    print("\n4️⃣ Simulando comando /set_image...")
    original_image = config.get('image', '')
    new_image = "https://nova-imagem-unificada.jpg"
    config['image'] = new_image
    
    if save_config(config):
        print(f"✅ Comando /set_image executado: {new_image}")
    else:
        print("❌ Falha no comando /set_image")
    
    # 5. Verifica se tudo foi salvo
    print("\n5️⃣ Verificando se as alterações foram salvas...")
    config_check = load_config()
    
    if config_check.get('text') == new_text:
        print("✅ Texto salvo corretamente")
    else:
        print("❌ Texto NÃO foi salvo")
    
    if config_check.get('image') == new_image:
        print("✅ Imagem salva corretamente")
    else:
        print("❌ Imagem NÃO foi salva")
    
    if (config_check.get('buttons', [{}])[0].get('text') == "🚀 BOTÃO ALTERADO VIA UNIFICADO"):
        print("✅ Botão salvo corretamente")
    else:
        print("❌ Botão NÃO foi salvo")
    
    # 6. Restaura configuração original
    print("\n6️⃣ Restaurando configuração original...")
    config['text'] = original_text
    config['image'] = original_image
    config['buttons'][0] = original_button
    
    if save_config(config):
        print("✅ Configuração original restaurada")
    else:
        print("❌ Falha ao restaurar configuração")
    
    print("\n🎯 TESTE CONCLUÍDO!")

if __name__ == "__main__":
    test_admin_commands()