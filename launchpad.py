from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode

import logging
import requests
import json

from creds import token as bot_token

class Launch():
    def __init__(self, mission_name, provider, vehicle, padname, padloc, description, launch_date):
        self.mission_name = mission_name
        self.provider = provider
        self.vehicle = vehicle
        self.padname = padname
        self.padloc = padloc
        self.description = description
        self.launch_date = launch_date
        self.text = self.createDisplayText()

    def createDisplayText(self):
        text = '**Mission:** ' + self.mission_name + '\n' \
                '**Provider:** ' + self.provider + '\n' \
                '**Vehicle:** ' + self.vehicle + '\n' \
                '**Launching from** ' + self.padname + '(' + self.padloc + ')\n' \
                '**Date:** ' + self.launch_date + '\n\n' \
                '' + self.description
        return text
    
    def getFormattedText(self):
        return self.text

#Start command
def start(update, context):
    welcome_text = '**Welcome to the Launchpad Bot**'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=welcome_text, 
                            parse_mode=ParseMode.MARKDOWN_V2)

def launches(update, context):
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 5
    api_json = json.loads(j.text)['result']
    print(api_json)
    txts = []
    for i in range(0, n_results):
        l = Launch(
            str(api_json[i]['name']),
            str(api_json[i]['provider']['name']),
            str(api_json[i]['vehicle']['name']),
            str(api_json[i]['pad']['location']['name']),
            str(api_json[i]['pad']['location']['statename']) + str(api_json[i]['pad']['location']['country']),
            str(api_json[i]['launch_description']),
            str(api_json[i]['win_open'])
        )
        txts.append(l.getFormattedText())
    
    endtext = ""
    for i in range(0, len(txts)):
        endtext = endtext + txts[i] + '\n===========\n'
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=endtext, 
                            parse_mode=ParseMode.MARKDOWN_V2)

def main():
    print("Launchpad Bot started!\n")
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Setup the logging part of the bot
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    nextFive_handler = CommandHandler('launches', launches)
    dispatcher.add_handler(nextFive_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    