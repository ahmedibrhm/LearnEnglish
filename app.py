from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TELEGRAM_BOT_TOKEN
from handlers import start, handle_message




def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Bot's API token
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command handler and the message handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.voice, handle_message)) # Handle voice messages as well

    # Start the Bot (polling)
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
