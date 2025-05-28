#!/usr/bin/env python3
"""
Interface Gráfica para Gerenciamento dos Bots Telegram
Permite controlar e monitorar os bots Kangaroo e Administrativo através de uma GUI tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import threading
import subprocess
import datetime
import asyncio
from typing import Dict, List, Any, Optional
import queue
import time

# Importa funções de gerenciamento
from bot_messages import add_pending_message, load_pending_messages, get_messages_to_send

class BotManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Kangaroo - Gerenciador")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis de controle
        self.main_bot_process = None
        self.admin_bot_process = None
        self.log_queue = queue.Queue()
        
        # Configuração de estilo
        self.setup_styles()
        
        # Criação da interface
        self.create_widgets()
        
        # Inicia o monitoramento de logs
        self.start_log_monitoring()
        
        # Carrega dados iniciais
        self.refresh_data()
        
    def setup_styles(self):
        """Configura os estilos da interface."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Error.TLabel', foreground='#e74c3c')
        style.configure('Warning.TLabel', foreground='#f39c12')
        
    def create_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🤖 Bot Kangaroo - Painel de Controle", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de controle dos bots
        self.create_bot_control_frame(main_frame)
        
        # Frame de estatísticas
        self.create_stats_frame(main_frame)
        
        # Notebook para abas
        self.create_notebook(main_frame)
        
        # Frame de logs
        self.create_log_frame(main_frame)
        
    def create_bot_control_frame(self, parent):
        """Cria o frame de controle dos bots."""
        control_frame = ttk.LabelFrame(parent, text="Controle dos Bots", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Status dos bots
        ttk.Label(control_frame, text="Bot Principal:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.main_bot_status = ttk.Label(control_frame, text="Parado", style='Error.TLabel')
        self.main_bot_status.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(control_frame, text="Bot Admin:", style='Subtitle.TLabel').grid(row=1, column=0, sticky=tk.W)
        self.admin_bot_status = ttk.Label(control_frame, text="Parado", style='Error.TLabel')
        self.admin_bot_status.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Botões de controle
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.start_main_btn = ttk.Button(button_frame, text="Iniciar Bot Principal", 
                                        command=self.start_main_bot)
        self.start_main_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_main_btn = ttk.Button(button_frame, text="Parar Bot Principal", 
                                       command=self.stop_main_bot, state='disabled')
        self.stop_main_btn.grid(row=0, column=1, padx=5)
        
        self.start_admin_btn = ttk.Button(button_frame, text="Iniciar Bot Admin", 
                                         command=self.start_admin_bot)
        self.start_admin_btn.grid(row=1, column=0, padx=(0, 5), pady=(5, 0))
        
        self.stop_admin_btn = ttk.Button(button_frame, text="Parar Bot Admin", 
                                        command=self.stop_admin_bot, state='disabled')
        self.stop_admin_btn.grid(row=1, column=1, padx=5, pady=(5, 0))
        
        # Botão de atualização
        ttk.Button(button_frame, text="🔄 Atualizar", 
                  command=self.refresh_data).grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
    def create_stats_frame(self, parent):
        """Cria o frame de estatísticas."""
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas", padding="10")
        stats_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), padx=(10, 0))
        stats_frame.columnconfigure(1, weight=1)
        
        # Labels de estatísticas
        ttk.Label(stats_frame, text="Grupos Cadastrados:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.groups_count_label = ttk.Label(stats_frame, text="0")
        self.groups_count_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Mensagens Pendentes:", style='Subtitle.TLabel').grid(row=1, column=0, sticky=tk.W)
        self.pending_messages_label = ttk.Label(stats_frame, text="0")
        self.pending_messages_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Última Verificação:", style='Subtitle.TLabel').grid(row=2, column=0, sticky=tk.W)
        self.last_check_label = ttk.Label(stats_frame, text="Nunca")
        self.last_check_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
    def create_notebook(self, parent):
        """Cria o notebook com as abas principais."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Aba de Grupos
        self.create_groups_tab()
        
        # Aba de Mensagens
        self.create_messages_tab()
        
        # Aba de Configurações
        self.create_config_tab()
        
        # Aba de Mensagens Pendentes
        self.create_pending_messages_tab()
        
    def create_groups_tab(self):
        """Cria a aba de gerenciamento de grupos."""
        groups_frame = ttk.Frame(self.notebook)
        self.notebook.add(groups_frame, text="📱 Grupos")
        
        # Frame de lista de grupos
        list_frame = ttk.LabelFrame(groups_frame, text="Grupos Cadastrados", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para grupos
        columns = ('ID', 'Nome', 'Tipo', 'Membros', 'Data Adição')
        self.groups_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Configuração das colunas
        for col in columns:
            self.groups_tree.heading(col, text=col)
            self.groups_tree.column(col, width=150)
        
        # Scrollbar para a treeview
        groups_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.groups_tree.yview)
        self.groups_tree.configure(yscrollcommand=groups_scrollbar.set)
        
        self.groups_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        groups_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de botões para grupos
        groups_buttons_frame = ttk.Frame(groups_frame)
        groups_buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(groups_buttons_frame, text="🔄 Atualizar Lista", 
                  command=self.refresh_groups).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(groups_buttons_frame, text="❌ Remover Grupo", 
                  command=self.remove_selected_group).pack(side=tk.LEFT, padx=5)
        ttk.Button(groups_buttons_frame, text="📊 Detalhes", 
                  command=self.show_group_details).pack(side=tk.LEFT, padx=5)
        
    def create_messages_tab(self):
        """Cria a aba de envio de mensagens."""
        messages_frame = ttk.Frame(self.notebook)
        self.notebook.add(messages_frame, text="💬 Mensagens")
        
        # Frame de envio de mensagem
        send_frame = ttk.LabelFrame(messages_frame, text="Enviar Nova Mensagem", padding="10")
        send_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Seleção de destino
        dest_frame = ttk.Frame(send_frame)
        dest_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dest_frame, text="Destino:", style='Subtitle.TLabel').pack(side=tk.LEFT)
        
        self.dest_var = tk.StringVar(value="all")
        ttk.Radiobutton(dest_frame, text="Todos os grupos", variable=self.dest_var, 
                       value="all").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(dest_frame, text="Grupo específico", variable=self.dest_var, 
                       value="specific").pack(side=tk.LEFT, padx=(10, 0))
        
        # Seleção de grupo específico
        specific_frame = ttk.Frame(send_frame)
        specific_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(specific_frame, text="Grupo:").pack(side=tk.LEFT)
        self.group_combo = ttk.Combobox(specific_frame, state="readonly")
        self.group_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Área de texto da mensagem
        ttk.Label(send_frame, text="Mensagem:", style='Subtitle.TLabel').pack(anchor=tk.W)
        self.message_text = scrolledtext.ScrolledText(send_frame, height=8, wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Opções de envio
        options_frame = ttk.Frame(send_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.send_now_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enviar imediatamente", 
                       variable=self.send_now_var).pack(side=tk.LEFT)
        
        # Botões de ação
        buttons_frame = ttk.Frame(send_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="📤 Enviar Mensagem", 
                  command=self.send_message).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="📅 Agendar Mensagem", 
                  command=self.schedule_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🧹 Limpar", 
                  command=self.clear_message).pack(side=tk.LEFT, padx=5)
        
    def create_config_tab(self):
        """Cria a aba de configurações."""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configurações")
        
        # Frame de configuração de boas-vindas
        welcome_frame = ttk.LabelFrame(config_frame, text="Mensagem de Boas-vindas", padding="10")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto de boas-vindas
        ttk.Label(welcome_frame, text="Texto:", style='Subtitle.TLabel').pack(anchor=tk.W)
        self.welcome_text = scrolledtext.ScrolledText(welcome_frame, height=6, wrap=tk.WORD)
        self.welcome_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Frame de botões da mensagem de boas-vindas
        buttons_config_frame = ttk.LabelFrame(welcome_frame, text="Botões", padding="5")
        buttons_config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Lista de botões
        self.buttons_listbox = tk.Listbox(buttons_config_frame, height=4)
        self.buttons_listbox.pack(fill=tk.X, pady=(0, 5))
        
        # Frame para adicionar botões
        add_button_frame = ttk.Frame(buttons_config_frame)
        add_button_frame.pack(fill=tk.X)
        
        ttk.Label(add_button_frame, text="Texto:").grid(row=0, column=0, sticky=tk.W)
        self.button_text_entry = ttk.Entry(add_button_frame)
        self.button_text_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(add_button_frame, text="URL:").grid(row=1, column=0, sticky=tk.W)
        self.button_url_entry = ttk.Entry(add_button_frame)
        self.button_url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        add_button_frame.columnconfigure(1, weight=1)
        
        button_actions_frame = ttk.Frame(buttons_config_frame)
        button_actions_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_actions_frame, text="➕ Adicionar", 
                  command=self.add_button).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_actions_frame, text="❌ Remover", 
                  command=self.remove_button).pack(side=tk.LEFT, padx=5)
        
        # Botões de configuração
        config_buttons_frame = ttk.Frame(welcome_frame)
        config_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(config_buttons_frame, text="💾 Salvar Configurações", 
                  command=self.save_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons_frame, text="🔄 Recarregar", 
                  command=self.load_config).pack(side=tk.LEFT, padx=5)
        
    def create_pending_messages_tab(self):
        """Cria a aba de mensagens pendentes."""
        pending_frame = ttk.Frame(self.notebook)
        self.notebook.add(pending_frame, text="📋 Pendentes")
        
        # Frame de lista de mensagens pendentes
        list_frame = ttk.LabelFrame(pending_frame, text="Mensagens Pendentes", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mensagens pendentes
        columns = ('ID', 'Título', 'Status', 'Criado em', 'Agendado para')
        self.pending_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Configuração das colunas
        for col in columns:
            self.pending_tree.heading(col, text=col)
            self.pending_tree.column(col, width=120)
        
        # Scrollbar para a treeview
        pending_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.pending_tree.yview)
        self.pending_tree.configure(yscrollcommand=pending_scrollbar.set)
        
        self.pending_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pending_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de botões para mensagens pendentes
        pending_buttons_frame = ttk.Frame(pending_frame)
        pending_buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(pending_buttons_frame, text="🔄 Atualizar Lista", 
                  command=self.refresh_pending_messages).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pending_buttons_frame, text="👁️ Ver Detalhes", 
                  command=self.show_message_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(pending_buttons_frame, text="❌ Cancelar Mensagem", 
                  command=self.cancel_pending_message).pack(side=tk.LEFT, padx=5)
        
    def create_log_frame(self, parent):
        """Cria o frame de logs."""
        log_frame = ttk.LabelFrame(parent, text="Logs do Sistema", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Área de texto para logs
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botões de log
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(log_buttons_frame, text="🧹 Limpar Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons_frame, text="💾 Salvar Logs", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
    def start_main_bot(self):
        """Inicia o bot principal."""
        try:
            self.main_bot_process = subprocess.Popen(['python', 'unified_bot.py'])
            self.main_bot_status.config(text="Executando", style='Success.TLabel')
            self.start_main_btn.config(state='disabled')
            self.stop_main_btn.config(state='normal')
            self.log_message("✅ Bot principal iniciado com sucesso")
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar bot principal: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar bot principal: {e}")
    
    def stop_main_bot(self):
        """Para o bot principal."""
        if self.main_bot_process:
            self.main_bot_process.terminate()
            self.main_bot_process = None
            self.main_bot_status.config(text="Parado", style='Error.TLabel')
            self.start_main_btn.config(state='normal')
            self.stop_main_btn.config(state='disabled')
            self.log_message("⏹️ Bot principal parado")
    
    def start_admin_bot(self):
        """Inicia o bot administrativo."""
        try:
            self.admin_bot_process = subprocess.Popen(['python', 'admin_bot.py'])
            self.admin_bot_status.config(text="Executando", style='Success.TLabel')
            self.start_admin_btn.config(state='disabled')
            self.stop_admin_btn.config(state='normal')
            self.log_message("✅ Bot administrativo iniciado com sucesso")
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar bot administrativo: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar bot administrativo: {e}")
    
    def stop_admin_bot(self):
        """Para o bot administrativo."""
        if self.admin_bot_process:
            self.admin_bot_process.terminate()
            self.admin_bot_process = None
            self.admin_bot_status.config(text="Parado", style='Error.TLabel')
            self.start_admin_btn.config(state='normal')
            self.stop_admin_btn.config(state='disabled')
            self.log_message("⏹️ Bot administrativo parado")
    
    def refresh_data(self):
        """Atualiza todos os dados da interface."""
        self.refresh_groups()
        self.refresh_pending_messages()
        self.load_config()
        self.update_stats()
        self.log_message("🔄 Dados atualizados")
    
    def refresh_groups(self):
        """Atualiza a lista de grupos."""
        # Limpa a treeview
        for item in self.groups_tree.get_children():
            self.groups_tree.delete(item)
        
        # Carrega grupos do arquivo
        try:
            if os.path.exists('groups.json'):
                with open('groups.json', 'r', encoding='utf-8') as f:
                    groups = json.load(f)
                
                # Atualiza o combobox de grupos
                group_names = []
                
                for group in groups:
                    group_id = group.get('chat_id', group.get('id', 'N/A'))
                    title = group.get('title', 'Sem nome')
                    group_type = group.get('type', 'N/A')
                    members = group.get('member_count', 0)
                    added_date = group.get('added_date', 'N/A')
                    
                    # Adiciona à treeview
                    self.groups_tree.insert('', 'end', values=(
                        group_id, title, group_type, members, added_date
                    ))
                    
                    # Adiciona ao combobox
                    group_names.append(f"{title} ({group_id})")
                
                self.group_combo['values'] = group_names
                if group_names:
                    self.group_combo.current(0)
                    
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar grupos: {e}")
    
    def refresh_pending_messages(self):
        """Atualiza a lista de mensagens pendentes."""
        # Limpa a treeview
        for item in self.pending_tree.get_children():
            self.pending_tree.delete(item)
        
        try:
            pending_data = load_pending_messages()
            messages = pending_data.get('messages', [])
            
            for message in messages:
                msg_id = message.get('id', 'N/A')
                title = message.get('title', 'Sem título')
                status = message.get('status', 'N/A')
                created_at = message.get('created_at', 'N/A')
                scheduled_time = message.get('scheduled_time', 'Imediato')
                
                # Formata as datas
                if created_at != 'N/A':
                    try:
                        created_dt = datetime.datetime.fromisoformat(created_at)
                        created_at = created_dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                
                if scheduled_time != 'Imediato' and scheduled_time:
                    try:
                        scheduled_dt = datetime.datetime.fromisoformat(scheduled_time)
                        scheduled_time = scheduled_dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                
                self.pending_tree.insert('', 'end', values=(
                    msg_id, title, status, created_at, scheduled_time
                ))
                
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar mensagens pendentes: {e}")
    
    def update_stats(self):
        """Atualiza as estatísticas."""
        try:
            # Conta grupos
            groups_count = 0
            if os.path.exists('groups.json'):
                with open('groups.json', 'r', encoding='utf-8') as f:
                    groups = json.load(f)
                    groups_count = len(groups)
            
            self.groups_count_label.config(text=str(groups_count))
            
            # Conta mensagens pendentes
            pending_data = load_pending_messages()
            pending_count = len([m for m in pending_data.get('messages', []) if m.get('status') == 'pending'])
            self.pending_messages_label.config(text=str(pending_count))
            
            # Atualiza última verificação
            self.last_check_label.config(text=datetime.datetime.now().strftime('%H:%M:%S'))
            
        except Exception as e:
            self.log_message(f"❌ Erro ao atualizar estatísticas: {e}")
    
    def load_config(self):
        """Carrega as configurações do bot."""
        try:
            config = {}
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # Carrega texto de boas-vindas
            welcome_text = config.get('text', 'Bem-vindo ao Bot Kangaroo!')
            self.welcome_text.delete(1.0, tk.END)
            self.welcome_text.insert(1.0, welcome_text)
            
            # Carrega botões
            self.buttons_listbox.delete(0, tk.END)
            buttons = config.get('buttons', [])
            for button in buttons:
                text = button.get('text', 'Botão')
                url = button.get('url', '')
                self.buttons_listbox.insert(tk.END, f"{text} -> {url}")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar configurações: {e}")
    
    def save_config(self):
        """Salva as configurações do bot."""
        try:
            config = {
                'text': self.welcome_text.get(1.0, tk.END).strip(),
                'buttons': [],
                'image': ''
            }
            
            # Salva botões
            for i in range(self.buttons_listbox.size()):
                button_text = self.buttons_listbox.get(i)
                if ' -> ' in button_text:
                    text, url = button_text.split(' -> ', 1)
                    config['buttons'].append({'text': text, 'url': url})
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            self.log_message("✅ Configurações salvas com sucesso")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def add_button(self):
        """Adiciona um novo botão à configuração."""
        text = self.button_text_entry.get().strip()
        url = self.button_url_entry.get().strip()
        
        if not text or not url:
            messagebox.showwarning("Aviso", "Preencha o texto e a URL do botão")
            return
        
        self.buttons_listbox.insert(tk.END, f"{text} -> {url}")
        self.button_text_entry.delete(0, tk.END)
        self.button_url_entry.delete(0, tk.END)
    
    def remove_button(self):
        """Remove o botão selecionado."""
        selection = self.buttons_listbox.curselection()
        if selection:
            self.buttons_listbox.delete(selection[0])
    
    def send_message(self):
        """Envia uma mensagem através do sistema."""
        message_text = self.message_text.get(1.0, tk.END).strip()
        
        if not message_text:
            messagebox.showwarning("Aviso", "Digite uma mensagem para enviar")
            return
        
        try:
            # Determina grupos alvo
            if self.dest_var.get() == "all":
                # Carrega todos os grupos
                if os.path.exists('groups.json'):
                    with open('groups.json', 'r', encoding='utf-8') as f:
                        groups = json.load(f)
                    target_groups = [group.get('chat_id', group.get('id')) for group in groups]
                else:
                    target_groups = []
            else:
                # Grupo específico
                selected = self.group_combo.get()
                if not selected:
                    messagebox.showwarning("Aviso", "Selecione um grupo")
                    return
                
                # Extrai o ID do grupo da seleção
                group_id = selected.split('(')[-1].rstrip(')')
                target_groups = [group_id]
            
            if not target_groups:
                messagebox.showwarning("Aviso", "Nenhum grupo disponível para envio")
                return
            
            # Adiciona mensagem à fila
            success, msg_id = add_pending_message(
                message_text=message_text,
                target_groups=target_groups,
                send_now=self.send_now_var.get(),
                title="Mensagem via GUI"
            )
            
            if success:
                self.log_message(f"✅ Mensagem {msg_id} adicionada à fila de envio")
                messagebox.showinfo("Sucesso", f"Mensagem adicionada à fila! ID: {msg_id}")
                self.refresh_pending_messages()
                self.clear_message()
            else:
                self.log_message("❌ Erro ao adicionar mensagem à fila")
                messagebox.showerror("Erro", "Erro ao adicionar mensagem à fila")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao enviar mensagem: {e}")
            messagebox.showerror("Erro", f"Erro ao enviar mensagem: {e}")
    
    def schedule_message(self):
        """Abre diálogo para agendar mensagem."""
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de agendamento em desenvolvimento")
    
    def clear_message(self):
        """Limpa o campo de mensagem."""
        self.message_text.delete(1.0, tk.END)
    
    def remove_selected_group(self):
        """Remove o grupo selecionado."""
        selection = self.groups_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um grupo para remover")
            return
        
        item = self.groups_tree.item(selection[0])
        group_id = item['values'][0]
        group_name = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Remover o grupo '{group_name}'?"):
            try:
                # Carrega grupos
                if os.path.exists('groups.json'):
                    with open('groups.json', 'r', encoding='utf-8') as f:
                        groups = json.load(f)
                    
                    # Remove o grupo
                    groups = [g for g in groups if str(g.get('chat_id', g.get('id'))) != str(group_id)]
                    
                    # Salva a lista atualizada
                    with open('groups.json', 'w', encoding='utf-8') as f:
                        json.dump(groups, f, ensure_ascii=False, indent=4)
                    
                    self.log_message(f"✅ Grupo '{group_name}' removido")
                    self.refresh_groups()
                    
            except Exception as e:
                self.log_message(f"❌ Erro ao remover grupo: {e}")
                messagebox.showerror("Erro", f"Erro ao remover grupo: {e}")
    
    def show_group_details(self):
        """Mostra detalhes do grupo selecionado."""
        selection = self.groups_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um grupo para ver detalhes")
            return
        
        item = self.groups_tree.item(selection[0])
        values = item['values']
        
        details = f"""Detalhes do Grupo:

ID: {values[0]}
Nome: {values[1]}
Tipo: {values[2]}
Membros: {values[3]}
Data de Adição: {values[4]}"""
        
        messagebox.showinfo("Detalhes do Grupo", details)
    
    def show_message_details(self):
        """Mostra detalhes da mensagem selecionada."""
        selection = self.pending_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma mensagem para ver detalhes")
            return
        
        item = self.pending_tree.item(selection[0])
        msg_id = item['values'][0]
        
        try:
            pending_data = load_pending_messages()
            messages = pending_data.get('messages', [])
            
            message = next((m for m in messages if m.get('id') == int(msg_id)), None)
            if message:
                details = f"""Detalhes da Mensagem:

ID: {message.get('id')}
Título: {message.get('title')}
Status: {message.get('status')}
Criado em: {message.get('created_at')}
Agendado para: {message.get('scheduled_time', 'Imediato')}

Texto:
{message.get('text', '')}

Grupos alvo: {len(message.get('target_groups', []))}"""
                
                messagebox.showinfo("Detalhes da Mensagem", details)
            else:
                messagebox.showerror("Erro", "Mensagem não encontrada")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar detalhes: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar detalhes: {e}")
    
    def cancel_pending_message(self):
        """Cancela uma mensagem pendente."""
        selection = self.pending_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma mensagem para cancelar")
            return
        
        item = self.pending_tree.item(selection[0])
        msg_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Cancelar a mensagem ID {msg_id}?"):
            try:
                pending_data = load_pending_messages()
                messages = pending_data.get('messages', [])
                
                # Marca como cancelada
                for message in messages:
                    if message.get('id') == int(msg_id):
                        message['status'] = 'cancelled'
                        break
                
                # Salva as alterações
                with open('pending_messages.json', 'w', encoding='utf-8') as f:
                    json.dump(pending_data, f, ensure_ascii=False, indent=4)
                
                self.log_message(f"✅ Mensagem {msg_id} cancelada")
                self.refresh_pending_messages()
                
            except Exception as e:
                self.log_message(f"❌ Erro ao cancelar mensagem: {e}")
                messagebox.showerror("Erro", f"Erro ao cancelar mensagem: {e}")
    
    def log_message(self, message):
        """Adiciona uma mensagem ao log."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Adiciona à fila de logs
        self.log_queue.put(log_entry)
    
    def clear_logs(self):
        """Limpa a área de logs."""
        self.log_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Salva os logs em um arquivo."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                
                self.log_message(f"✅ Logs salvos em {filename}")
                messagebox.showinfo("Sucesso", f"Logs salvos em {filename}")
                
            except Exception as e:
                self.log_message(f"❌ Erro ao salvar logs: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar logs: {e}")
    
    def start_log_monitoring(self):
        """Inicia o monitoramento de logs em thread separada."""
        def monitor_logs():
            while True:
                try:
                    # Processa mensagens da fila de logs
                    while not self.log_queue.empty():
                        self.log_queue.get_nowait()
                    
                    time.sleep(1)
                except:
                    break
        
        log_thread = threading.Thread(target=monitor_logs, daemon=True)
        log_thread.start()
    
    def on_closing(self):
        """Manipula o fechamento da aplicação."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair? Os bots em execução serão parados."):
            # Para os bots se estiverem executando
            if self.main_bot_process:
                self.main_bot_process.terminate()
            if self.admin_bot_process:
                self.admin_bot_process.terminate()
            
            self.root.destroy()

def main():
    """Função principal da aplicação."""
    root = tk.Tk()
    app = BotManagerGUI(root)
    
    # Configura o protocolo de fechamento
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Inicia a aplicação
    root.mainloop()

if __name__ == "__main__":
    main()