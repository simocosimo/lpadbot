from telegram.ext import Updater
import logging

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher

# Setup the logging part of the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Start commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Testttt")

if __name__ == '__main__':
    # Start polling for commands
    updater.start_polling()
    updater.idle()