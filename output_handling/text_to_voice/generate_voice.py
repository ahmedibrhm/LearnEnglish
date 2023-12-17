import uuid
from openai import OpenAI
client = OpenAI()

def convert_text_audio(text):
    # use OPENAI API to convert text to audio
    print('hhh', text)
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    )

    file_name = str(uuid.uuid4()) + ".mp3"
    response.stream_to_file(file_name)
    return file_name