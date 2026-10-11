import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Abilita il logging per monitorare eventuali errori
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Il tuo token del bot fornito da BotFather
TOKEN = "8842104179:AAHqPXP5cECd77diF5Jw84u1qsFDucqQruc"

# Il link di benvenuto con il ref link aggiornato
REF_LINK = "https://clienti.zappix.it/r/greatjupiter"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    first_name = user.first_name if user else "utente"
    
    # Messaggio di benvenuto personalizzato
    welcome_message = (
        f"Ciao {first_name}! 👋\n\n"
        "Benvenuto nel bot ufficiale di **Great Jupiter**!\n\n"
        "Per iniziare subito e accedere alla piattaforma, "
        "clicca sul pulsante qui sotto:"
    )
    
    # Pulsante con il link referral
    keyboard = [
        [InlineKeyboardButton("🚀 Accedi a Zappix", url=REF_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    # Permette di leggere il token dalle variabili d'ambiente (per la distribuzione su Render)
    bot_token = os.environ.get("BOT_TOKEN", TOKEN)
    
    application = ApplicationBuilder().token(bot_token).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("Bot avviato e in ascolto...")
    application.run_polling()

if __name__ == '__main__':
    main()
