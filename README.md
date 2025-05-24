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
- **🔘 Configurar Botões 1-4** - Edita texto e links
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

## 📁 Estrutura do Projeto

```
bottest/
├── unified_bot.py          # Bot principal
├── admin_bot.py           # Bot administrativo
├── config.json           # Configurações compartilhadas
├── start_admin.sh        # Script de inicialização admin
├── images/              # Diretório para fotos
├── test_image_upload.py # Testes do sistema
└── README.md           # Este arquivo
```

## 🔧 Configuração JSON

```json
{
  "image": "https://exemplo.com/imagem.jpg",
  "text": "👋 Mensagem personalizada",
  "buttons": [
    {"text": "Botão 1", "url": "https://link1.com"},
    {"text": "Botão 2", "url": "https://link2.com"},
    {"text": "Botão 3", "url": "https://link3.com"},
    {"text": "Botão 4", "url": "https://link4.com"}
  ]
}
```

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