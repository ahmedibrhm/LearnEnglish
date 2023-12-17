from openai import OpenAI
client = OpenAI()

def convert_audio_text(audio_path, language='', prompt=''):
    # use OPENAI API to convert audio to text
    file = open(audio_path, "rb")
    print('file', file)
    transcript = client.audio.transcriptions.create(model="whisper-1", file=file, response_format="text", language=language, prompt=prompt)
    return transcript