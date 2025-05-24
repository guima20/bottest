# 📦 Download do Sistema Heylink Completo

## 🚀 Arquivo ZIP Disponível

O sistema completo está disponível para download em formato ZIP:

**📁 Arquivo:** `heylink-sistema-completo.zip`

## 📋 Conteúdo do ZIP

O arquivo ZIP contém todos os arquivos necessários para executar o sistema:

```
heylink-sistema-completo.zip
├── app.py                    # Aplicação Flask principal
├── proxy_server.py           # Servidor proxy para acesso externo
├── start_external.sh         # Script de inicialização automática
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação completa
├── .gitignore               # Configuração Git
├── templates/               # Templates HTML
│   ├── index.html           # Landing page
│   ├── admin_dashboard.html # Painel administrativo
│   ├── admin_login.html     # Página de login
│   └── base.html           # Template base
├── static/                  # Arquivos estáticos
│   ├── css/
│   │   └── style.css       # Estilos CSS
│   └── js/
│       └── script.js       # JavaScript
└── documentação/           # Arquivos de documentação
    ├── ACESSO_EXTERNO.md
    ├── README_HEYLINK.md
    └── SISTEMA_COMPLETO.md
```

## 🛠️ Como usar o ZIP

### 1. Download e Extração
```bash
# Baixe o arquivo ZIP do GitHub
# Extraia o conteúdo
unzip heylink-sistema-completo.zip
cd bottest/
```

### 2. Configuração do Ambiente
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Execução

#### Opção A: Cloudflare Tunnel (Recomendado)
```bash
# Script automatizado - instala e configura tudo
./start_cloudflare.sh
```

#### Opção B: Servidor Local
```bash
# Execução local simples
python app.py

# Ou com proxy para HTTPS
./start_external.sh
```

## 🌍 Acesso ao Sistema

### Local
- **Landing Page:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

### Cloudflare Tunnel (HTTPS Público)
- **Landing Page:** https://abc-def-123.trycloudflare.com
- **Admin:** https://abc-def-123.trycloudflare.com/admin
- **Para Telegram:** Use o link HTTPS no BotFather

### Externo (HTTPS)
- **Landing Page:** https://seu-dominio.com
- **Admin:** https://seu-dominio.com/admin

## 🔐 Credenciais

- **Senha Admin:** admin123

## 📱 Telegram Mini App

O sistema está configurado para funcionar como Telegram Mini App:

1. Configure no @BotFather
2. Use a URL HTTPS do seu servidor
3. O sistema já possui os headers necessários

## 🆘 Suporte

- **GitHub:** https://github.com/guima20/bottest
- **Issues:** https://github.com/guima20/bottest/issues
- **Documentação:** README.md

---

**✅ Sistema testado e funcionando perfeitamente!**