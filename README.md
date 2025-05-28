# 🤖 Sistema de Bots Telegram - Kangaroo

Um sistema completo de bots para Telegram com interface gráfica, composto por um bot principal para interação com grupos e um bot administrativo para gerenciamento.

## 📥 Download Direto

**🔗 Link para download:** [https://github.com/guima20/bottest/archive/refs/heads/main.zip](https://github.com/guima20/bottest/archive/refs/heads/main.zip)

**📂 Repositório GitHub:** [https://github.com/guima20/bottest](https://github.com/guima20/bottest)

### Instruções de Download:
1. **Download direto:** Clique no link acima para baixar o arquivo ZIP
2. **Clone via Git:** `git clone https://github.com/guima20/bottest.git`
3. **Download manual:** Acesse o repositório e clique em "Code" → "Download ZIP"

## 📋 Características

### Bot Principal (Kangaroo)
- ✅ Coleta automática de chat_id quando adicionado a grupos
- ✅ Comando `/start` para registro e ativação
- ✅ Mensagens de boas-vindas personalizáveis
- ✅ Processamento de mensagens agendadas
- ✅ Botões inline customizáveis
- ✅ Verificação periódica de mensagens pendentes

### Bot Administrativo
- ✅ Verificação de permissões de administrador
- ✅ Envio de mensagens para grupos específicos ou todos
- ✅ Agendamento de mensagens
- ✅ Interface com botões inline
- ✅ Sistema de logs
- ✅ Gerenciamento de grupos
- ✅ Configurações personalizáveis

### Interface Gráfica (GUI)
- ✅ Controle completo dos bots via tkinter
- ✅ Monitoramento em tempo real
- ✅ Gerenciamento de grupos
- ✅ Envio de mensagens
- ✅ Configuração de boas-vindas
- ✅ Visualização de logs
- ✅ Estatísticas do sistema

## 🚀 Instalação e Uso

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd guima20-project

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração

Edite o arquivo `.env` com seus tokens e configurações:

```env
TELEGRAM_BOT_TOKEN=7862546836:AAHtlgCVOdrI5saF0Ca4ruX1c56FyVHUQAE
TELEGRAM_ADMIN_BOT_TOKEN=7727769382:AAEvsuGUALNt5rDLjyOdHaTRKnJmu36ch5A
ADMIN_IDS=123456789,987654321
TELEGRAM_CHAT_ID=-100123456789
```

### 3. Inicialização

#### Opção 1: Interface Gráfica (Recomendado)
```bash
python start_gui.py
```

#### Opção 2: Linha de Comando
```bash
# Terminal 1 - Bot Principal
python unified_bot.py

# Terminal 2 - Bot Administrativo  
python admin_bot.py
```

## 📁 Estrutura de Arquivos

```
/
├── unified_bot.py          # Bot principal (Kangaroo)
├── admin_bot.py            # Bot administrativo
├── bot_messages.py         # Gerenciamento de mensagens
├── gui_manager.py          # Interface gráfica
├── start_gui.py            # Script de inicialização
├── config.json             # Configurações do bot principal
├── groups.json             # Registro de grupos
├── pending_messages.json   # Mensagens agendadas
├── requirements.txt        # Dependências
├── .env                    # Variáveis de ambiente
└── README.md              # Este arquivo
```

## 🎯 Funcionalidades Principais

### 📱 Gerenciamento de Grupos
- Registro automático quando o bot é adicionado
- Visualização de grupos cadastrados
- Remoção de grupos
- Estatísticas de membros

### 💬 Sistema de Mensagens
- Envio imediato para grupos específicos ou todos
- Agendamento de mensagens
- Botões personalizáveis
- Histórico de mensagens enviadas

### ⚙️ Configurações
- Mensagem de boas-vindas personalizável
- Botões inline configuráveis
- Configurações de administradores
- Logs do sistema

### 🖥️ Interface Gráfica
- **Controle de Bots**: Iniciar/parar bots com um clique
- **Estatísticas**: Visualização em tempo real
- **Gerenciamento**: Grupos, mensagens e configurações
- **Logs**: Monitoramento completo do sistema

## 🔧 Configuração Avançada

### Tokens dos Bots
1. Crie os bots no [@BotFather](https://t.me/BotFather)
2. Obtenha os tokens
3. Configure no arquivo `.env`

### Administradores
1. Obtenha seu ID do Telegram (use [@userinfobot](https://t.me/userinfobot))
2. Adicione ao `ADMIN_IDS` no `.env`
3. Separe múltiplos IDs com vírgula

### Canal de Logs
1. Crie um canal ou grupo
2. Adicione o bot administrativo
3. Configure o `TELEGRAM_CHAT_ID` no `.env`

## 📊 Monitoramento

### Logs do Sistema
- Inicialização dos bots
- Mensagens enviadas
- Erros e avisos
- Atividades administrativas

### Estatísticas
- Número de grupos cadastrados
- Mensagens pendentes
- Última verificação
- Status dos bots

## 🛠️ Solução de Problemas

### Bot não inicia
1. Verifique se o token está correto
2. Confirme se as dependências estão instaladas
3. Verifique as permissões de arquivo

### Mensagens não são enviadas
1. Verifique se o bot está ativo nos grupos
2. Confirme se há mensagens pendentes
3. Verifique os logs para erros

### Interface gráfica não abre
1. Verifique se o tkinter está instalado
2. Use o modo de linha de comando como alternativa
3. Verifique os logs de erro

## 🔒 Segurança

- ✅ Verificação de permissões de administrador
- ✅ Tokens seguros via variáveis de ambiente
- ✅ Logs de todas as atividades
- ✅ Validação de entrada de dados

## 📝 Logs

O sistema mantém logs detalhados de:
- Inicialização e parada dos bots
- Mensagens enviadas e recebidas
- Erros e exceções
- Atividades administrativas
- Alterações de configuração

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato via Telegram
- Consulte a documentação

---

**Desenvolvido com ❤️ para a comunidade Telegram**
