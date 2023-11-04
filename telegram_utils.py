import os
from bot import bot

def download_audio_from_telegram(file_id):
    """
    Downloads an audio file from Telegram based on its file ID.
    Returns the local file path of the downloaded audio.
    """
    file_info = bot.get_file(file_id)
    file_path = os.path.join("/tmp", file_id + ".oga")  # Save as .oga (Opus codec used by Telegram for voice messages)
    file_info.download(file_path)
    return file_path