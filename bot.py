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
BOT_TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo token correto
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"
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

# ==================== MENSAGENS POR IDIOMA ====================
mensagens = {
    "en": {
        "menu": "🌍 *Welcome to AgroDigital Club!*\n\n🚀 Exclusive opportunities in digital agribusiness with global growth potential.\n\n💡 *Join the pre-sale of SoByen (SBN) and secure your position.*\n\nChoose an option below 👇",
        "buttons": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter the amount you want to invest", "investir"),
            ("📊 Access panel", "painel"),
            ("✅ View token contract", "contrato")
        ],
        "back": "⬅️ Return",
        "lang_menu": "🌍 *Choose your language:*",
        "como_comprar": f"🔥 *3 QUICK STEPS TO GET YOUR SBN TOKENS!*\n\n✅ Send **BNB (BSC Network)** to:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Fill the whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receive tokens after pre-sale.",
        "contrato_msg": f"✅ *Verified on BscScan for your security:*\n{BSCSCAN_URL}",
        "painel_msg": f"📊 Access the full control panel here:\n{PAINEL_URL}",
        "form_msg": f"📄 The form will open in English for global standardization:\n{GOOGLE_FORMS_URL}",
        "invest_msg": "💵 *Enter the amount you want to invest (min 1,000 USD, max 5,000 USD)* and click ✅ Send Proposal."
    },
    "pt": {
        "menu": "🌱 *Bem-vindo(a) ao AgroDigital Club!*\n\n🚀 Oportunidades exclusivas no agronegócio digital com potencial global.\n\n💡 *Participe da pré-venda do token SoByen (SBN).*",
        "buttons": [
            ("✅ Como comprar", "comprar"),
            ("📄 Abrir formulário whitelist", "formulario"),
            ("💰 Informar valor que deseja investir", "investir"),
            ("📊 Acessar painel", "painel"),
            ("✅ Ver contrato do token", "contrato")
        ],
        "back": "⬅️ Voltar",
        "lang_menu": "🌍 *Escolha seu idioma:*",
        "como_comprar": f"🔥 *3 PASSOS PARA GARANTIR SEUS TOKENS SBN!*\n\n✅ Envie **BNB (Rede BSC)** para:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Preencha a whitelist:\n{GOOGLE_FORMS_URL}\n✅ Receba os tokens após a pré-venda.",
        "contrato_msg": f"✅ *Contrato verificado na BscScan para sua segurança:*\n{BSCSCAN_URL}",
        "painel_msg": f"📊 Acesse o painel completo de controle aqui:\n{PAINEL_URL}",
        "form_msg": f"📄 O formulário abrirá padronizado em inglês:\n{GOOGLE_FORMS_URL}",
        "invest_msg": "💵 *Digite o valor que pretende investir (mínimo 1.000 USD e máximo 5.000 USD)* e clique ✅ Enviar Proposta."
    },
    "es": {
        "menu": "🌾 *¡Bienvenido(a) a AgroDigital Club!*\n\n🚀 Oportunidades exclusivas en el agronegocio digital con potencial global.\n\n💡 *Participa en la preventa del token SoByen (SBN).*",
        "buttons": [
            ("✅ Cómo comprar", "comprar"),
            ("📄 Abrir formulario whitelist", "formulario"),
            ("💰 Ingresar el monto que desea invertir", "investir"),
            ("📊 Acceder al panel", "painel"),
            ("✅ Ver contrato del token", "contrato")
        ],
        "back": "⬅️ Volver",
        "lang_menu": "🌍 *Elige tu idioma:*",
        "como_comprar": f"🔥 *¡3 PASOS RÁPIDOS PARA OBTENER TUS TOKENS SBN!*\n\n✅ Envía **BNB (Red BSC)** a:\n`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n✅ Completa la whitelist:\n{GOOGLE_FORMS_URL}\n✅ Recibe los tokens al finalizar la preventa.",
        "contrato_msg": f"✅ *Contrato verificado en BscScan para su seguridad:*\n{BSCSCAN_URL}",
        "painel_msg": f"📊 Accede al panel de control completo aquí:\n{PAINEL_URL}",
        "form_msg": f"📄 El formulario se abrirá estandarizado en inglés:\n{GOOGLE_FORMS_URL}",
        "invest_msg": "💵 *Ingrese el monto que desea invertir (mínimo 1.000 USD y máximo 5.000 USD)* y haga clic en ✅ Enviar Propuesta."
    }
}

# ==================== FLUXO PRINCIPAL ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    await update.message.reply_text("🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
                                    parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def mostrar_menu(query, idioma):
    msg = mensagens[idioma]["menu"]
    botoes = mensagens[idioma]["buttons"] + [(mensagens[idioma]["back"], "retornar_lang")]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idioma = query.data.split("_")[1]
    context.user_data["idioma"] = idioma
    await mostrar_menu(query, idioma)

# ==================== CALLBACK BOTÕES ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idioma = context.user_data.get("idioma", "en")
    await query.answer()

    if query.data == "comprar":
        await query.edit_message_text(mensagens[idioma]["como_comprar"], parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]["back"], callback_data="retornar")]]))

    elif query.data == "formulario":
        await query.edit_message_text(mensagens[idioma]["form_msg"], parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]["back"], callback_data="retornar")]]))

    elif query.data == "investir":
        await query.edit_message_text(mensagens[idioma]["invest_msg"], parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Send Proposal / Enviar Proposta", callback_data="esperando_valor")],
                                                                         [InlineKeyboardButton(mensagens[idioma]["back"], callback_data="retornar")]]))

    elif query.data == "painel":
        await query.edit_message_text(mensagens[idioma]["painel_msg"], parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]["back"], callback_data="retornar")]]))

    elif query.data == "contrato":
        await query.edit_message_text(mensagens[idioma]["contrato_msg"], parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(mensagens[idioma]["back"], callback_data="retornar")]]))

    elif query.data == "retornar":
        await mostrar_menu(query, idioma)

    elif query.data == "retornar_lang":
        await start(update, context)

# ==================== MAIN ====================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ BOT atualizado online!")
    app.run_polling()

if __name__ == "__main__":
    main()
