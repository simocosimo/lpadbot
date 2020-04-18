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
                            disable_web_page_preview=True,
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
    
    providers_list = ["spacex", "ula", "nasa", "roscosmos", "jaxa", "china"]
    selected = ""
    for i in range(0, len(providers_list)):
        if providers_list[i] in str(api_json[i]['provider']['name']).lower():
            selected = i + '.jpg'
            break

    context.bot.send_photo(chat_id=update.effective_chat.id, 
                            photo=open('imgs/' + selected, 'rb'),
                            caption=txts[0], 
                            parse_mode=ParseMode.HTML)

def info(update, context):
    text = "<b>Launchpad Bot</b> for Telegram by @simocosimo\n" \
            "I really hope you like the bot. It is a work in progress, I want to improve" \
            " it as much as possible, in style and in informations. Bare in mind that " \
            " space launches are usually subjected to change in schedule, so take the dates" \
            " with a grain of salt. \nIf you want to make a little donation to help the " \
            "project, <a href='https://www.paypal.me/simocosimo'>you can do it!</a> You absolutely don't have to, but they are really " \
            "appreciated <3"
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=text, 
                            parse_mode=ParseMode.HTML)

def helpCommand(update, context):
    helptext = "<b>/start</b> - Welcomes you\n" \
                "<b>/launches</b> - Shows the upcoming 5 launches\n" \
                "<b>/next</b> - Shows the next upcming launch\n" \
                "<b>/info</b> - Shows infos about the bot\n" \
                "<b>/help</b> - Shows this help screen\n"
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=helptext, 
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

    #nextOne_handler = CommandHandler('next', nextLaunch)
    #dispatcher.add_handler(nextOne_handler)

    nextPic_handler = CommandHandler('next', nextLaunch)
    dispatcher.add_handler(nextPic_handler)

    info_handler = CommandHandler('info', info)
    dispatcher.add_handler(info_handler)

    help_handler = CommandHandler('help', helpCommand)
    dispatcher.add_handler(help_handler)

    # Start polling for commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    