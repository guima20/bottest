# 🤖 Bot do Telegram - Sistema Completo

Sistema completo de bots do Telegram em Python com painel administrativo para configuração dinâmica.

## 📋 Funcionalidades

### 🎯 Bot Principal (`telegram_bot.py`)
- **Comando `/start`**: Envia imagem, texto e 4 botões configuráveis
- **Botão "🔄 Refresh"**: Reenvia a mensagem principal
- **Comando `/help`**: Mostra ajuda do bot
- **Configuração dinâmica**: Carrega dados do arquivo `config.json`

### 🔧 Bot Administrativo (`admin_bot.py`)
- **`/set_image [url]`**: Define nova imagem
- **`/set_text [texto]`**: Define novo texto principal
- **`/set_button [1-4] [texto] [url]`**: Atualiza botão específico
- **`/show_config`**: Mostra configuração atual
- **Segurança**: Apenas usuários autorizados podem usar

## 🚀 Instalação

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Criar Bots no Telegram
1. Acesse [@BotFather](https://t.me/BotFather) no Telegram
2. Crie dois bots:
   - Bot principal: `/newbot` → Nome do seu bot
   - Bot admin: `/newbot` → Nome do bot admin
3. Salve os tokens fornecidos

### 3. Descobrir seu ID de Usuário
1. Envie uma mensagem para [@userinfobot](https://t.me/userinfobot)
2. Anote seu ID numérico

### 4. Configurar Variáveis de Ambiente
```bash
# Linux/Mac
export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_ADMIN_BOT_TOKEN="0987654321:ZYXwvuTSRqponMLKjihGFEdcba"
export ADMIN_IDS="123456789,987654321"

# Windows
set TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
set TELEGRAM_ADMIN_BOT_TOKEN=0987654321:ZYXwvuTSRqponMLKjihGFEdcba
set ADMIN_IDS=123456789,987654321
```

## 🎮 Execução

### Executar Ambos os Bots (Recomendado)
```bash
python run_bots.py
```

### Executar Bots Separadamente
```bash
# Apenas bot principal
python run_main_bot.py

# Apenas bot administrativo
python run_admin_bot.py
```

## 📁 Estrutura de Arquivos

```
bottest/
├── telegram_bot.py          # Bot principal
├── admin_bot.py             # Bot administrativo
├── run_bots.py              # Executa ambos os bots
├── run_main_bot.py          # Executa apenas bot principal
├── run_admin_bot.py         # Executa apenas bot admin
├── config.json              # Configurações (criado automaticamente)
├── .env.example             # Exemplo de variáveis de ambiente
├── requirements.txt         # Dependências Python
└── README_TELEGRAM_BOT.md   # Este arquivo
```

## ⚙️ Configuração (config.json)

```json
{
  "image": "https://via.placeholder.com/600x400/0066cc/ffffff?text=Chips+Gratis",
  "text": "👋 Olá! REGISTRE-SE para receber CHIPS GRÁTIS até $130 👇",
  "buttons": [
    {"text": "👉 Grab Your Free NOW", "url": "https://link1.com"},
    {"text": "👉 Discover More FreeChips and GameTips", "url": "https://link2.com"},
    {"text": "👉 Add To Group", "url": "https://link3.com"},
    {"text": "👉 Join RichGroup", "url": "https://link4.com"}
  ]
}
```

## 🎯 Como Usar

### Bot Principal
1. Inicie uma conversa com seu bot principal
2. Digite `/start`
3. O bot enviará:
   - Uma imagem
   - Texto promocional
   - 4 botões com links
   - Botão "🔄 Refresh"

### Bot Administrativo
1. Inicie uma conversa com seu bot administrativo
2. Digite `/start` para ver os comandos
3. Use os comandos para configurar:

```bash
# Exemplos de comandos administrativos
/set_image https://exemplo.com/nova-imagem.jpg
/set_text Novo texto promocional aqui!
/set_button 1 Novo Botão https://novolink.com
/show_config
```

## 🔒 Segurança

- ✅ Apenas usuários com ID em `ADMIN_IDS` podem usar comandos administrativos
- ✅ Validação de URLs nos botões e imagens
- ✅ Tratamento de erros e logging
- ✅ Limite de caracteres para textos

## 🛠️ Personalização

### Adicionar Novos Comandos
Edite `telegram_bot.py` ou `admin_bot.py` e adicione novos handlers:

```python
async def novo_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Novo comando!")

# No main()
application.add_handler(CommandHandler("novo", novo_comando))
```

### Modificar Layout dos Botões
Edite a função `create_inline_keyboard()` em `telegram_bot.py`:

```python
def create_inline_keyboard(config: Dict[str, Any]) -> InlineKeyboardMarkup:
    keyboard = []
    
    # Exemplo: 2 botões por linha
    buttons = config.get('buttons', [])
    for i in range(0, len(buttons), 2):
        row = []
        for j in range(2):
            if i + j < len(buttons):
                button = buttons[i + j]
                row.append(InlineKeyboardButton(
                    text=button.get('text', 'Botão'),
                    url=button.get('url', 'https://telegram.org')
                ))
        keyboard.append(row)
    
    # Botão refresh
    keyboard.append([InlineKeyboardButton(
        text="🔄 Refresh",
        callback_data="refresh"
    )])
    
    return InlineKeyboardMarkup(keyboard)
```

## 🐛 Troubleshooting

### Erro: "Token não encontrado"
- Verifique se as variáveis de ambiente estão configuradas
- Use `echo $TELEGRAM_BOT_TOKEN` para verificar

### Erro: "Acesso negado"
- Verifique se seu ID está em `ADMIN_IDS`
- Use [@userinfobot](https://t.me/userinfobot) para confirmar seu ID

### Bot não responde
- Verifique se o token está correto
- Verifique a conexão com a internet
- Veja os logs para erros específicos

### Imagem não carrega
- Verifique se a URL da imagem é válida
- Teste a URL no navegador
- Use URLs HTTPS sempre que possível

## 📝 Logs

Os bots geram logs detalhados para debugging:

```
2024-01-01 12:00:00 - telegram_bot - INFO - Bot iniciado!
2024-01-01 12:00:01 - telegram_bot - INFO - Comando /start recebido de 123456789
2024-01-01 12:00:02 - telegram_bot - INFO - Mensagem principal enviada para chat 123456789
```

## 🔄 Atualizações

Para atualizar o sistema:

1. Faça backup do `config.json`
2. Atualize os arquivos Python
3. Reinstale dependências se necessário
4. Restaure o `config.json`

## 📞 Suporte

Para suporte ou dúvidas:
- Verifique os logs de erro
- Consulte a documentação do [python-telegram-bot](https://docs.python-telegram-bot.org/)
- Teste com comandos simples primeiro

---

**Desenvolvido com ❤️ usando Python e python-telegram-bot**