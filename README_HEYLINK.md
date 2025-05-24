# 🔗 Heylink - Sistema de Links Personalizados

Uma versão simples e funcional do Heylink, desenvolvida com **Python + Flask**, compatível com **Telegram Mini Apps**.

## ✨ Funcionalidades

- 🎨 **Landing Page Dinâmica** - Página personalizada com seus links
- 🖼️ **Upload de Imagens** - Logo principal e imagens para cada link
- ⚙️ **Painel Administrativo** - Interface para gerenciar links e configurações
- 📱 **Responsivo** - Funciona perfeitamente em desktop e mobile
- 🤖 **Telegram Mini App** - Compatível com Telegram WebApp
- 🎯 **Simples e Rápido** - Configuração em minutos

## 🚀 Instalação e Execução

### Método 1: Script Automático (Recomendado)

```bash
# Tornar o script executável
chmod +x run.sh

# Executar
./run.sh
```

### Método 2: Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python app.py
```

## 🌐 Acesso

- **Site Principal**: http://localhost:12000
- **Painel Admin**: http://localhost:12000/admin
- **Senha Admin**: `admin123`

## 📱 Configuração para Telegram Mini App

### 1. Deploy em Servidor

Para usar como Telegram Mini App, você precisa fazer deploy em um servidor com HTTPS. Opções recomendadas:

- **Render.com** (Gratuito)
- **Railway.app** (Gratuito)
- **Heroku** (Pago)
- **Replit** (Gratuito com limitações)

### 2. Configurar Bot no Telegram

1. Fale com [@BotFather](https://t.me/botfather)
2. Crie um novo bot: `/newbot`
3. Configure o Mini App: `/newapp`
4. Insira a URL do seu deploy

### 3. Headers de Segurança

O sistema já está configurado com os headers necessários:

```python
Content-Security-Policy: frame-ancestors 'self' https://t.me https://web.telegram.org
X-Frame-Options: ALLOWALL
Access-Control-Allow-Origin: *
```

## 🗂️ Estrutura do Projeto

```
bottest/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── run.sh                # Script de execução
├── heylink.db            # Banco de dados SQLite (criado automaticamente)
├── static/
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   ├── js/
│   │   └── script.js     # JavaScript e integração Telegram
│   └── uploads/          # Imagens enviadas
└── templates/
    ├── base.html         # Template base
    ├── index.html        # Landing page
    ├── admin_login.html  # Login admin
    └── admin_dashboard.html # Dashboard admin
```

## 🎨 Personalização

### Alterar Senha do Admin

Edite o arquivo `app.py`:

```python
ADMIN_PASSWORD = 'sua_nova_senha'
```

### Personalizar Cores

Edite o arquivo `static/css/style.css`:

```css
body {
    background: linear-gradient(135deg, #sua_cor1 0%, #sua_cor2 100%);
}
```

### Adicionar Logo Padrão

1. Coloque sua imagem em `static/uploads/`
2. No painel admin, faça upload do logo

## 📊 Banco de Dados

O sistema usa **SQLite** com duas tabelas:

### Tabela `config`
- `id` - ID único
- `title` - Título da página
- `description` - Descrição
- `logo_path` - Caminho do logo

### Tabela `links`
- `id` - ID único
- `title` - Título do link
- `description` - Descrição do link
- `url` - URL de destino
- `image_path` - Caminho da imagem
- `order_index` - Ordem de exibição
- `created_at` - Data de criação

## 🔧 Configurações Avançadas

### Alterar Porta

Edite `app.py`:

```python
app.run(host='0.0.0.0', port=SUA_PORTA, debug=True)
```

### Configurar Upload

Edite `app.py`:

```python
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## 🚀 Deploy

### Render.com

1. Conecte seu repositório GitHub
2. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

### Railway.app

1. Conecte seu repositório GitHub
2. Configure variáveis de ambiente se necessário
3. Deploy automático

### Heroku

```bash
# Criar Procfile
echo "web: python app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy Heylink"
git push heroku main
```

## 🔒 Segurança

- ✅ Headers configurados para Telegram Mini App
- ✅ Validação de uploads de imagem
- ✅ Sanitização de inputs
- ✅ Proteção contra XSS
- ✅ Sessões seguras

### Melhorias de Segurança Recomendadas

Para produção, considere:

1. **Senha mais forte** para admin
2. **Autenticação mais robusta** (OAuth, JWT)
3. **Rate limiting** para uploads
4. **Backup automático** do banco
5. **Logs de auditoria**

## 🐛 Solução de Problemas

### Erro de Permissão

```bash
chmod +x run.sh
```

### Porta em Uso

Altere a porta no `app.py` ou mate o processo:

```bash
sudo lsof -i :12000
sudo kill -9 PID
```

### Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📝 Changelog

### v1.0.0
- ✅ Sistema básico funcionando
- ✅ Painel administrativo
- ✅ Upload de imagens
- ✅ Compatibilidade Telegram Mini App
- ✅ Design responsivo

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- 📧 Email: seu-email@exemplo.com
- 💬 Telegram: @seu_usuario
- 🐛 Issues: GitHub Issues

---

**Desenvolvido com ❤️ para a comunidade**