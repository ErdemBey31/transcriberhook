from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
token = "6422272052:AAEBkx3UANSWYelsjFnyP2e2YnEY6Pg7zEk"

@app.route('/bot', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['message']
    chat_id = message['chat']['id']
    text = get_message_text(message)

    if text.startswith('/start'):
        send_message(chat_id, "*Çevirmek için mesaj gönder!!*")
    else:
        translation = translate_text(text)
        send_message(chat_id, f"{translation}")

    return jsonify({'success': True})

def get_message_text(message):
    if 'caption' in message:
        return message['caption']
    elif 'text' in message:
        return message['text']
    else:
        return ''

def translate_text(text):
    response = requests.get(f"""https://codingllama.codingteamapi.workers.dev/?token=CTAPI-038AXEXYbdOjvRotvRCPXWiBvv&question=Merhaba! Çeviri konusunda yardımınıza ihtiyacım var. Auto-dedected bir metni Türkçeye çevirmeniz mümkün mü? Metni aşağıda bulabilirsiniz:

{text}
Çevirinizi bekliyor olacağım. Teşekkür ederim!

""")
    translation = response.json().get('bot')
    return translation

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'markdown'
    }
    requests.post(url, json=params)
