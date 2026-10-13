import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8842104179:AAEmtUu47NgudEivhiLWj-Gng5ZKXFvsyS0"
IL_TUO_CANALE_LINK = "https://t.me/+oA8lp-NvSxsxYTk0"

MESSAGGIO_BENVENUTO = (
    "👋 **Benvenuto nel gruppo!**\n\n"
    "📌 Per accedere ai servizi e aprire il tuo conto PAM, "
    "unisciti al canale ufficiale o usa il pulsante qui sotto.\n"
    "⚠️ *Regole del gruppo:* No spam, no link esterni, no insulti."
)

PAROLE_VIETATE = [
    "cazzo", "merda", "stronzo", "vaffanculo", "puttana",
    "guadagno facile", "crypto bonus", "investimento sicuro"
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Unisciti al Canale Ufficiale", url=IL_TUO_CANALE_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Ciao! Clicca sul pulsante qui sotto per accedere:", reply_markup=reply_markup)

async def benvenuto_nuovo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        keyboard = [[InlineKeyboardButton("📢 Entra nel Canale Ufficiale", url=IL_TUO_CANALE_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Ciao {member.first_name}!\n\n{MESSAGGIO_BENVENUTO}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def modera_messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    testo = update.message.text.lower()
    if any(parola in testo for parola in PAROLE_VIETATE):
        try:
            await update.message.delete()
            awarded = await update.message.reply_text(
                f"⚠️ {update.message.from_user.first_name}, il tuo messaggio è stato rimosso perché conteneva linguaggio o contenuti non consentiti."
            )
        except Exception as e:
            logging.error(f"Errore durante l'eliminazione: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, benvenuto_nuovo_membro))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, modera_messaggi))
    print("Bot avviato in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
