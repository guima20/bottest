#!/usr/bin/env python3
"""
Teste das funções administrativas sem usar o bot
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

def test_admin_functions():
    """Testa as funções administrativas"""
    print("🧪 TESTANDO FUNÇÕES ADMINISTRATIVAS...")
    
    # 1. Carrega configuração atual
    print("\n1️⃣ Carregando configuração atual...")
    config = load_config()
    print(f"📋 Config carregado: {len(config)} campos")
    
    if 'text' in config:
        print(f"📝 Texto atual: {config['text'][:50]}...")
    
    # 2. Testa alteração de texto
    print("\n2️⃣ Testando alteração de texto...")
    original_text = config.get('text', '')
    new_text = "TESTE ADMIN - " + original_text
    config['text'] = new_text
    
    if save_config(config):
        print("✅ Texto alterado e salvo")
    else:
        print("❌ Falha ao salvar texto")
    
    # 3. Verifica se foi salvo
    print("\n3️⃣ Verificando se foi salvo...")
    config_check = load_config()
    if config_check.get('text') == new_text:
        print("✅ Alteração confirmada no arquivo")
    else:
        print("❌ Alteração NÃO foi salva")
    
    # 4. Testa alteração de botão
    print("\n4️⃣ Testando alteração de botão...")
    if 'buttons' in config_check and len(config_check['buttons']) > 0:
        original_button_text = config_check['buttons'][0]['text']
        config_check['buttons'][0]['text'] = "TESTE BOTÃO - " + original_button_text
        
        if save_config(config_check):
            print("✅ Botão alterado e salvo")
        else:
            print("❌ Falha ao salvar botão")
    
    # 5. Verifica novamente
    print("\n5️⃣ Verificação final...")
    final_config = load_config()
    print(f"📝 Texto final: {final_config.get('text', 'N/A')[:50]}...")
    if 'buttons' in final_config and len(final_config['buttons']) > 0:
        print(f"🔘 Botão 1: {final_config['buttons'][0]['text'][:30]}...")
    
    # 6. Restaura configuração original
    print("\n6️⃣ Restaurando configuração original...")
    config['text'] = original_text
    if 'buttons' in config and len(config['buttons']) > 0:
        config['buttons'][0]['text'] = original_button_text
    
    if save_config(config):
        print("✅ Configuração original restaurada")
    else:
        print("❌ Falha ao restaurar configuração")

if __name__ == "__main__":
    test_admin_functions()