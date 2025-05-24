# 🚀 Guia Rápido - Bots do Telegram

## ⚡ Instalação Rápida

```bash
# 1. Instalar dependências
./install.sh

# 2. Testar configuração
python test_config.py
```

## 🤖 Criar Bots no Telegram

1. **Acesse [@BotFather](https://t.me/BotFather)**
2. **Crie bot principal:**
   ```
   /newbot
   Nome: Meu Bot de Chips
   Username: meubot_chips_bot
   ```
3. **Crie bot admin:**
   ```
   /newbot
   Nome: Admin Bot Chips
   Username: admin_chips_bot
   ```
4. **Salve os tokens fornecidos**

## 🆔 Descobrir seu ID

1. **Envie mensagem para [@userinfobot](https://t.me/userinfobot)**
2. **Anote o número do seu ID**

## ⚙️ Configurar Variáveis

```bash
# Linux/Mac
export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_ADMIN_BOT_TOKEN="0987654321:ZYXwvuTSRqponMLKjihGFEdcba"
export ADMIN_IDS="123456789"

# Windows
set TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
set TELEGRAM_ADMIN_BOT_TOKEN=0987654321:ZYXwvuTSRqponMLKjihGFEdcba
set ADMIN_IDS=123456789
```

## 🎮 Executar

```bash
# Ambos os bots
python run_bots.py

# Ou separadamente
python run_main_bot.py    # Bot principal
python run_admin_bot.py   # Bot admin
```

## 📱 Testar

### Bot Principal
1. Envie `/start` para seu bot principal
2. Deve receber: imagem + texto + 4 botões + refresh

### Bot Admin
1. Envie `/start` para seu bot admin
2. Use comandos:
   ```
   /set_image https://nova-imagem.jpg
   /set_text Novo texto aqui!
   /set_button 1 Novo Botão https://link.com
   /show_config
   ```

## 🔧 Comandos Admin

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/set_image [url]` | Define imagem | `/set_image https://img.com/foto.jpg` |
| `/set_text [texto]` | Define texto | `/set_text Novo texto promocional!` |
| `/set_button [1-4] [texto] [url]` | Atualiza botão | `/set_button 1 Clique Aqui https://site.com` |
| `/show_config` | Mostra config atual | `/show_config` |

## ✅ Verificação

```bash
# Testar tudo
python test_config.py

# Ver logs em tempo real
tail -f *.log  # Se houver arquivos de log
```

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| "Token não encontrado" | Configure `TELEGRAM_BOT_TOKEN` |
| "Acesso negado" | Verifique `ADMIN_IDS` |
| "Imagem não carrega" | Use URL HTTPS válida |
| Bot não responde | Verifique token e internet |

## 📁 Arquivos Importantes

- `config.json` - Configurações do bot
- `telegram_bot.py` - Bot principal
- `admin_bot.py` - Bot administrativo
- `test_config.py` - Teste de configuração

---

**🎯 Em 5 minutos você terá bots funcionando!**