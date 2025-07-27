import datetime
import gspread
import os  # ✅ Para ler variáveis de ambiente do Railway
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

# =================== CONFIGURAÇÕES PRINCIPAIS ===================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ✅ Agora pega o token automaticamente do Railway

if not BOT_TOKEN:
    raise ValueError("❌ ERRO: BOT_TOKEN não foi encontrado! Configure no Railway.")

PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1i1HuHfXV4JqZG5XIn_GfbeZJXewR0RgN7SgLD5/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffed967987a5a5edf8dd#code"

# =================== CONEXÃO GOOGLE SHEETS ===================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

def registrar_acao(user, idioma, acao, valor="-"):
    try:
        sheet = conectar_planilha()
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([agora, user.first_name, user.id, idioma, acao, valor])
    except Exception as e:
        print(f"Erro ao registrar ação: {e}")

# =================== MENSAGENS MULTILÍNGUES ===================
mensagens = {
    "en": {
        "welcome": "🌱 Welcome to AgroDigital Club!\n🚀 Here you will find exclusive digital agribusiness opportunities.\n💡 Join the pre-sale and secure your strategic market position.\nChoose an option below 👇",
        "how_to_buy": "🌍 3 STEPS TO BUY TOKENS:\n✅ Send *BNB (BSC Network)* to the official address.\n✅ Fill the whitelist here:\n{GOOGLE_FORMS_URL}\n✅ Tokens will be distributed after pre-sale.\n⏳ Only 48h and 500 spots!",
        "enter_value": "💰 Enter the amount you want to invest (min 100 USD)*",
        "default_reply": "🤖 I didn’t understand your message, here’s the main menu again 👇"
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao AgroDigital Club!\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n💡 Participe da pré-venda e garanta posição estratégica no mercado.\nEscolha uma opção abaixo 👇",
        "how_to_buy": "🌍 3 PASSOS PARA COMPRAR TOKENS:\n✅ Envie *BNB (Rede BSC)* para o endereço oficial.\n✅ Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receba os tokens após o fim da pré-venda.\n⏳ Apenas 48h e 500 vagas!",
        "enter_value": "💰 Digite o valor que deseja investir (mínimo 100 USD)*",
        "default_reply": "🤖 Não entendi sua mensagem, aqui está o menu principal novamente 👇"
    },
    "es": {
        "welcome": "🌱 Bienvenido(a) al AgroDigital Club!\n🚀 Aquí encontrarás oportunidades exclusivas en el agronegocio digital.\n💡 Participa en la preventa y asegura tu posición estratégica en el mercado.\nElige una opción abajo 👇",
        "how_to_buy": "🌍 3 PASOS PARA COMPRAR TOKENS:\n✅ Envía *BNB (Red BSC)* a la dirección oficial.\n✅ Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ Recibe los tokens al finalizar la preventa.\n⏳ ¡Solo 48h y 500 plazas!",
        "enter_value": "💰 Ingrese el monto que desea invertir (mínimo 100 USD)*",
        "default_reply": "🤖 No entendí tu mensaje, aquí está el menú principal nuevamente 👇"
    }
}

# =================== ESCOLHA DE IDIOMA ===================
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")]
    ]
    await update.message.reply_text(
        "🌍 Please select your language / Por favor selecione seu idioma / Por favor seleccione su idioma:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =================== MENU PRINCIPAL ===================
async def show_menu(update_or_query, idioma="en", edit=False):
    text = mensagens[idioma]["welcome"]
    keyboard = [
        [InlineKeyboardButton("🌍 " + ("How to buy" if idioma == "en" else "Como comprar" if idioma == "pt" else "Cómo comprar"), callback_data="how_to_buy")],
        [InlineKeyboardButton("📄 " + ("Open whitelist form" if idioma == "en" else "Abrir formulário" if idioma == "pt" else "Abrir formulario"), url=GOOGLE_FORMS_URL)],
        [InlineKeyboardButton("💰 " + ("Enter the amount you want to invest" if idioma == "en" else "Digitar valor que deseja investir" if idioma == "pt" else "Ingresar monto a invertir"), callback_data="enter_value")],
        [InlineKeyboardButton("📊 Access panel", url=PAINEL_URL)],
        [InlineKeyboardButton("🔗 View contract on BscScan", url=BSC_SCAN_URL)],
        [InlineKeyboardButton("🌍 " + ("Change language" if idioma == "en" else "Trocar idioma" if idioma == "pt" else "Cambiar idioma"), callback_data="change_lang")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if edit and hasattr(update_or_query, "edit_message_text"):
        await update_or_query.edit_message_text(text, reply_markup=markup)
    else:
        await update_or_query.message.reply_text(text, reply_markup=markup)

# =================== CALLBACK BOTÕES ===================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    idioma = context.user_data.get("idioma", "en")

    if data == "how_to_buy":
        await query.edit_message_text(mensagens[idioma]["how_to_buy"].replace("{GOOGLE_FORMS_URL}", GOOGLE_FORMS_URL))
    elif data == "enter_value":
        await query.edit_message_text(mensagens[idioma]["enter_value"])
    elif data == "change_lang":
        await ask_language(update, context)
    elif data.startswith("set_lang_"):
        idioma = data.replace("set_lang_", "")
        context.user_data["idioma"] = idioma
        await show_menu(query, idioma, edit=True)

# =================== MENSAGENS LIVRES ===================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idioma = context.user_data.get("idioma", "en")
    await update.message.reply_text(mensagens[idioma]["default_reply"])
    await show_menu(update, idioma)

# =================== START BOT ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ask_language(update, context)

# =================== MAIN ===================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BOT MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
