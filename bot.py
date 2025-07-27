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

# ==================== CONFIGURAÇÕES ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ✅ Variável do Railway
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuHfX.../edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital-panel-git-main-isr-stls-projects.vercel.app/"
BSCSCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffded967987a5a5edf8d8#code"

# ==================== CONEXÃO GOOGLE SHEETS ====================
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

# ==================== MENSAGENS MULTILÍNGUES ====================
mensagens = {
    "pt": {
        "bemvindo": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\nEscolha uma opção abaixo 👇",
        "botoes": [
            ("✅ Como comprar", "comprar"),
            ("📄 Abrir whitelist", "formulario"),
            ("💰 Informar valor que deseja investir", "investir"),
            ("📊 Acessar painel", "painel"),
            ("🔗 Ver contrato BscScan", "bscscan"),
            ("🌍 Trocar idioma", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *3 PASSOS PARA GARANTIR SEUS TOKENS!*\n\n✅ Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receba seus tokens após a pré-venda.\n\n⏳ *Só 48h e 500 vagas!*",
        "retornar": "⬅ Voltar ao menu"
    },
    "en": {
        "bemvindo": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive digital agribusiness opportunities.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your position in the market.*\n\nChoose an option below 👇",
        "botoes": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter the amount you want to invest", "investir"),
            ("📊 Access panel", "painel"),
            ("🔗 View contract on BscScan", "bscscan"),
            ("🌍 Change language", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *3 QUICK STEPS TO GET YOUR TOKENS!*\n\n✅ Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Fill the whitelist:\n{GOOGLE_FORMS_URL}\n✅ Tokens will be delivered after pre-sale.\n\n⏳ *Only 48h and 500 spots!*",
        "retornar": "⬅ Back to menu"
    },
    "es": {
        "bemvindo": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrará oportunidades exclusivas en el agronegocio digital.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure su posición en el mercado.*\n\nSeleccione una opción abajo 👇",
        "botoes": [
            ("✅ Cómo comprar", "comprar"),
            ("📄 Abrir formulario", "formulario"),
            ("💰 Ingresar el monto que desea invertir", "investir"),
            ("📊 Acceder al panel", "painel"),
            ("🔗 Ver contrato en BscScan", "bscscan"),
            ("🌍 Cambiar idioma", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *¡3 PASOS PARA OBTENER TUS TOKENS!*\n\n✅ Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ Recibe tus tokens tras la preventa.\n\n⏳ *¡Solo 48h y 500 plazas!*",
        "retornar": "⬅ Volver al menú"
    }
}

# ==================== MENU DE IDIOMA ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ==================== MOSTRAR MENU PRINCIPAL ====================
async def mostrar_menu(query_or_update, idioma, edit=False):
    msg = mensagens[idioma]["bemvindo"]
    botoes = mensagens[idioma]["botoes"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await query_or_update.edit_message_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query_or_update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== ESCOLHER IDIOMA ====================
async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = query.data.split("_")[1]
    context.user_data["idioma"] = idioma
    registrar_acao(query.from_user, idioma, "Escolheu idioma")
    await mostrar_menu(query, idioma, edit=True)

# ==================== CALLBACK DOS BOTÕES ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")

    if query.data == "formulario":
        await query.edit_message_text(f"📄 *Form link:* {GOOGLE_FORMS_URL}\n\n{mensagens[idioma]['retornar']}",
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]['retornar'], callback_data="retornar")]]))

    elif query.data == "painel":
        await query.edit_message_text(f"📊 *Access full control panel here:* {PAINEL_URL}",
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]['retornar'], callback_data="retornar")]]))

    elif query.data == "bscscan":
        await query.edit_message_text(f"🔗 *View verified contract on BscScan:*\n{BSCSCAN_URL}",
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]['retornar'], callback_data="retornar")]]))

    elif query.data == "investir":
        frases = {
            "pt": "💵 *Digite o valor que pretende investir (mínimo 1.000 USD e máximo 5.000 USD) e clique em ENVIAR PROPOSTA*",
            "en": "💵 *Enter the amount you want to invest (min 1,000 USD - max 5,000 USD) and click SEND PROPOSAL*",
            "es": "💵 *Ingrese el monto que desea invertir (mínimo 1.000 USD - máximo 5.000 USD) y haga clic en ENVIAR PROPUESTA*"
        }
        await query.edit_message_text(frases.get(idioma, frases["en"]), parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Enviar Proposta / Send Proposal", callback_data="retornar")]]))
        context.user_data['esperando_valor'] = True

    elif query.data == "comprar":
        texto_comprar = mensagens.get(idioma, mensagens["en"])["como_comprar"]
        await query.edit_message_text(texto_comprar, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]['retornar'], callback_data="retornar")]]))

    elif query.data == "voltar_idioma":
        await start(update, context)

    elif query.data == "retornar":
        await mostrar_menu(query, idioma, edit=True)

# ==================== REGISTRAR INVESTIMENTO ====================
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Informou Valor", valor)
        await update.message.reply_text(f"✅ *Investment of {valor} USD recorded successfully!*",
                                        parse_mode="Markdown")
        context.user_data['esperando_valor'] = False

# ==================== MAIN ====================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT MULTILÍNGUE ONLINE e com painel + BscScan!")
    app.run_polling()

if __name__ == "__main__":
    main()
