import os
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

# ===================== CONFIGURAÇÕES =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN não carregado! Configure no Railway corretamente.")

PLANILHA_URL = "https://docs.google.com/spreadsheets/d/xxxxxx/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/xxxxxx"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0xSEUCONTRATO"

# ===================== GOOGLE SHEETS =====================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

def registrar_acao(user, idioma, acao, valor="-"):
    try:
        sheet = conectar_planilha()
        sheet.append_row([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user.first_name,
            user.username,
            idioma,
            acao,
            valor
        ])
    except Exception as e:
        print(f"⚠️ Erro ao registrar ação: {e}")

# ===================== MENSAGENS MULTILÍNGUES =====================
mensagens = {
    "en": {
        "welcome": "🌱 Welcome to *AgroDigital Club!*\n🚀 Here you will find exclusive digital agribusiness opportunities.\n💡 Join our pre-sale and secure your strategic market position.\n\nChoose an option below 👇",
        "how_to_buy": "✅ 3 STEPS TO JOIN THE PRE-SALE:\n1️⃣ Send **BNB** to the contract.\n2️⃣ Fill the whitelist form.\n3️⃣ Wait for token distribution after pre-sale.",
        "enter_value": "💰 Enter the amount you want to invest (min 100 USD)*",
        "default_reply": "🤖 I didn’t understand your message, here’s the main menu again 👇",
        "change_lang": "🌐 Please select your language:"
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao *AgroDigital Club!*\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n💡 Participe da pré-venda e garanta posição estratégica no mercado.\n\nEscolha uma opção abaixo 👇",
        "how_to_buy": "✅ 3 PASSOS PARA PARTICIPAR DA PRÉ-VENDA:\n1️⃣ Envie **BNB** para o contrato.\n2️⃣ Preencha o formulário whitelist.\n3️⃣ Aguarde a distribuição após a pré-venda.",
        "enter_value": "💰 Digite o valor que deseja investir (mínimo 100 USD)*",
        "default_reply": "🤖 Não entendi sua mensagem, aqui está o menu novamente 👇",
        "change_lang": "🌐 Por favor, selecione o idioma:"
    },
    "es": {
        "welcome": "🌱 ¡Bienvenido(a) a *AgroDigital Club!*\n🚀 Aquí encontrarás oportunidades exclusivas en el agronegocio digital.\n💡 Participa en la preventa y asegura una posición estratégica en el mercado.\n\nElige una opción abajo 👇",
        "how_to_buy": "✅ 3 PASOS PARA PARTICIPAR EN LA PREVENTA:\n1️⃣ Envía **BNB** al contrato.\n2️⃣ Completa el formulario whitelist.\n3️⃣ Espera la distribución después de la preventa.",
        "enter_value": "💰 Ingrese el monto que desea invertir (mínimo 100 USD)*",
        "default_reply": "🤖 No entendí tu mensaje, aquí está el menú nuevamente 👇",
        "change_lang": "🌐 Por favor, selecciona el idioma:"
    }
}

# ===================== FUNÇÃO SEGURA PARA REPLY =====================
async def safe_reply(update: Update, text: str, **kwargs):
    if update.message:
        return await update.message.reply_text(text, **kwargs)
    elif update.callback_query and update.callback_query.message:
        return await update.callback_query.message.reply_text(text, **kwargs)
    else:
        print("⚠️ Nenhuma mensagem válida para reply_text")
        return None

# ===================== MENU =====================
def menu_principal(idioma):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 How to buy", callback_data="how_to_buy")],
        [InlineKeyboardButton("📝 Open whitelist form", url=GOOGLE_FORMS_URL)],
        [InlineKeyboardButton("💰 Enter the amount you want to invest", callback_data="enter_value")],
        [InlineKeyboardButton("📊 Access panel", url=PAINEL_URL)],
        [InlineKeyboardButton("🔗 View contract on BscScan", url=BSC_SCAN_URL)],
        [InlineKeyboardButton("🌐 Change language", callback_data="change_lang")]
    ])

async def show_menu(update: Update, idioma: str):
    text = mensagens[idioma]["welcome"]
    reply_markup = menu_principal(idioma)
    await safe_reply(update, text, reply_markup=reply_markup, parse_mode="Markdown")

# ===================== FLUXO DE IDIOMA =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ask_language(update, context)

async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await safe_reply(update, "🌐 Please select your language / Por favor selecione o idioma:", reply_markup=reply_markup)

# ===================== CALLBACK BUTTON =====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("set_lang_"):
        lang = query.data.split("_")[-1]
        context.user_data["idioma"] = lang
        return await show_menu(update, lang)

    idioma = context.user_data.get("idioma", "en")

    if query.data == "how_to_buy":
        await query.edit_message_text(mensagens[idioma]["how_to_buy"])
    elif query.data == "enter_value":
        await query.edit_message_text(mensagens[idioma]["enter_value"])
    elif query.data == "change_lang":
        await ask_language(update, context)
    else:
        await show_menu(update, idioma)

# ===================== MENSAGENS SOLTAS =====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idioma = context.user_data.get("idioma", "en")
    await safe_reply(update, mensagens[idioma]["default_reply"])
    await show_menu(update, idioma)

# ===================== MAIN =====================
def main():
    print("🚀 Iniciando bot AgroDigital...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BOT MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
