import datetime
import os  # Para pegar o token do Railway
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
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Lê automaticamente do Railway
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"
PAINEL_URL = "https://agrodigital-panel-git-main-isr-stls-projects.vercel.app/"

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
        "bemvindo": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial de crescimento global.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\nEscolha uma opção abaixo 👇",
        "botoes": [
            ("✅ Como comprar", "comprar"),
            ("📄 Abrir formulário", "formulario"),
            ("💰 Informar valor que deseja investir", "investir"),
            ("⬅️ Retornar", "retornar")
        ],
        "como_comprar": f"🔥 *3 PASSOS RÁPIDOS PARA GARANTIR SEUS TOKENS SBN!*\n\n✅ 1. Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Preencha a whitelist:\n[📄 Clique aqui para abrir o formulário]({GOOGLE_FORMS_URL})\n\n✅ 3. Receba seus tokens automaticamente após o fim da pré-venda.\n\n⏳ *Só 48h e apenas 500 vagas disponíveis!*"
    },
    "en": {
        "bemvindo": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive opportunities in digital agribusiness with global growth potential.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your strategic position in the market.*\n\nChoose an option below 👇",
        "botoes": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter the amount you want to invest", "investir"),
            ("⬅️ Back", "retornar")
        ],
        "como_comprar": f"🔥 *3 QUICK STEPS TO GET YOUR SBN TOKENS!*\n\n✅ 1. Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Fill the whitelist:\n[📄 Open Whitelist Form]({GOOGLE_FORMS_URL})\n\n✅ 3. Tokens will be delivered automatically after pre-sale ends.\n\n⏳ *Only 48h and 500 spots available!*"
    },
    "es": {
        "bemvindo": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrará oportunidades exclusivas en el agronegocio digital con potencial de crecimiento global.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure una posición estratégica en el mercado.*\n\nSeleccione una opción abajo 👇",
        "botoes": [
            ("✅ Cómo comprar", "comprar"),
            ("📄 Abrir formulario", "formulario"),
            ("💰 Ingresar el monto que desea invertir", "investir"),
            ("⬅️ Regresar", "retornar")
        ],
        "como_comprar": f"🔥 *¡3 PASOS RÁPIDOS PARA OBTENER TUS TOKENS SBN!*\n\n✅ 1. Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n✅ 2. Completa la whitelist:\n[📄 Abrir formulario]({GOOGLE_FORMS_URL})\n\n✅ 3. Recibe tus tokens automáticamente al finalizar la preventa.\n\n⏳ *¡Solo 48h y 500 plazas disponibles!*"
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

# ==================== MENU POR IDIOMA ============================
async def mostrar_menu(query, idioma, edit=False):
    msg = mensagens[idioma]["bemvindo"]
    botoes = mensagens[idioma]["botoes"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== ESCOLHER IDIOMA ===========================
async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = query.data.split("_")[1]  # en, pt, es
    context.user_data["idioma"] = idioma
    registrar_acao(query.from_user, idioma, "Escolheu idioma")
    await mostrar_menu(query, idioma, edit=True)

# ==================== BOTÕES PRINCIPAIS =========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")  # Default inglês

    if query.data == "formulario":
        registrar_acao(query.from_user, idioma, "Abriu Formulário")
        await query.edit_message_text(
            f"📄 *The form will open in English for global standardization.*\n\n[📄 Open Whitelist Form]({GOOGLE_FORMS_URL})",
            parse_mode="Markdown"
        )

    elif query.data == "investir":
        frases_investir = {
            "pt": "💵 *Digite o valor que pretende investir (mínimo 1.000 USD e máximo 5.000 USD)*\nExemplo: 1500",
            "en": "💵 *Enter the amount you want to invest (minimum 1,000 USD and maximum 5,000 USD)*\nExample: 1500",
            "es": "💵 *Ingrese el monto que desea invertir (mínimo 1.000 USD y máximo 5.000 USD)*\nEjemplo: 1500"
        }
        texto_investir = frases_investir.get(idioma, frases_investir["en"])
        await query.edit_message_text(texto_investir, parse_mode="Markdown")
        context.user_data['esperando_valor'] = True

    elif query.data == "comprar":
        registrar_acao(query.from_user, idioma, "Clicou Como Comprar")
        texto_comprar = mensagens.get(idioma, mensagens["en"])["como_comprar"]
        await query.edit_message_text(texto_comprar, parse_mode="Markdown")

    elif query.data == "retornar":
        await mostrar_menu(query, idioma, edit=True)

# ==================== REGISTRAR VALOR INVESTIDO =================
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Informou Valor", valor)
        await update.message.reply_text(
            f"✅ Investimento *{valor}* registrado com sucesso!",
            parse_mode="Markdown"
        )
        context.user_data['esperando_valor'] = False
        await mostrar_menu(update, idioma)  # Volta ao menu depois de registrar

# ==================== MAIN APP ==================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT MULTILÍNGUE 2.0 ONLINE e registrando interações na planilha!")
    app.run_polling()

if __name__ == "__main__":
    main()
