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

# ================= CONFIGURAÇÕES =================
BOT_TOKEN = "SEU_TOKEN_AQUI"  # NÃO deixe "SEU_TOKEN_AQUI", substitua pelo token correto no Railway
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/xxxxxx/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/xxxxxx"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0xSEUCONTRATO"

# ================= GOOGLE SHEETS =================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

# ================= TEXTOS MULTILÍNGUES =================
mensagens = {
    "en": {
        "welcome": "🌱 Welcome to AgroDigital Club!\n🚀 Here you will find exclusive digital agribusiness opportunities.\n💡 Join the pre-sale and secure your strategic market position.\nChoose an option below 👇",
        "how_to_buy": "🌍 3 STEPS TO BUY TOKENS!\n\n✅ Send *BNB (BSC)* to: 0x...\n✅ Fill whitelist: {FORMS}\n✅ Tokens will be distributed after pre-sale.\n⏳ Only 48h!",
        "enter_value": "💰 Enter the amount you want to invest (min 100 USD)*",
        "default_reply": "🤖 I didn’t understand, here’s the menu 👇"
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao AgroDigital Club!\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n💡 Participe da pré-venda e garanta posição estratégica.\nEscolha uma opção 👇",
        "how_to_buy": "🌍 3 PASSOS PARA COMPRAR TOKENS!\n\n✅ Envie *BNB (BSC)* para: 0x...\n✅ Preencha whitelist: {FORMS}\n✅ Tokens serão entregues após a pré-venda.\n⏳ Apenas 48h!",
        "enter_value": "💰 Digite o valor que deseja investir (mínimo 100 USD)*",
        "default_reply": "🤖 Não entendi, aqui está o menu 👇"
    },
    "es": {
        "welcome": "🌱 Bienvenido(a) a AgroDigital Club!\n🚀 Aquí encontrarás oportunidades exclusivas en el agronegocio digital.\n💡 Participa en la preventa y asegura tu posición estratégica.\nElige una opción 👇",
        "how_to_buy": "🌍 3 PASOS PARA COMPRAR TOKENS!\n\n✅ Envía *BNB (BSC)* a: 0x...\n✅ Completa whitelist: {FORMS}\n✅ Tokens serán distribuidos después de la preventa.\n⏳ Solo 48h!",
        "enter_value": "💰 Ingresa el monto que deseas invertir (mínimo 100 USD)*",
        "default_reply": "🤖 No entendí, aquí está el menú 👇"
    }
}

# ================= MENU PRINCIPAL =================
def menu_principal(idioma="en"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 How to buy" if idioma=="en" else "🌍 Como comprar" if idioma=="pt" else "🌍 Cómo comprar", callback_data="how_to_buy")],
        [InlineKeyboardButton("📄 Open whitelist form" if idioma=="en" else "📄 Abrir formulário" if idioma=="pt" else "📄 Abrir formulario", url=GOOGLE_FORMS_URL)],
        [InlineKeyboardButton("💰 Enter the amount" if idioma=="en" else "💰 Digitar valor" if idioma=="pt" else "💰 Ingresar monto", callback_data="enter_value")],
        [InlineKeyboardButton("📊 Access panel", url=PAINEL_URL)],
        [InlineKeyboardButton("🔗 View contract on BscScan", url=BSC_SCAN_URL)],
        [InlineKeyboardButton("🌐 Change language" if idioma=="en" else "🌐 Trocar idioma" if idioma=="pt" else "🌐 Cambiar idioma", callback_data="change_lang")]
    ])

# ================= ESCOLHA DE IDIOMA =================
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    await update.message.reply_text("🌐 Please choose your language:", reply_markup=InlineKeyboardMarkup(keyboard))

# ================= INÍCIO =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["idioma"] = "en"  # Default
    await ask_language(update, context)

# ================= CALLBACK BOTÕES =================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("lang_"):
        idioma = query.data.split("_")[1]
        context.user_data["idioma"] = idioma
        await query.edit_message_text(
            mensagens[idioma]["welcome"],
            reply_markup=menu_principal(idioma)
        )
    elif query.data == "how_to_buy":
        idioma = context.user_data.get("idioma", "en")
        await query.edit_message_text(
            mensagens[idioma]["how_to_buy"].replace("{FORMS}", GOOGLE_FORMS_URL),
            reply_markup=menu_principal(idioma)
        )
    elif query.data == "enter_value":
        idioma = context.user_data.get("idioma", "en")
        await query.edit_message_text(
            mensagens[idioma]["enter_value"],
            reply_markup=menu_principal(idioma)
        )
    elif query.data == "change_lang":
        await ask_language(update, context)

# ================= MENSAGENS SOLTAS =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idioma = context.user_data.get("idioma", "en")
    await update.message.reply_text(
        mensagens[idioma]["default_reply"],
        reply_markup=menu_principal(idioma)
    )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ BOT MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
