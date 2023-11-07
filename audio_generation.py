import requests
import base64
import uuid
from settings import GOOGLE_API_KEY

def get_audio(text, language_code, voice_name, api_key):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + api_key
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    data = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": language_code,
            "name": voice_name
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 1.3
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data['audioContent']

def convert_segments_to_audio(segments):
    audio = ""
    file_name = str(uuid.uuid4()) + ".mp3"
    for segment in segments:
        if segment[0] == 'arabic':
            lang = 'ar-EG'
            voice_name = 'ar-XA-Wavenet-A'
        else:
            lang = 'en-US'
            voice_name = 'en-US-Neural2-C'
        audio += get_audio(segment[1], lang, voice_name, GOOGLE_API_KEY)
    audio_bytes = base64.b64decode(audio)
    with open(file_name, "wb") as file:
        file.write(audio_bytes)
    return file_name
