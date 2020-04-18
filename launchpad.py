from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode

import logging
import requests
import json

from creds import token as bot_token
from launch import Launch

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
    txts = []
    for i in range(0, n_results):
        padlocation = str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country'])
        print(str(api_json[i]['pad']['location']['statename']))
        if str(api_json[i]['pad']['location']['statename']) == "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        print(padlocation)

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

def nextLaunch(update, context):
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 1
    api_json = json.loads(j.text)['result']
    txts = []
    for i in range(0, n_results):
        padlocation = str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country'])
        print(str(api_json[i]['pad']['location']['statename']))
        if str(api_json[i]['pad']['location']['statename']) == "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        print(padlocation)
        
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

    nextOne_handler = CommandHandler('next', nextLaunch)
    dispatcher.add_handler(nextOne_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    