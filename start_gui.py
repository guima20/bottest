#!/usr/bin/env python3
"""
Script de inicialização para o sistema de bots Telegram com interface gráfica.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    try:
        import telegram
        import dotenv
        return True
    except ImportError as e:
        return False, str(e)

def install_dependencies():
    """Instala as dependências necessárias."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Função principal de inicialização."""
    print("🤖 Iniciando Sistema de Bots Telegram - Kangaroo")
    print("=" * 50)
    
    # Verifica dependências
    deps_check = check_dependencies()
    if deps_check != True:
        print("❌ Dependências não encontradas. Tentando instalar...")
        if install_dependencies():
            print("✅ Dependências instaladas com sucesso!")
        else:
            print("❌ Erro ao instalar dependências. Instale manualmente:")
            print("pip install -r requirements.txt")
            return
    
    # Verifica se os arquivos necessários existem
    required_files = [
        'unified_bot.py',
        'admin_bot.py', 
        'bot_messages.py',
        'gui_manager.py',
        'config.json',
        'groups.json',
        'pending_messages.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos necessários não encontrados: {', '.join(missing_files)}")
        return
    
    print("✅ Todos os arquivos necessários encontrados!")
    print("🚀 Iniciando interface gráfica...")
    
    # Inicia a interface gráfica
    try:
        from gui_manager import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Erro ao iniciar interface gráfica: {e}")
        
        # Fallback para interface de linha de comando
        print("\n🔄 Tentando inicialização alternativa...")
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        choice = messagebox.askyesno(
            "Erro na Interface",
            "Erro ao iniciar a interface gráfica.\n\n"
            "Deseja tentar iniciar apenas os bots via linha de comando?\n\n"
            "Sim = Iniciar bots\n"
            "Não = Sair"
        )
        
        if choice:
            print("🤖 Iniciando bots via linha de comando...")
            try:
                # Inicia o bot principal
                print("Iniciando bot principal...")
                subprocess.Popen([sys.executable, "unified_bot.py"])
                
                # Inicia o bot administrativo
                print("Iniciando bot administrativo...")
                subprocess.Popen([sys.executable, "admin_bot.py"])
                
                print("✅ Bots iniciados com sucesso!")
                print("Para parar os bots, use Ctrl+C ou feche este terminal.")
                
                # Mantém o script rodando
                try:
                    while True:
                        pass
                except KeyboardInterrupt:
                    print("\n⏹️ Parando bots...")
                    
            except Exception as e:
                print(f"❌ Erro ao iniciar bots: {e}")
        
        root.destroy()

if __name__ == "__main__":
    main()