# 🔗 Sistema Heylink - Clone Funcional

Sistema web completo que replica as funcionalidades do Heylink, desenvolvido com **Python Flask** para uso em **Telegram Mini Apps**.

## ✨ Funcionalidades

### 🎯 Landing Page Dinâmica
- ✅ Logo personalizado no topo
- ✅ Título e descrição customizáveis
- ✅ Lista de links com imagens e descrições
- ✅ Design responsivo e moderno
- ✅ Compatível com Telegram Mini App

### 🛠️ Painel Administrativo
- ✅ Proteção por senha
- ✅ Adicionar/editar/excluir links
- ✅ Upload de imagens e logos
- ✅ Configuração de título e descrição
- ✅ Interface intuitiva

### 🔒 Segurança e Compatibilidade
- ✅ Headers CORS configurados
- ✅ Content Security Policy para Telegram
- ✅ Suporte a HTTPS
- ✅ Acesso externo configurado

## 🚀 Como executar

### 1. Execução Rápida (Recomendado)
```bash
./start_external.sh
```

### 2. Execução Manual

#### 2.1. Configurar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

#### 2.2. Executar aplicação
```bash
python app.py
```

### 3. Acessar sistema

#### 🌐 Acesso Local
- **Landing Page:** http://localhost:8000
- **Painel Admin:** http://localhost:8000/admin

#### 🌍 Acesso Externo HTTPS
- **Landing Page:** https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
- **Landing Page:** https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
- **Painel Admin:** Adicione `/admin` ao final da URL

#### 🔐 Credenciais
- **Senha Admin:** admin123

### 4. Parar sistema
```bash
./stop_system.sh
```

## 📁 Estrutura do Projeto

```
bottest/
├── app.py                 # Aplicação Flask principal
├── proxy_server.py        # Servidor proxy para acesso externo
├── start_external.sh      # Script de inicialização
├── stop_system.sh         # Script para parar sistema
├── requirements.txt       # Dependências Python
├── heylink.db            # Banco de dados SQLite
├── templates/            # Templates HTML
│   ├── index.html        # Landing page
│   ├── admin.html        # Painel administrativo
│   └── login.html        # Página de login
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   ├── js/
│   │   └── script.js     # JavaScript
│   └── uploads/          # Imagens enviadas
└── venv/                 # Ambiente virtual Python
```

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.x + Flask
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Banco de Dados:** SQLite
- **Estilo:** Bootstrap 5 + Font Awesome
- **Deploy:** Configurado para Heroku, Render, Replit

## 📱 Telegram Mini App

### Configuração no BotFather

1. Crie um bot no @BotFather
2. Configure o Mini App:
   ```
   /newapp
   /setmenubutton
   ```
3. Use a URL HTTPS do sistema:
   ```
   https://work-1-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev
   ```

### Headers Configurados

```http
Content-Security-Policy: frame-ancestors 'self' https://t.me https://web.telegram.org
X-Frame-Options: ALLOWALL
Access-Control-Allow-Origin: *
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export ADMIN_PASSWORD=admin123
```

### Deploy em Produção

#### Heroku
```bash
git push heroku main
```

#### Render
1. Conecte o repositório GitHub
2. Configure build command: `pip install -r requirements.txt`
3. Configure start command: `python app.py`

#### Replit
1. Importe o repositório
2. Execute: `python app.py`

## 📊 Banco de Dados

### Tabela: links
```sql
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: config
```sql
CREATE TABLE config (
    id INTEGER PRIMARY KEY,
    title TEXT DEFAULT 'Meu Heylink',
    description TEXT DEFAULT 'Todos os meus links em um só lugar',
    logo_path TEXT
);
```

## 🎨 Personalização

### Cores e Estilo
Edite `/static/css/style.css` para personalizar:
- Cores do tema
- Fontes
- Espaçamentos
- Animações

### Layout
Modifique `/templates/index.html` para:
- Alterar estrutura da página
- Adicionar novos elementos
- Personalizar footer

## 🐛 Solução de Problemas

### Porta em uso
```bash
pkill -f "python app.py"
pkill -f "python proxy_server.py"
```

### Permissões de arquivo
```bash
chmod +x start_external.sh
chmod +x stop_system.sh
```

### Banco de dados corrompido
```bash
rm heylink.db
python app.py  # Recria automaticamente
```

## 📝 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

- **Issues:** https://github.com/guima20/bottest/issues
- **Documentação:** Este README
- **Telegram:** @seu_usuario

---

**Desenvolvido com ❤️ usando Python + Flask**