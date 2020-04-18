from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode

import logging
import requests
import json

from creds import token as bot_token

class Launch():
    gmpas_baseurl = "https://www.google.com/maps/search/?api=1&query="

    def __init__(self, mission_name, provider, vehicle, padname, padloc, description, launch_date):
        self.mission_name = mission_name
        self.provider = provider
        self.vehicle = vehicle
        self.padname = padname
        self.padloc = padloc
        self.description = description
        self.text = self.createDisplayText()
        self.launch_date = "TBD"

        if launch_date is not "None":
            parts = launch_date.split('T')
            day = parts[0].split('-')
            self.launch_date = day[1] + '-' + day[2] + '-' + day[0] + ' ' + parts[1][0:-1] + '(UTC)'

    def createDisplayText(self):
        print(self.launch_date)
        gmaps_querykey = self.padname.replace(' ', '+')
        text = '<b>Mission:</b> ' + self.mission_name + '\n' \
                '<b>Provider:</b> ' + self.provider + '\n' \
                '<b>Vehicle:</b> ' + self.vehicle + '\n' \
                '<b>Launching from</b> <a href="' + self.gmpas_baseurl + gmaps_querykey + '">' + self.padname + ' (' + self.padloc + ')</a>\n' \
                '<b>Date:</b> <i>' + self.launch_date + '</i>\n\n' \
                '' + self.description
        return text
    
    def getFormattedText(self):
        return self.text

#Start command
def start(update, context):
    welcome_text = '<b>Welcome to the Launchpad Bot</b>\n'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=welcome_text, 
                            parse_mode=ParseMode.HTML)

def launches(update, context):
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 5
    api_json = json.loads(j.text)['result']
    padlocation = ""
    txts = []
    for i in range(0, n_results):
        if str(api_json[i]['pad']['location']['statename']) is "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        else:
            str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country']),

        l = Launch(
            str(api_json[i]['name']),
            str(api_json[i]['provider']['name']),
            str(api_json[i]['vehicle']['name']),
            str(api_json[i]['pad']['location']['name']),
            padlocation,
            str(api_json[i]['launch_description']),
            str(api_json[i]['win_open'])
        )
        txts.append(l.getFormattedText())
    
    endtext = ""
    for i in range(0, len(txts)):
        endtext = endtext + txts[i] + '\n===========\n'
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=endtext, 
                            parse_mode=ParseMode.HTML)

def next(update, context):
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 1
    api_json = json.loads(j.text)['result']
    padlocation = ""
    txts = []
    for i in range(0, n_results):
        if str(api_json[i]['pad']['location']['statename']) is "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        else:
            str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country']),

        l = Launch(
            str(api_json[i]['name']),
            str(api_json[i]['provider']['name']),
            str(api_json[i]['vehicle']['name']),
            str(api_json[i]['pad']['location']['name']),
            padlocation,
            str(api_json[i]['launch_description']),
            str(api_json[i]['win_open'])
        )
        txts.append(l.getFormattedText())
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=txts[0], 
                            parse_mode=ParseMode.HTML)

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

    nextOne_handler = CommandHandler('next', launches)
    dispatcher.add_handler(nextOne_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    