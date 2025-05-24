# 🌐 Configuração Cloudflare Tunnel (100% Gratuito)

## 🚀 Instalação e Configuração

### 1. **Instalar Cloudflared**

#### **Ubuntu/Debian:**
```bash
# Download e instalação
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verificar instalação
cloudflared --version
```

#### **Outras distribuições:**
```bash
# CentOS/RHEL/Fedora
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm
sudo rpm -i cloudflared-linux-amd64.rpm

# Arch Linux
sudo pacman -S cloudflared

# Via Snap (qualquer distribuição)
sudo snap install cloudflared
```

### 2. **Executar o Túnel**

#### **Método Rápido (Recomendado):**
```bash
# Terminal 1 - Flask
cd ~/Downloads/heylink-sistema-completo/bottest
source venv/bin/activate
python app.py

# Terminal 2 - Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000
```

#### **Resultado:**
```
2025-05-24T16:30:00Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less tunnels have no uptime guarantee. If you intend to use tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2025-05-24T16:30:00Z INF Requesting new quick Tunnel on trycloudflare.com...
2025-05-24T16:30:01Z INF +--------------------------------------------------------------------------------------------+
2025-05-24T16:30:01Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2025-05-24T16:30:01Z INF |  https://abc-def-123.trycloudflare.com                                                     |
2025-05-24T16:30:01Z INF +--------------------------------------------------------------------------------------------+
```

**Seu link HTTPS:** `https://abc-def-123.trycloudflare.com`

### 3. **Script Automatizado**

Crie o arquivo `start_cloudflare.sh`:

```bash
#!/bin/bash
echo "🌐 Iniciando Heylink com Cloudflare Tunnel..."

# Verificar se cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo "❌ Cloudflared não encontrado. Instalando..."
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
fi

# Verificar se Flask está rodando
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "🚀 Iniciando Flask..."
    source venv/bin/activate
    python app.py &
    FLASK_PID=$!
    sleep 3
fi

# Iniciar túnel
echo "📡 Criando túnel Cloudflare..."
cloudflared tunnel --url http://localhost:8000

# Cleanup ao sair
if [ ! -z "$FLASK_PID" ]; then
    trap "kill $FLASK_PID" EXIT
fi
```

### 4. **Configuração Avançada (Opcional)**

#### **Criar Túnel Nomeado (Conta Cloudflare):**
```bash
# 1. Login na Cloudflare
cloudflared tunnel login

# 2. Criar túnel nomeado
cloudflared tunnel create meu-heylink

# 3. Configurar DNS
cloudflared tunnel route dns meu-heylink heylink.seudominio.com

# 4. Criar arquivo de configuração
nano ~/.cloudflared/config.yml
```

**Conteúdo do config.yml:**
```yaml
tunnel: meu-heylink
credentials-file: ~/.cloudflared/meu-heylink.json

ingress:
  - hostname: heylink.seudominio.com
    service: http://localhost:8000
  - service: http_status:404
```

```bash
# 5. Executar túnel nomeado
cloudflared tunnel run meu-heylink
```

## 🔧 **Vantagens do Cloudflare Tunnel:**

### ✅ **Prós:**
- **100% Gratuito** - Sem limites de tempo ou conexões
- **HTTPS Automático** - Certificado SSL incluído
- **CDN Global** - Performance otimizada mundialmente
- **Sem Configuração** - Funciona imediatamente
- **Estável** - Infraestrutura Cloudflare
- **Sem Cadastro** - Para túneis rápidos

### ❌ **Contras:**
- **URL Aleatória** - Muda a cada reinício (túnel rápido)
- **Sem Dashboard** - Menos recursos de monitoramento
- **Dependência** - Precisa da Cloudflare

## 📱 **Configuração no Telegram:**

### **1. Executar o Túnel:**
```bash
chmod +x start_cloudflare.sh
./start_cloudflare.sh
```

### **2. Copiar o Link HTTPS:**
Exemplo: `https://abc-def-123.trycloudflare.com`

### **3. Configurar no BotFather:**
```
/start
/newbot
Nome: Meu Heylink Bot
Username: meu_heylink_bot

/newapp
Bot: @meu_heylink_bot
Nome: Meu Heylink
Username: meu_heylink
URL: https://abc-def-123.trycloudflare.com
Descrição: Todos os meus links em um só lugar

/setmenubutton
Bot: @meu_heylink_bot
URL: https://abc-def-123.trycloudflare.com
Texto: 🔗 Meus Links
```

### **4. Testar:**
1. Acesse o link no navegador
2. Verifique se carrega normalmente
3. Teste no Telegram via bot

## 🆘 **Solução de Problemas:**

### **Erro de Instalação:**
```bash
# Atualizar repositórios
sudo apt update

# Instalar dependências
sudo apt install wget curl

# Tentar novamente
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### **Túnel Não Conecta:**
```bash
# Verificar se Flask está rodando
curl http://localhost:8000

# Verificar logs
cloudflared tunnel --url http://localhost:8000 --loglevel debug
```

### **URL Não Funciona:**
- Aguarde 1-2 minutos para propagação DNS
- Teste em navegador anônimo
- Verifique se não há firewall bloqueando

## 🎯 **Resumo dos Comandos:**

```bash
# 1. Instalar
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 2. Executar Flask
python app.py

# 3. Criar túnel
cloudflared tunnel --url http://localhost:8000

# 4. Copiar link HTTPS e configurar no Telegram
```

---

**✅ Cloudflare Tunnel é a solução mais confiável e gratuita para expor seu servidor local!**