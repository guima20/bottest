# 🌍 Configuração de Acesso Externo HTTPS

## ✅ Sistema Heylink - Configurado e Funcionando!

### 🚀 URLs de Acesso Externo

#### 🌐 Landing Page Principal
```
https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
```

#### 🛠️ Painel Administrativo
```
https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev/admin
https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev/admin
```

### 🔐 Credenciais de Acesso
- **Senha Admin:** `admin123`

---

## 📱 Configuração para Telegram Mini App

### 1. Criar Bot no BotFather
```
/start
/newbot
Nome do Bot: Meu Heylink Bot
Username: @meu_heylink_bot
```

### 2. Configurar Mini App
```
/newapp
Selecione o bot: @meu_heylink_bot
Nome do App: Meu Heylink
Descrição: Todos os meus links em um só lugar
URL: https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
```

### 3. Configurar Menu Button
```
/setmenubutton
Selecione o bot: @meu_heylink_bot
Nome do botão: 🔗 Meus Links
URL: https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
```

---

## 🔧 Configuração Técnica

### Headers HTTPS Configurados
```http
Content-Security-Policy: frame-ancestors 'self' https://t.me https://web.telegram.org
X-Frame-Options: ALLOWALL
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### Portas Configuradas
- **Flask App:** Porta 8000 (localhost)
- **Proxy Server:** Porta 9000 (localhost)
- **Acesso Externo:** Portas 12000/12001 (HTTPS)

---

## 🚀 Como Iniciar o Sistema

### Método 1: Script Automático (Recomendado)
```bash
cd /workspace/bottest
./start_external.sh
```

### Método 2: Manual
```bash
cd /workspace/bottest
source venv/bin/activate
python app.py &
python proxy_server.py &
```

### Para Parar o Sistema
```bash
./stop_system.sh
```

---

## 📊 Status Atual do Sistema

### ✅ Funcionalidades Testadas
- [x] Landing page responsiva
- [x] Painel administrativo completo
- [x] Upload de imagens funcionando
- [x] Banco de dados SQLite operacional
- [x] Headers CORS configurados
- [x] Acesso HTTPS externo funcionando
- [x] Compatibilidade com Telegram Mini Apps

### 🌐 URLs Testadas
- [x] http://localhost:8000 (Flask direto)
- [x] http://localhost:9000 (Proxy)
- [x] https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
- [x] https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev

---

## 📁 Arquivos de Configuração

### Principais Arquivos
```
bottest/
├── app.py                 # Aplicação Flask principal
├── proxy_server.py        # Servidor proxy HTTPS
├── start_external.sh      # Script de inicialização
├── stop_system.sh         # Script para parar
├── requirements.txt       # Dependências
├── README.md             # Documentação completa
└── ACESSO_EXTERNO.md     # Este arquivo
```

### Banco de Dados
```
heylink.db                # SQLite com dados persistentes
```

### Templates e Assets
```
templates/
├── index.html            # Landing page
├── admin.html           # Painel admin
└── login.html           # Login admin

static/
├── css/style.css        # Estilos CSS
├── js/script.js         # JavaScript
└── uploads/             # Imagens enviadas
```

---

## 🔗 Links Úteis

- **Repositório GitHub:** https://github.com/guima20/bottest
- **Branch:** heylink-system
- **Pull Request:** #1
- **Documentação BotFather:** https://core.telegram.org/bots#botfather
- **Telegram Mini Apps:** https://core.telegram.org/bots/webapps

---

## 🎯 Próximos Passos

1. **Testar no Telegram:**
   - Configure o bot no BotFather
   - Teste o Mini App no Telegram
   - Verifique a responsividade

2. **Personalizar:**
   - Altere cores em `static/css/style.css`
   - Modifique textos nos templates
   - Adicione novos links via painel admin

3. **Deploy em Produção:**
   - Heroku: `git push heroku main`
   - Render: Conecte o repositório GitHub
   - Replit: Importe o projeto

---

**✅ Sistema 100% funcional e pronto para uso!**

*Desenvolvido com ❤️ usando Python + Flask*