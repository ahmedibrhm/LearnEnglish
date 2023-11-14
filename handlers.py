from concurrent.futures import ThreadPoolExecutor
from audio_generation import convert_segments_to_audio
from open_ai_utils import get_openai_response, convert_audio_text, convert_text_audio
from telegram_utils import download_audio_from_telegram
from telegram.ext import CallbackContext
from bot import bot
from telegram import Update
import os

# Executor for handling tasks in the background
executor = ThreadPoolExecutor(max_workers=10)

SYSTEM_PROMPT = "You are a teacher talking to a student. The student is having trouble understanding a concept. Help them understand the concept. You are teaching Arabic. The student is speaking English."

INITIAL_MESSAGE = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

user_conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')

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

        previous_conversation = user_conversations.get(user_id, INITIAL_MESSAGE)
        message_with_context = previous_conversation + [
            {
                "role": "user",
                "content": user_message
            }
        ]
        response = get_openai_response(message_with_context)
        message_with_context.append({
            "role": "assistant",
            "content": response
        })
        audio_file = convert_text_audio(response)
        bot.send_voice(chat_id=user_id, voice=open(audio_file, 'rb'))
        os.remove(audio_file)
        user_conversations[user_id] = message_with_context
        trim_conversation_history(user_id)

    # Submit the message processing to the thread pool
    executor.submit(process_message, update, context)

def trim_conversation_history(user_id):
    """
    Trims the user's conversation history to keep it within limits.
    """
    conversation = user_conversations[user_id]
    while len(combine_text_by_role(conversation)) > 4000:
        conversation = [conversation[0]] + conversation[2:]
    user_conversations[user_id] = conversation

def combine_text_by_role(conversation):
    combined_text = ""
    for message in conversation:
        if message["role"] == "system":
            combined_text += f"\n\nSystem: {message['content']}"
        elif message["role"] == "user":
            combined_text += f"\n\nUser: {message['content']}"
        elif message["role"] == "assistant":
            combined_text += f"\n\nAssistant: {message['content']}"
    return combined_text.strip()
