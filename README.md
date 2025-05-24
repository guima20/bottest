# 🤖 Sistema de Bots Telegram - Kangaroo

Sistema completo de bots do Telegram com interface administrativa visual e gerenciamento de configurações em tempo real.

## 📋 Descrição

Este projeto implementa um sistema dual de bots:

1. **Bot Principal** (`@Kangaroo_bot_bot`) - Responde aos usuários com mensagens configuráveis
2. **Bot Administrativo** (`@kangarooadm_bot`) - Interface visual para gerenciar configurações

## ✨ Funcionalidades

### 🤖 Bot Principal
- Comando `/start` envia:
  - Imagem configurável (URL ou arquivo local)
  - Texto personalizado
  - 4 botões inline configuráveis
  - Botão "🔄 Refresh" para reenvio

### 🔧 Bot Administrativo
- Interface com botões interativos
- **📊 Status Atual** - Visualiza configuração
- **📝 Alterar Texto** - Edita mensagem principal
- **🖼️ Alterar Imagem** - Upload de fotos ou URLs
- **🔘 Configurar Botões 1-4** - Edita texto, links e tipo
- **🏢 Add To Group** - Configuração global da funcionalidade
- **🔄 Tipos de Botão** - URL normal ou Add To Group
- **📋 Ver Configuração** - Exibe JSON completo
- **🔄 Atualizar Menu** - Refresh da interface

## 🚀 Instalação e Uso

### Pré-requisitos
```bash
pip install python-telegram-bot==21.0.1 python-dotenv
```

### Configuração
1. Crie arquivo `.env`:
```env
MAIN_BOT_TOKEN=seu_token_bot_principal
ADMIN_BOT_TOKEN=seu_token_bot_admin
ADMIN_IDS=id1,id2
```

2. Execute os bots:
```bash
# Bot principal
python3 unified_bot.py

# Bot administrativo
./start_admin.sh
```

## 🏢 Nova Funcionalidade: Add To Group

### ✨ O que é?
Permite que usuários adicionem o bot aos seus grupos e canais do Telegram com um simples clique.

### 🎯 Como funciona?
1. **Administrador** configura botões como "Add To Group"
2. **Usuário** clica no botão no bot principal
3. **Telegram** abre interface para escolher grupo/canal
4. **Bot** é adicionado automaticamente

### ⚙️ Configuração
- **Global**: Ativar/desativar funcionalidade
- **Por botão**: Cada botão pode ser URL ou Add To Group
- **Mensagem**: Texto personalizado ao clicar

📖 **[Guia Completo](ADD_TO_GROUP_GUIDE.md)** - Documentação detalhada

## 📁 Estrutura do Projeto

```
bottest/
├── unified_bot.py          # Bot principal
├── admin_bot.py           # Bot administrativo
├── config.json           # Configurações compartilhadas
├── start_admin.sh        # Script de inicialização admin
├── images/              # Diretório para fotos
├── test_image_upload.py # Testes do sistema
├── ADD_TO_GROUP_GUIDE.md # Guia da funcionalidade Add To Group
└── README.md           # Este arquivo
```

## 🔧 Configuração JSON

```json
{
  "image": "https://exemplo.com/imagem.jpg",
  "text": "👋 Mensagem personalizada",
  "add_to_group_enabled": true,
  "add_to_group_message": "Adicione o bot ao seu grupo!",
  "buttons": [
    {"text": "👉 Add To Group", "url": "", "type": "add_to_group"},
    {"text": "👉 Website", "url": "https://link2.com", "type": "url"},
    {"text": "👉 Support", "url": "https://link3.com", "type": "url"},
    {"text": "👉 Channel", "url": "https://link4.com", "type": "url"}
  ]
}
```

### 🆕 Novos Campos
- `add_to_group_enabled`: Ativa/desativa funcionalidade Add To Group
- `add_to_group_message`: Mensagem exibida ao clicar no botão
- `buttons[].type`: Tipo do botão ("url" ou "add_to_group")

## 🛡️ Segurança

- Acesso administrativo restrito por ID do usuário
- Validação de permissões em todas as operações
- Logs detalhados para auditoria

## 📸 Sistema de Imagens

- **Upload direto**: Envie fotos para o bot admin
- **URLs**: Suporte para links de imagens
- **Armazenamento local**: Compatibilidade entre bots
- **Preview**: Visualização após upload

## 🔄 Fluxo de Uso

1. **Configuração**: Use `@kangarooadm_bot` para configurar
2. **Teste**: Verifique com `@Kangaroo_bot_bot`
3. **Ajustes**: Volte ao admin para modificações
4. **Deploy**: Sistema pronto para produção

## 📊 Monitoramento

```bash
# Verificar status dos bots
ps aux | grep -E "(unified_bot|admin_bot)"

# Logs em tempo real
tail -f unified_bot.log
tail -f admin_bot.log
```

## 🎯 Características Técnicas

- **Linguagem**: Python 3.x
- **Framework**: python-telegram-bot 21.0.1
- **Armazenamento**: JSON local
- **Interface**: Botões inline interativos
- **Compatibilidade**: URLs e arquivos locais
- **Tratamento de erros**: Robusto com fallbacks

## 🚀 Deploy

Sistema pronto para deploy em:
- VPS/Servidor dedicado
- Docker containers
- Cloud platforms (Heroku, AWS, etc.)

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs dos bots
2. Execute `test_image_upload.py` para diagnóstico
3. Consulte a documentação do python-telegram-bot

---

**Desenvolvido com ❤️ para automação de bots Telegram**