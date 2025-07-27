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
BOT_TOKEN = "SEU_TOKEN_AQUI"  # 🚨 Substitua pelo token correto
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuHfXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital-panel-git-main-isr-stls-projects.vercel.app/"
BSCSCAN_URL = "https://bscscan.com/address/0x9ea22b56062f5a8e870ffded967987a5a5edf8d8#code"

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
    "pt": {
        "bemvindo": "🌱 *Bem-vindo(a) ao AgroDigital Club!*\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial global.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\nEscolha uma opção abaixo 👇",
        "botoes": [
            ("🌍 Como comprar", "comprar"),
            ("📄 Abrir formulário da whitelist", "formulario"),
            ("💰 Informar valor que deseja investir", "investir"),
            ("📊 Acessar painel", "painel"),
            ("🔗 Ver contrato no BscScan", "bscscan"),
            ("🌍 Trocar idioma", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *3 PASSOS RÁPIDOS PARA GARANTIR SEUS TOKENS!*\n\n✅ 1. Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Receba seus tokens ao final da pré-venda.\n\n⏳ *Apenas 48h e 500 vagas!*",
        "painel": f"📊 *Acesse o painel completo de controle:*\n{PAINEL_URL}",
        "bscscan": f"🔗 *Contrato verificado no BscScan:*\n{BSCSCAN_URL}",
        "investir_texto": "💵 *Digite o valor que pretende investir (mínimo 1.000 USD e máximo 5.000 USD)*\nExemplo: 1500"
    },
    "en": {
        "bemvindo": "🌍 *Welcome to AgroDigital Club!*\n\n🚀 Here you will find exclusive digital agribusiness opportunities with global growth potential.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your strategic market position.*\n\nChoose an option below 👇",
        "botoes": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter the amount you want to invest", "investir"),
            ("📊 Access panel", "painel"),
            ("🔗 View contract on BscScan", "bscscan"),
            ("🌍 Change language", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *3 QUICK STEPS TO GET YOUR TOKENS!*\n\n✅ 1. Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Fill the whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Tokens will be delivered after the pre-sale ends.\n\n⏳ *Only 48h and 500 spots available!*",
        "painel": f"📊 *Access the full control panel:*\n{PAINEL_URL}",
        "bscscan": f"🔗 *Verified contract on BscScan:*\n{BSCSCAN_URL}",
        "investir_texto": "💵 *Enter the amount you want to invest (min 1,000 USD and max 5,000 USD)*\nExample: 1500"
    },
    "es": {
        "bemvindo": "🌾 *¡Bienvenido(a) a AgroDigital Club!*\n\n🚀 Aquí encontrará oportunidades exclusivas en el agronegocio digital con potencial de crecimiento global.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure su posición estratégica en el mercado.*\n\nSeleccione una opción abajo 👇",
        "botoes": [
            ("🌍 Cómo comprar", "comprar"),
            ("📄 Abrir formulario de whitelist", "formulario"),
            ("💰 Ingresar el monto que desea invertir", "investir"),
            ("📊 Acceder al panel", "painel"),
            ("🔗 Ver contrato en BscScan", "bscscan"),
            ("🌍 Cambiar idioma", "voltar_idioma")
        ],
        "como_comprar": f"🔥 *¡3 PASOS RÁPIDOS PARA OBTENER TUS TOKENS!*\n\n✅ 1. Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Recibirás tus tokens al finalizar la preventa.\n\n⏳ *¡Solo 48h y 500 plazas disponibles!*",
        "painel": f"📊 *Accede al panel completo de control:*\n{PAINEL_URL}",
        "bscscan": f"🔗 *Contrato verificado en BscScan:*\n{BSCSCAN_URL}",
        "investir_texto": "💵 *Ingrese el monto que desea invertir (mínimo 1.000 USD y máximo 5.000 USD)*\nEjemplo: 1500"
    }
}

# ==================== START - ESCOLHA IDIOMA ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(
            "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await update.callback_query.edit_message_text(
            "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# ==================== APÓS ESCOLHER IDIOMA ========================
async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = query.data.split("_")[1]  # en, pt, es
    context.user_data["idioma"] = idioma
    await mostrar_menu(query, idioma)

# ==================== MENU PRINCIPAL ==============================
async def mostrar_menu(query_or_update, idioma, edit=False):
    msg = mensagens[idioma]["bemvindo"]
    botoes = mensagens[idioma]["botoes"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(query_or_update, Update):
        await query_or_update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        if edit:
            await query_or_update.edit_message_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await query_or_update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== BOTÕES PRINCIPAIS ===========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")  # Default inglês

    if query.data == "formulario":
        registrar_acao(query.from_user, idioma, "Abriu Formulário")
        await query.edit_message_text(f"📄 *Preencha a whitelist aqui:*\n{GOOGLE_FORMS_URL}", parse_mode="Markdown")
        await query.message.reply_text("↩️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="retornar")]]))

    elif query.data == "investir":
        texto_investir = mensagens[idioma]["investir_texto"]
        await query.edit_message_text(texto_investir, parse_mode="Markdown")
        context.user_data['esperando_valor'] = True

    elif query.data == "comprar":
        registrar_acao(query.from_user, idioma, "Clicou Como Comprar")
        texto_comprar = mensagens[idioma]["como_comprar"]
        await query.edit_message_text(texto_comprar, parse_mode="Markdown")
        await query.message.reply_text("↩️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="retornar")]]))

    elif query.data == "painel":
        await query.edit_message_text(mensagens[idioma]["painel"], parse_mode="Markdown")
        await query.message.reply_text("↩️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="retornar")]]))

    elif query.data == "bscscan":
        await query.edit_message_text(mensagens[idioma]["bscscan"], parse_mode="Markdown")
        await query.message.reply_text("↩️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="retornar")]]))

    elif query.data == "retornar":
        await mostrar_menu(query, idioma, edit=True)

    elif query.data == "voltar_idioma":
        if "idioma" in context.user_data:
            del context.user_data["idioma"]
        await start(update, context)

# ==================== REGISTRAR VALOR INVESTIDO ===================
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Informou Valor", valor)
        await update.message.reply_text(f"✅ Investment of {valor} USD recorded successfully!")
        context.user_data['esperando_valor'] = False

# ==================== MAIN APP ====================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT MULTILÍNGUE ONLINE e registrando interações na planilha!")
    app.run_polling()

if __name__ == "__main__":
    main()
