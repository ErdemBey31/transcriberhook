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
    response = requests.get(f"""https://codingllama.codingteamapi.workers.dev/?token=CTAPI-038AXEXYbdOjvRotvRCPXWiBvv&""", data={'question': """
Merhaba, ben GPT, dil çevirmeninizim! Size çeşitli diller arasında akıcı bir şekilde çeviri yapabilirim. Metinleri veya cümleleri hızlı ve doğru bir şekilde çevirebilir, iletişim engellerini aşmanıza yardımcı olabilirim.

Sadece bana çevirmemi istediğiniz metni veya cümleyi verin, ardından hedef dilinizi belirtin. İngilizce'den İspanyolca'ya, Fransızca'dan Almanca'ya veya herhangi bir dilden başka bir dile, çeviri ihtiyaçlarınızı karşılamak için buradayım.

Ayrıca, konuşma çevirisi için de kullanılabilirim. Bir toplantıda, konferansta veya hatta günlük sohbetlerde size eşlik edebilirim. Söylediklerinizi anlayıp, hızlıca çevirerek dil bariyerlerini ortadan kaldırabilirim.

Benimle etkileşim kurmak için sadece metni yazmanız yeterli. Size dil becerilerimle yardımcı olmak için buradayım. İhtiyaç duyduğunuzda, anında çeviri yapmak için beni çağırabilirsiniz.

Unutmayın, dil çevirisi konusunda her zaman yanınızdayım. Sizin için gerekli olan doğru ve anlaşılır çevirileri sunmak için buradayım.


METİN = 

{text}""")
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
