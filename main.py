import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token del bot
TOKEN = "8842104179:AAHqPXP5cECd77diF5Jw84u1qsFDucqQruc"

# Personalizza qui i tuoi dati:
IL_TUO_CANALE_LINK = "https://t.me/TUO_CANALE"  # Metti il link del tuo canale o del tuo ref link PAM
MESSAGGIO_BENVENUTO = (
    "👋 **Benvenuto nel gruppo!**\n\n"
    "📌 Per accedere ai servizi e aprire il tuo conto PAM tramite il nostro ref link, "
    "unisciti al canale ufficiale o usa il pulsante qui sotto.\n\n"
    "⚠️ *Regole del gruppo:* No spam, no link esterni, no linguaggio offensivo."
)

# Lista di parole offensive/spam da bloccare (puoi aggiungerne altre separate da virgola)
PAROLE_VIETATE = [
    "cazzo", "merda", "stronzo", "vaffanculo", "puttana", "bastardo",
    "guadagno facile", "crypto bonus", "investimento sicuro", "dm me", "scam"
]

# Abilita i log
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    keyboard = [
        [InlineKeyboardButton("📢 Unisciti al Canale / Ref Link", url=IL_TUO_CANALE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🚀 **Benvenuto in Great Jupiter!**\n\nClicca sul pulsante qui sotto per accedere:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def benvenuto_nuovo_utente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invia benvenuto ai nuovi membri del gruppo"""
    for member in update.message.new_chat_members:
        keyboard = [
            [InlineKeyboardButton("🔗 Apri Conto PAM / Canale", url=IL_TUO_CANALE_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Ciao {member.mention_html()}!\n\n{MESSAGGIO_BENVENUTO}",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

async def modera_messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Filtra e cancella messaggi con link di spam o parole vietate"""
    if not update.message or not update.message.text:
        return
    
    testo = update.message.text.lower()
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # 1. Blocco Spam di Link esterni (se non inviati dagli admin)
    if "http://" in testo or "https://" in testo or "t.me/" in testo:
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"⚠️ {update.message.from_user.mention_html()}, lo spam di link esterni non è consentito!",
                parse_mode="HTML"
            )
            return
        except Exception as e:
            logging.error(f"Errore eliminazione messaggio: {e}")

    # 2. Blocco parole vietate
    for parola in PAROLE_VIETATE:
        if parola in testo:
            try:
                await update.message.delete()
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🚫 {update.message.from_user.mention_html()}, il tuo messaggio è stato rimosso per linguaggio inappropriato.",
                    parse_mode="HTML"
                )
                return
            except Exception as e:
                logging.error(f"Errore eliminazione messaggio: {e}")

def main():
    """Avvio del bot"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, benvenuto_nuovo_utente))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, modera_messaggi))

    logging.info("Bot in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
