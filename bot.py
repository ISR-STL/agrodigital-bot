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
BOT_TOKEN = "SEU_TOKEN_AQUI"
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital-panel-git-main-isr-stls-projects.vercel.app/"
SUPORTE_EMAIL = "suport@agrodigital5ponto0.com"

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
        "bemvindo": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial global.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica!*\n\nEscolha uma opção abaixo 👇",
        "botoes": [
            ("✅ Como comprar", "comprar"),
            ("📄 Abrir formulário", "formulario"),
            ("💰 Informar valor para investir", "investir"),
            ("🖥 Abrir Painel AgroDigital", "painel"),
            ("📩 Suporte", "suporte"),
            ("⬅️ Retornar", "retornar")
        ],
        "voltar": "⬅️ Retornar",
        "como_comprar": f"🔥 *3 PASSOS RÁPIDOS PARA GARANTIR SEUS TOKENS SBN!*\n\n✅ 1. Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Receba seus tokens após o fim da pré-venda.\n⏳ *Só 48h e 500 vagas disponíveis!*"
    },
    "en": {
        "bemvindo": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Exclusive digital agribusiness opportunities with global growth potential.\n\n💡 *Join the pre-sale of SoByen (SBN) and secure your position!*\n\nChoose an option below 👇",
        "botoes": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter investment amount", "investir"),
            ("🖥 Open AgroDigital Panel", "painel"),
            ("📩 Support", "suporte"),
            ("⬅️ Return", "retornar")
        ],
        "voltar": "⬅️ Return",
        "como_comprar": f"🔥 *3 QUICK STEPS TO GET YOUR SBN TOKENS!*\n\n✅ 1. Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Fill the whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Receive tokens after pre-sale ends.\n⏳ *Only 48h and 500 spots available!*"
    },
    "es": {
        "bemvindo": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Oportunidades exclusivas en agronegocio digital con potencial global.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure su posición!*\n\nSeleccione una opción abajo 👇",
        "botoes": [
            ("✅ Cómo comprar", "comprar"),
            ("📄 Abrir formulario", "formulario"),
            ("💰 Ingresar monto para invertir", "investir"),
            ("🖥 Abrir Panel AgroDigital", "painel"),
            ("📩 Soporte", "suporte"),
            ("⬅️ Volver", "retornar")
        ],
        "voltar": "⬅️ Volver",
        "como_comprar": f"🔥 *¡3 PASOS RÁPIDOS PARA OBTENER TUS TOKENS SBN!*\n\n✅ 1. Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ 2. Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ 3. Recibe tus tokens después de la preventa.\n⏳ *¡Solo 48h y 500 plazas disponibles!*"
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
    await update.message.reply_text(
        "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ==================== MENU PRINCIPAL ==============================
async def mostrar_menu(update_or_query, idioma):
    botoes = mensagens[idioma]["botoes"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(mensagens[idioma]["bemvindo"], parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update_or_query.edit_message_text(mensagens[idioma]["bemvindo"], parse_mode="Markdown", reply_markup=reply_markup)

# ==================== APÓS ESCOLHER IDIOMA ========================
async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = query.data.split("_")[1]  # en, pt, es
    context.user_data["idioma"] = idioma
    registrar_acao(query.from_user, idioma, "Escolheu idioma")
    await mostrar_menu(query, idioma)

# ==================== BOTÕES PRINCIPAIS ===========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")  # Default inglês

    if query.data == "formulario":
        registrar_acao(query.from_user, idioma, "Abriu Formulário")
        keyboard = [[InlineKeyboardButton(mensagens[idioma]["voltar"], callback_data="retornar")]]
        await query.edit_message_text(f"📄 *The form opens in English for global use.*\n\n{GOOGLE_FORMS_URL}",
                                      parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "investir":
        frases = {
            "pt": "💵 *Digite o valor que pretende investir (mínimo 1.000 USD e máximo 5.000 USD)*\nExemplo: 1500",
            "en": "💵 *Enter the amount you want to invest (minimum 1,000 USD and maximum 5,000 USD)*\nExample: 1500",
            "es": "💵 *Ingrese el monto que desea invertir (mínimo 1.000 USD y máximo 5.000 USD)*\nEjemplo: 1500"
        }
        texto = frases.get(idioma, frases["en"])
        keyboard = [[InlineKeyboardButton(mensagens[idioma]["voltar"], callback_data="retornar")]]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        context.user_data['esperando_valor'] = True
    elif query.data == "comprar":
        registrar_acao(query.from_user, idioma, "Clicou Como Comprar")
        keyboard = [[InlineKeyboardButton(mensagens[idioma]["voltar"], callback_data="retornar")]]
        texto_comprar = mensagens.get(idioma, mensagens["en"])["como_comprar"]
        await query.edit_message_text(texto_comprar, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "painel":
        registrar_acao(query.from_user, idioma, "Abriu Painel")
        keyboard = [[InlineKeyboardButton(mensagens[idioma]["voltar"], callback_data="retornar")]]
        await query.edit_message_text(f"🖥 *Access the AgroDigital Panel here:* \n\n{PAINEL_URL}",
                                      parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "suporte":
        registrar_acao(query.from_user, idioma, "Clicou Suporte")
        keyboard = [[InlineKeyboardButton(mensagens[idioma]["voltar"], callback_data="retornar")]]
        await query.edit_message_text(f"📩 *For support, contact:*\n**{SUPORTE_EMAIL}**",
                                      parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "retornar":
        await mostrar_menu(query, idioma)

# ==================== REGISTRAR VALOR INVESTIDO ===================
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Informou Valor", valor)
        await update.message.reply_text(f"✅ Investimento *{valor}* registrado com sucesso!", parse_mode="Markdown")
        context.user_data['esperando_valor'] = False

# ==================== MAIN APP ====================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT MULTILÍNGUE COM SUPORTE, PAINEL E RETORNAR ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
