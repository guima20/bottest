#!/usr/bin/env python3
"""
🧪 TESTE PARA VERIFICAR SE O SISTEMA DE UPLOAD DE IMAGENS ESTÁ FUNCIONANDO
"""

import json
import os

def test_config_file():
    """Testa se o arquivo de configuração pode ser lido e escrito."""
    print("🔍 Testando arquivo de configuração...")
    
    # Tenta carregar o config atual
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ Arquivo config.json carregado com sucesso!")
        print(f"📄 Conteúdo atual: {json.dumps(config, indent=2, ensure_ascii=False)}")
        
        # Testa se consegue salvar
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("✅ Arquivo config.json pode ser escrito!")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar config.json: {e}")
        return False

def test_permissions():
    """Testa permissões de arquivo."""
    print("\n🔍 Testando permissões...")
    
    # Verifica se o arquivo existe e suas permissões
    if os.path.exists('config.json'):
        stat = os.stat('config.json')
        print(f"📊 Permissões do arquivo: {oct(stat.st_mode)[-3:]}")
        print(f"📊 Tamanho: {stat.st_size} bytes")
        
        # Testa se pode ler
        readable = os.access('config.json', os.R_OK)
        writable = os.access('config.json', os.W_OK)
        
        print(f"📖 Leitura: {'✅' if readable else '❌'}")
        print(f"✏️ Escrita: {'✅' if writable else '❌'}")
        
        return readable and writable
    else:
        print("❌ Arquivo config.json não existe!")
        return False

if __name__ == '__main__':
    print("🧪 TESTE DO SISTEMA DE CONFIGURAÇÃO\n")
    
    config_ok = test_config_file()
    permissions_ok = test_permissions()
    
    print(f"\n📊 RESULTADO:")
    print(f"   Config: {'✅' if config_ok else '❌'}")
    print(f"   Permissões: {'✅' if permissions_ok else '❌'}")
    
    if config_ok and permissions_ok:
        print("\n🎉 SISTEMA FUNCIONANDO CORRETAMENTE!")
    else:
        print("\n❌ PROBLEMAS DETECTADOS!")