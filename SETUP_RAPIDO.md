# 🚀 Setup Rápido - Bots do Telegram

## ✅ APIs Já Configuradas

Os tokens dos bots já estão configurados:

- **Bot Principal**: `7862546836:AAHtlgCVOdrI5saF0Ca4ruX1c56FyVHUQAE`
- **Bot Admin**: `7727769382:AAEvsuGUALNt5rDLjyOdHaTRKnJmu36ch5A`

## 🔧 Configuração Necessária

### 1. Descobrir seu ID do Telegram

Para usar o bot administrativo, você precisa do seu ID do Telegram:

1. Abra o Telegram
2. Procure por `@userinfobot`
3. Envie `/start` para ele
4. Ele retornará seu ID (ex: `123456789`)

### 2. Atualizar o ID de Admin

Edite o arquivo `.env` e substitua `123456789` pelo seu ID real:

```bash
ADMIN_IDS=SEU_ID_AQUI
```

## 🚀 Executar os Bots

### Opção 1: Execução Rápida (Recomendada)
```bash
python run_bots_production.py
```

### Opção 2: Execução Separada
```bash
# Terminal 1 - Bot Principal
python telegram_bot.py

# Terminal 2 - Bot Admin
python admin_bot.py
```

## 📱 Como Testar

### Bot Principal
1. Procure por seu bot principal no Telegram
2. Envie `/start`
3. Você verá: imagem + texto + 4 botões + refresh

### Bot Administrativo
1. Procure por seu bot admin no Telegram
2. Envie `/start`
3. Use a interface interativa para configurar:
   - 📝 Alterar texto
   - 📸 Enviar foto ou URL de imagem
   - 🔘 Configurar botões

## 🎯 Interface do Bot Admin

O bot administrativo tem uma interface super amigável:

- **📝 Alterar Texto**: Clique e digite o novo texto
- **📸 Alterar Imagem**: Envie uma foto diretamente ou cole uma URL
- **🔘 Botões 1-4**: Configure texto e link de cada botão
- **📋 Ver Configuração**: Mostra as configurações atuais
- **🔄 Atualizar**: Recarrega o menu

## 💡 Dicas Importantes

1. **Upload de Imagens**: Envie fotos diretamente no chat do bot admin
2. **URLs**: Devem começar com `http://` ou `https://`
3. **Emojis**: Use emojis para tornar mais atrativo
4. **Alterações**: São aplicadas imediatamente no bot principal

## 🔒 Segurança

- Apenas usuários com ID configurado em `ADMIN_IDS` podem usar o bot admin
- Todas as configurações são salvas localmente em `config.json`
- Logs detalhados para monitoramento

## 🆘 Resolução de Problemas

### Bot não responde
- Verifique se os tokens estão corretos
- Confirme que o bot está rodando
- Veja os logs para erros

### Não consigo acessar o bot admin
- Confirme que seu ID está em `ADMIN_IDS`
- Use `@userinfobot` para descobrir seu ID correto

### Imagem não aparece
- Teste com uma URL pública de imagem
- Ou envie uma foto diretamente no bot admin

## 📞 Suporte

Se tiver problemas:
1. Verifique os logs no terminal
2. Confirme as configurações no `.env`
3. Teste com `/help` nos bots

---

**🎉 Pronto! Seus bots estão configurados e prontos para uso!**