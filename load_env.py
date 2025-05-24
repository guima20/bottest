#!/usr/bin/env python3
"""
Script para carregar variáveis de ambiente de um arquivo .env
Útil para desenvolvimento local
"""

import os

def load_env_file(filename='.env'):
    """Carrega variáveis de ambiente de um arquivo"""
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip('"\'')
        print(f"✅ Variáveis carregadas de {filename}")
        return True
    except FileNotFoundError:
        print(f"❌ Arquivo {filename} não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro ao carregar {filename}: {e}")
        return False

if __name__ == '__main__':
    load_env_file()
    
    # Mostra variáveis carregadas
    env_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_ADMIN_BOT_TOKEN', 'ADMIN_IDS']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'TOKEN' in var:
                masked = value[:10] + '...' + value[-10:] if len(value) > 20 else value
                print(f"{var}: {masked}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: não configurado")