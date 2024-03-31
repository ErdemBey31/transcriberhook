from flask import Flask, request
import assemblyai as aai
import os
import requests

app = Flask(__name__)

aai.settings.api_key = "059b26e05fda420a9612d5aeb4bad83f"
config = aai.TranscriptionConfig(language_code="tr")
transcriber = aai.Transcriber(config=config)

bot_token = "6765509934:AAGIpSWslGRGlLlvWgjHg3q02f3QOnYdOFI"
YOUR_BOT_TOKEN = bot_token

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message')
    if message and 'text' in message:
        text = message['text']
        if text == '/start':
            send_start_message(message)
    elif message and 'voice' in message:
        voice_message = message['voice']
        file_id = voice_message['file_id']
        file_path = download_file(file_id)
        transcribe_audio(file_path)
        remove_file(file_path)
    return 'Webhook received successfully'

def send_start_message(message):
    chat_id = message['chat']['id']
    start_message = """
    👋 Merhaba! Transcriber Bot'a hoşgeldin.

    📝 Bu bot, grubunuzda gönderdiğiniz sesli mesajları metin haline çevirir.

    Sesli mesaj göndermek için sadece bir ses kaydediciye tıklayın ve sesli mesajı gönderin.

    Başlamak için /start komutunu kullanabilirsiniz.
    """
    send_message(chat_id, start_message)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Failed to send message. Error: {response.text}")

def download_file(file_id):
    
    file_url = f"https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(file_url)
    if response.status_code == 200:
        file_data = response.json()
        file_path = file_data.get('result', {}).get('file_path')
        if file_path:
            file_url = f"https://api.telegram.org/file/bot{YOUR_BOT_TOKEN}/{file_path}"
            response = requests.get(file_url)
            if response.status_code == 200:
                os.listdir(file_path)
                with open(file_path, 'w+') as file:
                    file.write(response.content)
    return file_path

def transcribe_audio(file_path):
    trans = transcriber.transcribe(file_path)
    # Process the transcription result as per your requirements.
    # You can send it as a response or take any other action.
    print(trans.text)

def remove_file(file_path):
    os.remove(file_path)
