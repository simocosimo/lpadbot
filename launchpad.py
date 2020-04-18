from telegram.ext import Updater, CommandHandler
from creds import token as bot_token
import logging

#Start commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Testttt")

def main():
    print("Launchpad Bot started!\n")
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Setup the logging part of the bot
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    