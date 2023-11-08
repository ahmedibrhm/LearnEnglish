from audio_generation import convert_segments_to_audio
from open_ai_utils import get_openai_response, split_text_by_language, combine_text_by_language, convert_audio_text, convert_text_audio
from telegram_utils import download_audio_from_telegram
from telegram.ext import CallbackContext
from bot import bot
from telegram import Update
import os

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Bot's API token
SYSTEM_PROMPT = "You are a teacher talking to a student. The student is having trouble understanding a concept. Help them understand the concept. You are teaching Arabic. The student is speaking English."

INITIAL_MESSAGE = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# Create a dictionary to store previous conversations with each user
user_conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def handle_message(update: Update, context: CallbackContext) -> None:
    print("Message received")
    if update.message.voice:
        # Download the audio
        print("Audio")
        audio_path = download_audio_from_telegram(update.message.voice.file_id)
        print("Audio path:", audio_path)
        # Convert audio to text
        user_message = convert_audio_text(audio_path)
        print("User message:", user_message)
        # Remove the downloaded audio file
        os.remove(audio_path)
    else:
        user_message = update.message.text

    user_id = update.message.chat_id
    print("User message:", user_message)

    # Get the previous conversation with the user from the dictionary
    previous_conversation = user_conversations.get(user_id, INITIAL_MESSAGE)

    # Combine the previous conversation with the current message
    message_with_context = previous_conversation + [
        {
            "role": "user",
            "content": user_message
        }
    ]

    print("Message with context:", message_with_context)
    # Get the response from OpenAI using the message with context
    response = get_openai_response(message_with_context)
    message_with_context.append({
        "role": "assistant",
        "content": response
    })
    print("Response:", response)

    # Convert the message to audio
    audio_file = convert_text_audio(response)
    print("Audio file:", audio_file)

    # Send the audio file to the user
    bot.send_voice(chat_id=user_id, voice=open(audio_file, 'rb'))

    # Remove the audio file
    os.remove(audio_file)

    # Store the current conversation with the user in the dictionary
    user_conversations[user_id] = message_with_context

    # Delete messages from the beginning until total length is 1000 words. Don't delete the first message.
    conversation = user_conversations[user_id]
    while len(combine_text_by_role(conversation)) > 4000:
        conversation = [conversation[0]] + conversation[2:]
    user_conversations[user_id] = conversation


def combine_text_by_role(conversation):
    """
    Combine the conversation into a single string with role-specific formatting
    """
    combined_text = ""
    for message in conversation:
        if message["role"] == "system":
            combined_text += f"\n\nSystem: {message['content']}"
        elif message["role"] == "user":
            combined_text += f"\n\nUser: {message['content']}"
        elif message["role"] == "assistant":
            combined_text += f"\n\nAssistant: {message['content']}"
    return combined_text.strip()