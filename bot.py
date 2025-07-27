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

# ======================= CONFIGURAÇÕES PRINCIPAIS =======================
BOT_TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo token correto do Railway
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1IiHufHXV4JqZG5XIn_GfbeZJXewR0RgW7SgLD5/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffed967987a5a5edf8dd#code"

# ======================= CONEXÃO GOOGLE SHEETS =======================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

# ======================= MENSAGENS MULTILÍNGUES =======================
mensagens = {
    "en": {
        "welcome": "🌱 Welcome to AgroDigital Club!\n\n🚀 Here you will find exclusive opportunities in digital agribusiness.\n\n💡 Join the exclusive pre-sale of AgroDigital tokens and secure your strategic market position.\n\nChoose an option below 👇",
        "how_to_buy": "🌍 3 STEPS TO BUY TOKENS!\n\n✅ Send **BNB (BSC Network)** to:\n`0xd85f998f4c136b46AC9a0b1091913B105f002`\n✅ Fill the whitelist here:\n" + GOOGLE_FORMS_URL + "\n✅ Tokens will be distributed after pre-sale.\n\n⏳ Limited spots available!",
        "enter_value": "💰 Enter the amount you want to invest (min 100 USD)",
        "default_reply": "🤖 I didn’t understand your message, here’s the menu again 👇",
        "menu_buttons": ["🌍 How to buy", "📄 Open whitelist form", "💵 Enter amount", "📊 Access panel", "🔗 View contract on BscScan", "🌎 Change language"]
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao AgroDigital Club!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n\n💡 Participe da pré-venda exclusiva dos tokens AgroDigital e garanta posição estratégica no mercado.\n\nEscolha uma opção abaixo 👇",
        "how_to_buy": "🌍 3 PASSOS PARA COMPRAR TOKENS!\n\n✅ Envie **BNB (Rede BSC)** para:\n`0xd85f998f4c136b46AC9a0b1091913B105f002`\n✅ Preencha o formulário aqui:\n" + GOOGLE_FORMS_URL + "\n✅ Tokens serão distribuídos após a pré-venda.\n\n⏳ Vagas limitadas!",
        "enter_value": "💰 Digite o valor que deseja investir (mínimo 100 USD)",
        "default_reply": "🤖 Não entendi sua mensagem, aqui está o menu novamente 👇",
        "menu_buttons": ["🌍 Como comprar", "📄 Abrir formulário", "💵 Digitar valor que deseja investir", "📊 Acessar painel", "🔗 Ver contrato na BscScan", "🌎 Trocar idioma"]
    },
    "es": {
        "welcome": "🌱 ¡Bienvenido(a) al AgroDigital Club!\n\n🚀 Aquí encontrarás oportunidades exclusivas en el agronegocio digital.\n\n💡 Participa en la preventa exclusiva de los tokens AgroDigital y asegura tu posición estratégica en el mercado.\n\nElige una opción abajo 👇",
        "how_to_buy": "🌍 3 PASOS PARA COMPRAR TOKENS!\n\n✅ Envía **BNB (Red BSC)** a:\n`0xd85f998f4c136b46AC9a0b1091913B105f002`\n✅ Completa el formulario aquí:\n" + GOOGLE_FORMS_URL + "\n✅ Los tokens serán distribuidos después de la preventa.\n\n⏳ ¡Cupos limitados!",
        "enter_value": "💰 Ingrese el monto que desea invertir (mínimo 100 USD)",
        "default_reply": "🤖 No entendí tu mensaje, aquí está el menú nuevamente 👇",
        "menu_buttons": ["🌍 Cómo comprar", "📄 Abrir formulario", "💵 Ingresar monto a invertir", "📊 Acceder al panel", "🔗 Ver contrato en BscScan", "🌎 Cambiar idioma"]
    }
}

# ======================= TELAS =======================
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")]
    ]
    await update.message.reply_text("🌎 Please select your language / Por favor, escolha seu idioma / Seleccione su idioma:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_menu(update_or_query, idioma="en", edit=False):
    buttons = [
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][0], callback_data="how_to_buy")],
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][1], url=GOOGLE_FORMS_URL)],
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][2], callback_data="enter_value")],
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][3], url=PAINEL_URL)],
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][4], url=BSC_SCAN_URL)],
        [InlineKeyboardButton(mensagens[idioma]["menu_buttons"][5], callback_data="change_lang")]
    ]
    text = mensagens[idioma]["welcome"]
    markup = InlineKeyboardMarkup(buttons)

    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text, reply_markup=markup)
    else:
        await update_or_query.edit_message_text(text, reply_markup=markup)

# ======================= HANDLERS =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sempre força escolha de idioma na primeira vez
    await ask_language(update, context)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Troca de idioma
    if query.data.startswith("set_lang_"):
        new_lang = query.data.replace("set_lang_", "")
        context.user_data["idioma"] = new_lang
        await show_menu(query, new_lang, edit=True)
        return

    # Mostrar menu para trocar idioma
    if query.data == "change_lang":
        await ask_language(query, context)
        return

    idioma = context.user_data.get("idioma", "en")

    if query.data == "how_to_buy":
        await query.edit_message_text(mensagens[idioma]["how_to_buy"])
    elif query.data == "enter_value":
        await query.edit_message_text(mensagens[idioma]["enter_value"])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idioma = context.user_data.get("idioma", "en")
    # Fallback para qualquer mensagem fora do fluxo
    await update.message.reply_text(mensagens[idioma]["default_reply"])
    await show_menu(update, idioma)

# ======================= MAIN =======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BOT MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
