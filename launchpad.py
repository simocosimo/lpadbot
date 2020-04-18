from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler

import logging
import requests
import json

from creds import token as bot_token

class Launch():
    def __init__(self, mission_name, provider, vehicle, padname, padloc, description, launch_date) {
        self.mission_name = mission_name
        self.provider = provider
        self.vehicle = vehicle
        self.padname = padname
        self.padloc = padloc
        self.description = description
        self.launch_date = launch_date
        self.text = createDisplayText()
    }

    def createDisplayText():
        text = '**Mission:** ' + self.mission_name + '\n' \
                '**Provider:** ' + self.provider + '\n' \
                '**Vehicle:** ' + self.vehicle + '\n' \
                '**Launching from** ' + self.padname + '(' + self.padloc + ')\n' \
                '**Date:** ' + self.launch_date + '\n\n' \
                '' + self.description
        return text
    
    def getFormattedText():
        return self.text

#Start command
def start(update, context):
    welcome_text = '###Welcome to the Launchpad Bot!'
    context.bot.send_message(chat_id=chat_id, text=welcome_text)

def getUpcomingLaunches(update, context):
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 5
    api_json = json.loads(j)['result']
    txts = []
    for i in range(0, n_results):
        l = new Launch(
            api_json[i]['name'],
            api_json[i]['provider']['name'],
            api_json[i]['vehicle']['name'],
            api_json[i]['pad']['location']['name'],
            api_json[i]['pad']['location']['statename'] + api_json[i]['pad']['location']['country'],
            api_json[i]['launch_description'],
            api_json[i]['win_open']
        )
        txts.append(l.getFormattedText())
    
    endtext = ""
    for i in range(0, len(txts)):
        endtext = endtext + txts[i] + '\n-----------\n'
    
    context.bot.send_message(chat_id=chat_id, 
                            text=endtext, 
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def main():
    print("Launchpad Bot started!\n")
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    chat_id = updater.message.chat_id

    # Setup the logging part of the bot
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    nextFive_handler = CommandHandler('upcoming', getUpcomingLaunches)
    dispatcher.add_error_handler(nextFive_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    