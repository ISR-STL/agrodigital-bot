import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==================== CONFIGURAÇÕES PRINCIPAIS ====================
BOT_TOKEN = "SEU_TOKEN_AQUI"  # ⚠️ Substitua pelo token correto do Railway
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuHfXV4JqZG5XIn_GfbeZJXewR0RgW7SgLD5/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffed967987a5a5edf8dd#code"

# ==================== CONEXÃO GOOGLE SHEETS =======================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

def registrar_acao(user, idioma, acao, valor="--"):
    try:
        sheet = conectar_planilha()
        sheet.append_row([
            user.full_name,
            f"@{user.username}" if user.username else "Sem username",
            idioma,
            acao,
            valor,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ])
    except Exception as e:
        print(f"Erro ao registrar na planilha: {e}")

# ==================== MENSAGENS MULTILÍNGUE ========================
mensagens = {
    "en": {
        "welcome": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive digital agribusiness opportunities.\n\n💡 Join the pre-sale of the SoByen (SBN) token and secure your strategic position in the market.\n\nChoose an option below 👇",
        "how_to_buy": f"🔥 *3 STEPS TO BUY SBN TOKENS!*\n\n✅ 1. Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Fill the whitelist in 30s:\n{GOOGLE_FORMS_URL}\n\n✅ 3. Tokens distributed after pre-sale.\n\n⏳ Only 48h and 500 spots!",
        "enter_value": "💵 Enter the amount you want to invest (min 100 USD)",
        "default_reply": "🤖 I didn't understand your message, but here's the main menu again 👇",
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n\n💡 Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.\n\nEscolha uma opção abaixo 👇",
        "how_to_buy": f"🔥 *3 PASSOS PARA COMPRAR SBN!*\n\n✅ 1. Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Preencha a whitelist em 30s:\n{GOOGLE_FORMS_URL}\n\n✅ 3. Receba seus tokens após a pré-venda.\n\n⏳ Somente 48h e 500 vagas!",
        "enter_value": "💵 Digite o valor que deseja investir (mínimo 100 USD)",
        "default_reply": "🤖 Não entendi sua mensagem, mas aqui está o menu principal novamente 👇",
    },
    "es": {
        "welcome": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrarás oportunidades exclusivas en el agro digital.\n\n💡 Participa en la preventa del token SoByen (SBN) y asegura tu posición estratégica en el mercado.\n\nElige una opción abajo 👇",
        "how_to_buy": f"🔥 *3 PASOS PARA COMPRAR SBN!*\n\n✅ 1. Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Completa la whitelist en 30s:\n{GOOGLE_FORMS_URL}\n\n✅ 3. Recibe tus tokens al finalizar la preventa.\n\n⏳ Solo 48h y 500 plazas!",
        "enter_value": "💵 Ingrese el monto que desea invertir (mínimo 100 USD)",
        "default_reply": "🤖 No entendí tu mensaje, pero aquí está el menú principal nuevamente 👇",
    }
}

# ==================== ESCOLHA DE IDIOMA ============================
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")]
    ]
    await update.message.reply_text(
        "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================== MENU PRINCIPAL ==============================
async def show_menu(update_or_query, idioma, edit=False):
    keyboard = [
        [InlineKeyboardButton("🌍 How to buy" if idioma == "en" else "✅ Como comprar" if idioma == "pt" else "✅ Cómo comprar", callback_data="how_to_buy")],
        [InlineKeyboardButton("📄 Open whitelist form" if idioma == "en" else "📄 Abrir formulário" if idioma == "pt" else "📄 Abrir formulario", callback_data="open_form")],
        [InlineKeyboardButton("💰 Enter the amount you want to invest" if idioma == "en" else "💰 Digite o valor que deseja investir" if idioma == "pt" else "💰 Ingrese el monto que desea invertir", callback_data="enter_amount")],
        [InlineKeyboardButton("📊 Access panel", url=PAINEL_URL)],
        [InlineKeyboardButton("🔗 View contract on BscScan", url=BSC_SCAN_URL)],
        [InlineKeyboardButton("🌍 Change language", callback_data="change_lang")]
    ]
    text = mensagens[idioma]["welcome"]

    if hasattr(update_or_query, "edit_message_text"):
        await update_or_query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update_or_query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== CALLBACK DO BOTÃO ============================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_idioma = context.user_data.get("idioma", "en")

    if query.data == "how_to_buy":
        await query.edit_message_text(mensagens[user_idioma]["how_to_buy"], parse_mode="Markdown")
    elif query.data == "open_form":
        await query.edit_message_text(f"📄 {GOOGLE_FORMS_URL}", parse_mode="Markdown")
    elif query.data == "enter_amount":
        await query.edit_message_text(mensagens[user_idioma]["enter_value"], parse_mode="Markdown")
        context.user_data["awaiting_amount"] = True
    elif query.data == "change_lang":
        await ask_language(query, context)
    elif query.data.startswith("set_lang_"):
        lang_code = query.data.split("_")[-1]
        context.user_data["idioma"] = lang_code
        await show_menu(query, lang_code, edit=True)

# ==================== MENSAGEM DE TEXTO ============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idioma = context.user_data.get("idioma", "en")

    # Se está aguardando valor
    if context.user_data.get("awaiting_amount"):
        amount = update.message.text.strip()
        registrar_acao(update.message.from_user, idioma, "Investimento", amount)
        await update.message.reply_text(f"✅ Investment of {amount} USD recorded successfully!")
        context.user_data["awaiting_amount"] = False
        await show_menu(update, idioma)
        return

    # Mensagem solta → responde e mostra menu
    await update.message.reply_text(mensagens[idioma]["default_reply"])
    await show_menu(update, idioma)

# ==================== COMANDO START ================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ask_language(update, context)

# ==================== MAIN APP ====================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ BOT MULTILÍNGUE ATIVO e aguardando interações!")
    app.run_polling()

if __name__ == "__main__":
    main()
