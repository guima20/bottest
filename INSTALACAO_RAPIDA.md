# 🚀 Instalação Rápida - Bot Telegram Kangaroo

## 📥 1. Download do Projeto

### Opção A: Download Direto (Recomendado)
```
https://github.com/guima20/bottest/archive/refs/heads/main.zip
```
- Clique no link acima
- Extraia o arquivo ZIP em uma pasta de sua escolha

### Opção B: Clone via Git
```bash
git clone https://github.com/guima20/bottest.git
cd bottest
```

## ⚙️ 2. Configuração Rápida

### 2.1 Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2.2 Configurar Tokens
Edite o arquivo `.env` e adicione seus tokens:
```
TELEGRAM_BOT_TOKEN=SEU_TOKEN_BOT_PRINCIPAL
TELEGRAM_ADMIN_BOT_TOKEN=SEU_TOKEN_BOT_ADMIN
ADMIN_IDS=SEU_ID_TELEGRAM
```

## 🎯 3. Executar o Sistema

### Opção A: Interface Gráfica (Recomendado)
```bash
python start_gui.py
```

### Opção B: Linha de Comando
```bash
# Terminal 1 - Bot Principal
python unified_bot.py

# Terminal 2 - Bot Administrativo  
python admin_bot.py
```

## ✅ 4. Teste de Instalação
```bash
python test_installation.py
```

## 🎮 5. Demonstração
```bash
python demo.py
```

## 📱 6. Como Obter os Tokens

### Bot Principal:
1. Acesse [@BotFather](https://t.me/BotFather) no Telegram
2. Digite `/newbot`
3. Escolha um nome e username para seu bot
4. Copie o token fornecido

### Bot Administrativo:
1. Repita o processo acima para criar um segundo bot
2. Este será usado apenas para administração

### Seu ID do Telegram:
1. Acesse [@userinfobot](https://t.me/userinfobot)
2. Digite `/start`
3. Copie seu ID numérico

## 🆘 Suporte

Se encontrar problemas:
1. Execute `python test_installation.py` para verificar a instalação
2. Verifique se todos os tokens estão corretos no arquivo `.env`
3. Certifique-se de que o Python 3.7+ está instalado

## 📂 Estrutura do Projeto

```
bottest/
├── unified_bot.py          # Bot principal
├── admin_bot.py           # Bot administrativo
├── gui_manager.py         # Interface gráfica
├── start_gui.py          # Inicializador da GUI
├── bot_messages.py       # Sistema de mensagens
├── config.json           # Configurações
├── .env                  # Tokens e variáveis
└── requirements.txt      # Dependências
```

---
**🤖 Sistema pronto para uso!** Adicione o bot principal aos seus grupos e use o bot administrativo para gerenciar mensagens.