from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo token do BotFather

# ✅ Mensagens PT + EN juntas
message_info = """
🚨 PRÉ-VENDA EXPRESS – SOMENTE 48 HORAS! 🚨  
🔥 SoByen (SBN) – Token do agronegócio digital  

✅ Pré-venda / Pre-sale: **US$ 0,03 → 0,90** (valores por lote)
✅ Compra mínima / Min buy: **US$ 5 | Máxima / Max: US$ 1.000**
✅ Pagamento / Payment: **BNB (BSC Network)**

💳 Carteira oficial / Official Wallet:
0x0d5B9634F1C33684C9d2606109B391301b95f002

⏳ Apenas 48h! Liquidez travada 12 meses  
👉 Whitelist: https://forms.gle/zVJN3BBuZgzCcGB36
"""

status_msg = """
📊 **Status da Pré-venda SBN**  
✅ Preço atual / Current price: **US$ 0,03**
✅ Próximo preço / Next price: **US$ 0,12**
✅ Lotes disponíveis / Lots available: **5**
✅ Duração / Duration: **72h**
✅ Whitelist limitada aos 500 primeiros
"""

# ✅ Menu de botões
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Informações Pré-venda / Info", callback_data='info')],
        [InlineKeyboardButton("📈 Status da pré-venda / Status", callback_data='status')],
        [InlineKeyboardButton("💼 Ver outras ofertas / Other offers", callback_data='offers')],
        [InlineKeyboardButton("💰 Investir agora / Invest now", url="https://forms.gle/zVJN3BBuZgzCcGB36")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bem-vindo(a) ao *AgroDigital Club*!\n\n🌱 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial global.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado!*\n\nEscolha uma opção abaixo para continuar 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ✅ Respostas dos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        await query.edit_message_text(text=message_info, parse_mode="Markdown")
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg, parse_mode="Markdown")
    elif query.data == 'offers':
        await query.edit_message_text("📌 Novos projetos exclusivos serão anunciados em breve! / New projects coming soon!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ BOT ONLINE E ESTÁVEL!")
    app.run_polling()

if __name__ == "__main__":
    main()
