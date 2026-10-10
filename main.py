import time
import requests

# Incolla il tuo token tra le virgolette (UNA SOLA VOLTA)
TOKEN = "8842104179:AAGypJ_Ud_mcE4jMgNvMHyaFuF4yyPtrb_4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    try:
        response = requests.get(URL + "getUpdates", params={"timeout": 100, "offset": offset})
        return response.json()
    except Exception as e:
        print(f"Errore di connessione: {e}")
        return None

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def main():
    print("Bot in ascolto... Premi Stop per fermarlo.")
    last_update_id = None
    
    while True:
        updates = get_updates(last_update_id)
        if updates and "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if text == "/start" and chat_id:
                    send_message(chat_id, "Ciao Grijupiter! Il tuo bot è ufficialmente online e pronto all'uso.")
        
        time.sleep(1)

if __name__ == '__main__':
    main()
