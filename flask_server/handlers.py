import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from concurrent.futures import ThreadPoolExecutor
from input_logic.generate_response import get_openai_response
from input_handling.audio_to_text.generate_text import convert_audio_text
from input_logic.add_user import add_user
from output_handling.text_to_voice.generate_voice import convert_text_audio
from telegram_utils import download_audio_from_telegram
from telegram.ext import CallbackContext
from bot import bot
from telegram import Update
import os
from db import Session, User, Conversation, Message

# Executor for handling tasks in the background
executor = ThreadPoolExecutor(max_workers=10)

user_conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    # Handler for the /start command
    update.message.reply_text('Hello! I am your bot.')
    # Add user to the database if not exists
    with Session() as session:
        user_id = update.message.chat_id
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=update.message.chat.username)
            session.add(user)
            session.commit()

def handle_message(update: Update, context: CallbackContext) -> None:
    # This function will be run in a separate thread
    def process_message(update, context):
        user_id = update.message.chat_id

        if update.message.voice:
            audio_path = download_audio_from_telegram(update.message.voice.file_id)
            user_message = convert_audio_text(audio_path)
            os.remove(audio_path)
        else:
            user_message = update.message.text
        
        assistant_id, thread_id = add_user()
        response = get_openai_response(user_message, assistant_id, thread_id)
        audio_file = convert_text_audio(response)
        bot.send_voice(chat_id=user_id, voice=open(audio_file, 'rb'))
        os.remove(audio_file)

    # Submit the message processing to the thread pool
    executor.submit(process_message, update, context)
