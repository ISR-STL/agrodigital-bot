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

# ==================== CONFIGURAÇÕES PRINCIPAIS ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ✅ Lê token diretamente do Railway

PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuHfXv4JqZG5XIn_GfbeZJXewR0RgW7SgLD5/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital5ponto0.com"
BSC_SCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffed967987a5a5edf8dd#code"

# ==================== CONEXÃO GOOGLE SHEETS =======================
def conectar_planilha():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(PLANILHA_URL).sheet1
        return sheet
    except Exception as e:
        print(f"⚠️ Erro ao conectar planilha: {e}")
        return None

def registrar_acao(user, idioma, acao, valor="--"):
    try:
        sheet = conectar_planilha()
        if sheet:
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
        "welcome": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive digital agribusiness opportunities.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your strategic position in the market.*\n\nChoose an option below 👇",
        "menu": [
            ("🌍 How to buy", "how_to_buy"),
            ("📄 Open whitelist form", "form"),
            ("💰 Enter the amount you want to invest", "enter_amount"),
            ("📊 Access panel", "panel"),
            ("🔗 View contract on BscScan", "bscscan"),
            ("🌍 Change language", "change_lang")
        ],
        "how_to_buy": "🔥 *3 STEPS TO BUY SBN TOKENS!*\n\n✅ Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Fill the whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receive tokens after pre-sale.\n\n⏳ *Only 48h and 500 spots!*",
        "enter_value": "💵 *Enter the amount you want to invest (min 100 USD)*",
        "default_reply": "🤖 I didn’t understand your message, here’s the menu again 👇"
    },
    "pt": {
        "welcome": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\nEscolha uma opção abaixo 👇",
        "menu": [
            ("🌍 Como comprar", "how_to_buy"),
            ("📄 Abrir formulário", "form"),
            ("💰 Digitar valor que deseja investir", "enter_amount"),
            ("📊 Acessar painel", "panel"),
            ("🔗 Ver contrato na BscScan", "bscscan"),
            ("🌍 Trocar idioma", "change_lang")
        ],
        "how_to_buy": "🔥 *3 PASSOS PARA COMPRAR TOKENS SBN!*\n\n✅ Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receba seus tokens após a pré-venda.\n\n⏳ *Só 48h e 500 vagas!*",
        "enter_value": "💵 *Digite o valor que deseja investir (mínimo 100 USD)*",
        "default_reply": "🤖 Não entendi sua mensagem, aqui está o menu novamente 👇"
    },
    "es": {
        "welcome": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrarás oportunidades exclusivas en agronegocios digitales.\n\n💡 *Participa en la preventa del token SoByen (SBN) y asegura una posición estratégica en el mercado.*\n\nElige una opción abajo 👇",
        "menu": [
            ("🌍 Cómo comprar", "how_to_buy"),
            ("📄 Abrir formulario", "form"),
            ("💰 Ingresar monto a invertir", "enter_amount"),
            ("📊 Acceder al panel", "panel"),
            ("🔗 Ver contrato en BscScan", "bscscan"),
            ("🌍 Cambiar idioma", "change_lang")
        ],
        "how_to_buy": "🔥 *¡3 PASOS PARA COMPRAR TOKENS SBN!*\n\n✅ Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ Recibe tus tokens tras la preventa.\n\n⏳ *¡Solo 48h y 500 plazas!*",
        "enter_value": "💵 *Ingrese el monto que desea invertir (mínimo 100 USD)*",
        "default_reply": "🤖 No entendí tu mensaje, aquí está el menú nuevamente 👇"
    }
}

# ==================== ESCOLHER IDIOMA ==============================
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*", parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*", parse_mode="Markdown", reply_markup=reply_markup)

# ==================== MOSTRAR MENU ================================
async def show_menu(update_or_query, lang, edit=False):
    msg_text = mensagens[lang]["welcome"]
    buttons = mensagens[lang]["menu"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(update_or_query, Update):
        if update_or_query.message:
            await update_or_query.message.reply_text(msg_text, parse_mode="Markdown", reply_markup=reply_markup)
        elif update_or_query.callback_query:
            await update_or_query.callback_query.edit_message_text(msg_text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        if edit:
            await update_or_query.edit_message_text(msg_text, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== START =======================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ask_language(update, context)

# ==================== CALLBACK ====================================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("set_lang_"):
        lang = data.split("_")[-1]
        context.user_data["lang"] = lang
        await show_menu(query, lang, edit=True)

    elif data == "change_lang":
        await ask_language(update, context)

    else:
        lang = context.user_data.get("lang", "en")
        if data == "how_to_buy":
            await query.edit_message_text(mensagens[lang]["how_to_buy"].replace("{GOOGLE_FORMS_URL}", GOOGLE_FORMS_URL), parse_mode="Markdown")
        elif data == "form":
            await query.edit_message_text(f"📄 {GOOGLE_FORMS_URL}", parse_mode="Markdown")
        elif data == "panel":
            await query.edit_message_text(f"📊 {PAINEL_URL}", parse_mode="Markdown")
        elif data == "bscscan":
            await query.edit_message_text(f"🔗 {BSC_SCAN_URL}", parse_mode="Markdown")
        elif data == "enter_amount":
            await query.edit_message_text(mensagens[lang]["enter_value"], parse_mode="Markdown")
            context.user_data["awaiting_amount"] = True

# ==================== HANDLE MESSAGES ============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if context.user_data.get("awaiting_amount"):
        amount = update.message.text.strip()
        registrar_acao(update.message.from_user, lang, "Investimento", amount)
        await update.message.reply_text(f"✅ Investment of {amount} USD recorded successfully!")
        context.user_data["awaiting_amount"] = False
        await show_menu(update, lang)
    else:
        await update.message.reply_text(mensagens[lang]["default_reply"])
        await show_menu(update, lang)

# ==================== MAIN =======================================
def main():
    if not BOT_TOKEN:
        print("❌ ERRO: BOT_TOKEN não carregado! Verifique a variável no Railway.")
        return
    else:
        print("✅ BOT_TOKEN carregado com sucesso!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 BOT MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
