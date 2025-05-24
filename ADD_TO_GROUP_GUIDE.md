# 🏢 Guia da Funcionalidade "Add To Group"

## 📋 Visão Geral

A funcionalidade **Add To Group** permite que usuários adicionem o bot aos seus grupos e canais do Telegram de forma simples e intuitiva. Esta funcionalidade utiliza o recurso `SwitchInlineQueryChosenChat` do Telegram.

## ✨ Características

### 🔧 Configuração Flexível
- ✅ **Ativar/Desativar** a funcionalidade globalmente
- 📝 **Mensagem personalizada** quando o usuário clica no botão
- 🔄 **Configuração por botão** - cada botão pode ser URL ou Add To Group

### 🎯 Tipos de Botão Disponíveis
1. **🔗 URL** - Link normal (padrão)
2. **🏢 Add To Group** - Permite adicionar bot a grupos/canais

## 🚀 Como Usar

### 👨‍💼 Para Administradores

#### 1. Configuração Global
```
/start no bot administrativo
→ 🏢 Configurar Add To Group
→ ✅ Ativar (para habilitar)
→ 📝 Alterar Mensagem (personalizar texto)
```

#### 2. Configuração por Botão
```
/start no bot administrativo
→ 🔘 Botão [1-4]
→ 🔄 Tipo: [URL/Add To Group]
```

#### 3. Verificar Status
```
/start no bot administrativo
→ 📋 Ver Configuração
```

### 👥 Para Usuários

1. **Enviar** `/start` no bot principal
2. **Clicar** no botão configurado como "Add To Group"
3. **Escolher** o grupo/canal onde adicionar o bot
4. **Confirmar** a adição

## ⚙️ Configuração Técnica

### 📄 Arquivo config.json
```json
{
  "add_to_group_enabled": true,
  "add_to_group_message": "Adicione o bot ao seu grupo!",
  "buttons": [
    {
      "text": "👉 Add To Group",
      "url": "",
      "type": "add_to_group"
    },
    {
      "text": "👉 Visit Website",
      "url": "https://example.com",
      "type": "url"
    }
  ]
}
```

### 🔧 Campos de Configuração

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `add_to_group_enabled` | boolean | Ativa/desativa a funcionalidade |
| `add_to_group_message` | string | Mensagem exibida ao clicar |
| `buttons[].type` | string | "url" ou "add_to_group" |

## 🎮 Interface Administrativa

### 📱 Menu Principal
```
🤖 Bot Administrativo - Status

🖼️ Imagem: ✅ Configurada
📝 Texto: ✅ Configurado
🏢 Add To Group: ✅ Ativado
🔘 Botões: 4/4 configurados

[🖼️ Alterar Imagem] [📝 Alterar Texto]
[🔘 Botão 1] [🔘 Botão 2]
[🔘 Botão 3] [🔘 Botão 4]
[🏢 Configurar Add To Group]
[📋 Ver Configuração] [🔄 Atualizar Menu]
```

### 🏢 Menu Add To Group
```
🏢 Configuração Add To Group

📊 Status: ✅ Ativado
📝 Mensagem: Adicione o bot ao grupo!

[❌ Desativar] [📝 Alterar Mensagem] [🔙 Voltar]
```

### 🔘 Menu de Botão
```
🔘 Configuração do Botão 1

📝 Texto atual: 👉 Add To Group
🔗 Link atual: 
🏢 Tipo: Add To Group

[📝 Alterar Texto] [🔗 Alterar Link]
[🔄 Tipo: Add To Group] [🔙 Voltar]
```

## 🔍 Visualização da Configuração

### 📋 Status Completo
```
📋 Configuração Atual:

🖼️ Imagem: https://example.com/image.jpg

📝 Texto: 
👋 Olá! REGISTRE-SE para receber CHIPS GRÁTIS até $130 👇

🏢 Add To Group:
• Status: ✅ Ativado
• Mensagem: Adicione o bot ao grupo!

🔘 Botões:
  1. 🏢 👉 Add To Group → 
  2. 🔗 👉 Visit Website → https://example.com
  3. 🔗 👉 Support → https://support.com
  4. 🔗 👉 Join Channel → https://t.me/channel
```

## 🛠️ Implementação Técnica

### 📦 Dependências
```python
from telegram import InlineKeyboardButton, SwitchInlineQueryChosenChat
```

### 🔧 Lógica do Botão
```python
if button.get('type') == 'add_to_group' and config.get('add_to_group_enabled', False):
    switch_query = SwitchInlineQueryChosenChat(
        query=config.get('add_to_group_message', 'Adicione o bot ao grupo!'),
        allow_group_chats=True,
        allow_supergroup_chats=True,
        allow_channel_chats=True
    )
    keyboard_row.append(InlineKeyboardButton(
        text=button.get('text', 'Add To Group'),
        switch_inline_query_chosen_chat=switch_query
    ))
else:
    # Botão URL normal
    keyboard_row.append(InlineKeyboardButton(
        text=button.get('text', 'Link'),
        url=button.get('url', 'https://telegram.org')
    ))
```

## 🎯 Casos de Uso

### 🏪 Bot de Loja
- Botão 1: 🏢 "Adicionar ao Grupo de Vendas"
- Botão 2: 🔗 "Ver Catálogo"
- Botão 3: 🔗 "Suporte"
- Botão 4: 🔗 "Canal de Ofertas"

### 🎮 Bot de Jogos
- Botão 1: 🏢 "Adicionar ao Grupo de Jogadores"
- Botão 2: 🔗 "Jogar Agora"
- Botão 3: 🔗 "Ranking"
- Botão 4: 🔗 "Regras"

### 📢 Bot de Notícias
- Botão 1: 🏢 "Adicionar ao Grupo"
- Botão 2: 🔗 "Últimas Notícias"
- Botão 3: 🔗 "Assinar Newsletter"
- Botão 4: 🔗 "Contato"

## 🔒 Segurança

- ✅ **Verificação de Admin** - Apenas administradores podem configurar
- ✅ **Validação de Dados** - Configurações são validadas antes de salvar
- ✅ **Fallback Seguro** - Se Add To Group estiver desabilitado, usa URL padrão

## 📈 Benefícios

### 👥 Para Usuários
- **Facilidade** - Um clique para adicionar o bot
- **Flexibilidade** - Escolhe onde adicionar
- **Controle** - Pode cancelar a operação

### 👨‍💼 Para Administradores
- **Configuração Simples** - Interface intuitiva
- **Controle Total** - Ativar/desativar quando necessário
- **Personalização** - Mensagens customizadas

### 🤖 Para o Bot
- **Crescimento Orgânico** - Usuários adicionam a grupos
- **Alcance Maior** - Presença em múltiplos grupos
- **Engajamento** - Interação direta com comunidades

## 🚀 Próximos Passos

1. **Testar** a funcionalidade em ambiente de produção
2. **Monitorar** métricas de adição a grupos
3. **Coletar** feedback dos usuários
4. **Otimizar** mensagens e interface

---

**📝 Nota:** Esta funcionalidade requer que o bot tenha permissões adequadas nos grupos onde for adicionado.