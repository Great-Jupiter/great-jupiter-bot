import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ChatJoinRequestHandler,
    filters
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Il tuo link referral ufficiale
IL_TUO_LINK_PAMM = "https://clienti.zappix.it/r/greatjupiter"

PAROLE_VIETATE = [
    "cazzo", "merda", "stronzo", "vaffanculo",
    "guadagno facile", "crypto bonus", "investimento sicuro", "guadagni garantiti"
]

DISCLAIMER_TESTO = (
    "\n\n⚠️ *Nota:* Le informazioni condivise hanno scopo informativo e analitico. "
    "Il trading comporta rischi ed è richiesta massima consapevolezza nella gestione del capitale."
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 Registrazione e Apertura Conto PAMM", url=IL_TUO_LINK_PAMM)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Ciao! Clicca sul pulsante qui sotto per accedere alla pagina di registrazione del conto PAMM:{DISCLAIMER_TESTO}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Gestisce L'UNICO benvenuto automatico: quando le persone CHIEDONO di accedere al gruppo privato
async def approva_richiesta_accesso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    if request:
        try:
            # Approva la richiesta d'accesso
            await request.approve()
            logging.info(f"Approvato l'accesso per {request.from_user.first_name}")
            
            keyboard = [
                [InlineKeyboardButton("🔗 Registrazione e Apertura Conto PAMM", url=IL_TUO_LINK_PAMM)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=request.chat.id,
                text=f"👋 **Benvenuto nel gruppo, {request.from_user.first_name}!**\n\n"
                     f"📌 Usa il pulsante in basso per procedere all'apertura del conto PAMM.{DISCLAIMER_TESTO}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Errore durante l'approvazione dell'utente: {e}")

async def modera_messaggio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    testo = update.message.text.lower()
    for parola in PAROLE_VIETATE:
        if parola in testo:
            try:
                await update.message.delete()
                await update.message.chat.send_message(
                    f"⚠️ {update.message.from_user.first_name}, il tuo messaggio è stato rimosso per linguaggio non consentito."
                )
            except Exception as e:
                logging.error(f"Errore durante l'eliminazione del messaggio: {e}")
            break

def main():
    if not TOKEN:
        raise ValueError("ERRORE: La variabile d'ambiente TELEGRAM_TOKEN non è stata trovata!")
    
    app = Application.builder().token(TOKEN).build()
    
    # Handler attivi
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approva_richiesta_accesso)) # Solo per richieste spontanee
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, modera_messaggio))
    
    print("Bot avviato in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
