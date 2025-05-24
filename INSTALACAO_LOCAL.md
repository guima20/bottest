# 🖥️ GUIA DE INSTALAÇÃO LOCAL

## 📋 PRÉ-REQUISITOS

- Python 3.8+ instalado
- Git instalado
- Tokens dos bots do Telegram

---

## 🚀 INSTALAÇÃO PASSO A PASSO

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/guima20/bottest.git
cd bottest
git checkout telegram-bot-system
```

### 2️⃣ Instalar Dependências
```bash
# Opção 1: Via pip
pip install python-telegram-bot==21.0.1 python-dotenv

# Opção 2: Via requirements.txt (se existir)
pip install -r requirements.txt
```

### 3️⃣ Configurar Variáveis de Ambiente
```bash
# Criar arquivo .env na raiz do projeto
nano .env
```

**Conteúdo do arquivo .env:**
```env
TELEGRAM_BOT_TOKEN=SEU_TOKEN_DO_BOT_PRINCIPAL
ADMIN_BOT_TOKEN=SEU_TOKEN_DO_BOT_ADMINISTRATIVO
```

### 4️⃣ Verificar Configuração
```bash
# Verificar se o config.json existe
cat config.json

# Se não existir, será criado automaticamente na primeira execução
```

### 5️⃣ Executar os Bots

#### Opção A: Execução em Terminais Separados
```bash
# Terminal 1 - Bot Principal
python3 unified_bot.py

# Terminal 2 - Bot Administrativo
python3 admin_bot.py
```

#### Opção B: Execução em Background
```bash
# Iniciar bot principal em background
nohup python3 unified_bot.py > unified_bot.log 2>&1 &

# Iniciar bot administrativo em background  
nohup python3 admin_bot.py > admin_bot.log 2>&1 &

# Verificar se estão rodando
ps aux | grep python3
```

---

## 🔧 CONFIGURAÇÃO INICIAL

### Configurar IDs de Administrador
Edite o arquivo `unified_bot.py` e `admin_bot.py`:
```python
ADMIN_IDS = [SEU_ID_TELEGRAM, OUTRO_ID_SE_NECESSARIO]
```

**Como descobrir seu ID do Telegram:**
1. Envie `/start` para @userinfobot
2. Copie o número do ID
3. Substitua nos arquivos

### Testar Funcionamento
1. Envie `/start` para o bot principal
2. Envie `/help` para o bot administrativo
3. Verifique se as mensagens são enviadas corretamente

---

## 📁 ESTRUTURA DE ARQUIVOS

```
bottest/
├── unified_bot.py              # Bot principal
├── admin_bot.py               # Bot administrativo  
├── config.json                # Configuração (criado automaticamente)
├── .env                       # Tokens (você deve criar)
├── images/                    # Pasta para imagens
│   └── current_image.jpg      # Imagem padrão
├── unified_bot.log            # Logs do bot principal
├── admin_bot.log              # Logs do bot admin
└── README.md                  # Documentação
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "ModuleNotFoundError"
```bash
pip install python-telegram-bot==21.0.1 python-dotenv
```

### Erro: "Token inválido"
- Verifique se os tokens estão corretos no arquivo `.env`
- Certifique-se de que não há espaços extras

### Erro: "Permission denied"
```bash
chmod +x unified_bot.py admin_bot.py
```

### Bot não responde
1. Verifique os logs: `tail -f unified_bot.log`
2. Confirme se o bot está rodando: `ps aux | grep python3`
3. Teste a conectividade: `ping api.telegram.org`

### Erro de conexão (como o que você teve)
- Verifique sua conexão com a internet
- Confirme se não há firewall bloqueando
- Teste com outro provedor de internet se necessário

---

## 📊 MONITORAMENTO

### Verificar Status dos Bots
```bash
# Ver processos rodando
ps aux | grep python3

# Ver logs em tempo real
tail -f unified_bot.log
tail -f admin_bot.log

# Verificar uso de recursos
top | grep python3
```

### Parar os Bots
```bash
# Parar todos os bots Python
pkill -f "python3.*bot"

# Ou parar individualmente por PID
kill PID_DO_PROCESSO
```

---

## 🔄 ATUALIZAÇÕES

### Atualizar do GitHub
```bash
git pull origin telegram-bot-system
```

### Backup da Configuração
```bash
# Fazer backup do config.json
cp config.json config_backup_$(date +%Y%m%d).json

# Fazer backup das imagens
tar -czf images_backup_$(date +%Y%m%d).tar.gz images/
```

---

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique os logs primeiro
2. Consulte a documentação no README.md
3. Verifique se todas as dependências estão instaladas
4. Confirme se os tokens estão corretos

**Repositório:** https://github.com/guima20/bottest  
**Branch:** telegram-bot-system

---

**🎉 BOA SORTE COM SEU BOT! 🎉**