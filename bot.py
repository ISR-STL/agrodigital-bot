import datetime
import gspread
import os
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
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Agora busca direto do Railway
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN não encontrado! Verifique as variáveis no Railway.")

PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuHfXv4JqZG5XIn_GfbeZJXewR0RgW7SgLD5/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital-panel-git-main-isr-stls-projects.vercel.app/"
BSCSCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffed967987a5a5edf8dd#code"

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

# ==================== MENSAGENS POR IDIOMA ========================
mensagens = {
    "en": {
        "welcome": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive digital agribusiness opportunities.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your strategic position in the market.*\n\nChoose an option below 👇",
        "buttons": [
            ("🌍 How to buy", "how_to_buy"),
            ("📄 Open whitelist form", "open_form"),
            ("💰 Enter the amount you want to invest", "enter_amount"),
            ("📊 Access panel", "access_panel"),
            ("🔗 View contract on BscScan", "bscscan"),
            ("🌍 Change language", "change_lang")
        ],
        "how_to_buy": "🔥 *3 STEPS TO BUY SBN TOKENS!*\n\n✅ Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Fill the whitelist here:\n{GOOGLE_FORMS_URL}\n✅ Tokens will be distributed after pre-sale.\n⏳ *Only 48h and 500 spots!*",
        "enter_value": "💵 *Enter the amount you want to invest (min 100 USD)*"
    },
    "pt": {
        "welcome": "🌍 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta sua posição estratégica no mercado.*\n\nEscolha uma opção abaixo 👇",
        "buttons": [
            ("🌍 Como comprar", "how_to_buy"),
            ("📄 Abrir formulário whitelist", "open_form"),
            ("💰 Informar valor que deseja investir", "enter_amount"),
            ("📊 Acessar painel", "access_panel"),
            ("🔗 Ver contrato no BscScan", "bscscan"),
            ("🌍 Alterar idioma", "change_lang")
        ],
        "how_to_buy": "🔥 *3 PASSOS PARA COMPRAR SEUS TOKENS SBN!*\n\n✅ Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receba os tokens após o fim da pré-venda.\n⏳ *Somente 48h e 500 vagas!*",
        "enter_value": "💵 *Digite o valor que deseja investir (mínimo 100 USD)*"
    },
    "es": {
        "welcome": "🌍 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrará oportunidades exclusivas en el agronegocio digital.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure su posición estratégica en el mercado.*\n\nSeleccione una opción abajo 👇",
        "buttons": [
            ("🌍 Cómo comprar", "how_to_buy"),
            ("📄 Abrir formulario whitelist", "open_form"),
            ("💰 Ingresar el monto que desea invertir", "enter_amount"),
            ("📊 Acceder al panel", "access_panel"),
            ("🔗 Ver contrato en BscScan", "bscscan"),
            ("🌍 Cambiar idioma", "change_lang")
        ],
        "how_to_buy": "🔥 *¡3 PASOS PARA COMPRAR TUS TOKENS SBN!*\n\n✅ Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ Recibe los tokens al finalizar la preventa.\n⏳ *¡Solo 48h y 500 plazas!*",
        "enter_value": "💵 *Ingrese el monto que desea invertir (mínimo 100 USD)*"
    }
}

# ==================== MENU INICIAL ============================
async def show_menu(update_or_query, idioma, edit=False):
    text = mensagens[idioma]["welcome"]
    btns = mensagens[idioma]["buttons"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in btns]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await update_or_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update_or_query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ==================== START COMMAND ===========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # idioma padrão inglês
    context.user_data["idioma"] = "en"
    await show_menu(update, "en")

# ==================== CALLBACK BUTTONS ========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")

    if query.data == "how_to_buy":
        await query.edit_message_text(
            mensagens[idioma]["how_to_buy"].replace("{GOOGLE_FORMS_URL}", GOOGLE_FORMS_URL),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]])
        )

    elif query.data == "open_form":
        await query.edit_message_text(
            f"📄 {GOOGLE_FORMS_URL}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]])
        )

    elif query.data == "enter_amount":
        await query.edit_message_text(
            mensagens[idioma]["enter_value"],
            parse_mode="Markdown"
        )
        context.user_data['awaiting_amount'] = True

    elif query.data == "access_panel":
        await query.edit_message_text(
            f"📊 Access the full panel here:\n{PAINEL_URL}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]])
        )

    elif query.data == "bscscan":
        await query.edit_message_text(
            f"🔗 Verified contract:\n{BSCSCAN_URL}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]])
        )

    elif query.data == "change_lang":
        keyboard = [
            [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")],
            [InlineKeyboardButton("🇧🇷 Português", callback_data="set_lang_pt")],
            [InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]
        ]
        await query.edit_message_text("🌍 Select your language:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("set_lang_"):
        new_lang = query.data.replace("set_lang_", "")
        context.user_data["idioma"] = new_lang
        await show_menu(query, new_lang, edit=True)

    elif query.data == "back_menu":
        await show_menu(query, idioma, edit=True)

# ==================== AMOUNT MESSAGE ==========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_amount"):
        amount = update.message.text.strip()
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Investimento", amount)
        await update.message.reply_text(f"✅ Investment of {amount} USD recorded successfully!")
        context.user_data['awaiting_amount'] = False
        await show_menu(update, idioma)

# ==================== MAIN ============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ BOT ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
