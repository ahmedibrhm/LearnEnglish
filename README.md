# README for Arabic Teaching Telegram Bot

## Overview

This Telegram bot is designed to help students who are learning the Arabic language. When interacted with, the bot behaves as a teacher assisting a student who is having difficulty understanding a concept in Arabic. Users can communicate with the bot using either text or voice messages. The bot is capable of converting voice messages into text and then generating a response. It can then send this response back as an audio message.

## Features

- **Text-based communication**: Users can send a text message to the bot, which will then generate an appropriate response.
- **Voice-based communication**: Users can send a voice message, which the bot will transcribe into text and then generate a response. The response will be sent back as an audio message.
- **Contextual Conversations**: The bot maintains a context of the conversation up to a certain word limit, ensuring continuity in the dialogue.

## Setup

1. Ensure you have all the required modules installed:
   ```bash
   pip install telegram
   ```

2. Replace `'YOUR_TELEGRAM_BOT_TOKEN'` in the code with your Telegram bot's API token.

3. Run the bot using the command:
   ```bash
   python filename.py
   ```

## Usage

- Send `/start` to initiate a conversation with the bot.
- To communicate, you can either:
    1. Type your message and send.
    2. Record a voice message and send.
- The bot will respond either with text or an audio message, based on the input method you used.

## Code Structure

- **Imported Modules**: 
  - `telegram`, `telegram.ext`: Used for Telegram bot functionalities.
  - `audio_generation`: Contains the `convert_segments_to_audio` function to convert text segments into an audio file.
  - `response_generation`: Contains functions for generating responses using OpenAI and handling multilingual text.
  - `telegram_utils`: Utility for downloading audio from Telegram.
  - `bot`: Contains the bot instance and API token.

- **Main Functionalities**:
  - `start()`: Sends a greeting message to the user.
  - `echo()`: Echoes back whatever text the user sends.
  - `handle_message()`: Handles incoming messages (both text and voice) and sends back the appropriate response.
  - `combine_text_by_role()`: Combines the conversation into a single string with role-specific formatting.
  - `main()`: The main function that initializes the bot, sets up handlers, and starts the bot's polling mechanism.

## Notes

- The bot uses a predefined system prompt to set the context of the conversation.
- The conversation history with each user is stored up to a certain word limit to maintain context.
- Ensure you have the required credentials and API token before running the bot.

## Future Improvements

- Consider integrating more advanced features like quizzes, flashcards, and other educational tools to enhance the learning experience.
- Add support for other languages.
- Optimize the bot's performance for large-scale deployment.