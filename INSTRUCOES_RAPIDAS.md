# 🚀 Bot do Telegram - Instruções Rápidas

## ⚡ Como Iniciar o Bot

### 1️⃣ Método Recomendado (Script Automático):
```bash
./start_unified.sh
```

### 2️⃣ Método Manual:
```bash
python3 unified_bot.py
```

### 3️⃣ Em Background:
```bash
nohup python3 unified_bot.py > bot.log 2>&1 &
```

## 🔧 Comandos Úteis

### 📊 Verificar se está rodando:
```bash
ps aux | grep unified_bot
```

### 📄 Ver logs em tempo real:
```bash
tail -f unified_bot.log
```

### 🛑 Parar o bot:
```bash
pkill -f unified_bot
```

## 🎯 Comandos do Bot

### 👥 Para Usuários:
- `/start` - Inicia o bot e mostra a mensagem principal

### 🔐 Para Administradores:
- `/set_image <url>` - Alterar imagem
- `/set_text <texto>` - Alterar texto  
- `/set_button <1-4> <texto> <url>` - Alterar botão
- `/show_config` - Mostrar configuração atual
- `/admin_help` - Ajuda administrativa

## ⚙️ Configuração

1. Configure seus tokens no arquivo `.env`
2. Ajuste os IDs dos administradores
3. Execute o bot com `./start_unified.sh`

✅ **Pronto para usar!**