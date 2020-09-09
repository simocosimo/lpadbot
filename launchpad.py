from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode, ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import logging
import requests
import json
import os

#from creds import token as bot_token
from launch import Launch, rocket

from functools import wraps

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

#Start command
@send_typing_action
def start(update, context):
    pass
    welcome_text = '<b>Welcome to the Launchpad Bot</b>\n'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=welcome_text, 
                            parse_mode=ParseMode.HTML)
    helpCommand(update, context)

@send_typing_action
def launches(update, context):
    pass
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 5
    api_json = json.loads(j.text)['result']
    txts = []
    livestream = ""
    for i in range(0, n_results):
        padlocation = str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country'])
        print(str(api_json[i]['pad']['location']['statename']))
        if str(api_json[i]['pad']['location']['statename']) == "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        print(padlocation)

        launch_date = str(api_json[i]['win_open'])
        if launch_date == "None":
            if str(api_json[i]['est_date']['month']) != "None":
                day = '0'
                month = '0'
                if int(api_json[i]['est_date']['month']) < 10:
                    month = month + str(api_json[i]['est_date']['month'])
                else:
                    month = str(api_json[i]['est_date']['month'])

                if str(api_json[i]['est_date']['day']) != "None":
                    if int(api_json[i]['est_date']['day']) < 10:
                        day = day + str(api_json[i]['est_date']['day'])
                    else:
                        day = str(api_json[i]['est_date']['day'])
                else:
                    day = "??"

                launch_date = month + '-' + day + '-' + str(api_json[i]['est_date']['year'])

        l = Launch(
            str(api_json[i]['name']),
            str(api_json[i]['provider']['name']),
            str(api_json[i]['vehicle']['name']),
            str(api_json[i]['pad']['location']['name']),
            padlocation,
            'nodescforlist',
            launch_date,
            livestream
        )
        txts.append(rocket + ' #' + str(i+1) + ' - <i>' + str(api_json[i]['name']) + '</i> ' + rocket \
                    + '\n' + l.getFormattedText())
    
    endtext = ""
    for i in range(0, len(txts)):
        endtext = endtext + txts[i]
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=endtext, 
                            disable_web_page_preview=True,
                            parse_mode=ParseMode.HTML)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

@send_typing_action
def nextLaunch(update, context):
    pass
    j = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
    n_results = 1
    api_json = json.loads(j.text)['result']
    txts = []
    livestream = ""
    for i in range(0, n_results):
        padlocation = str(api_json[i]['pad']['location']['statename']) + ', ' + str(api_json[i]['pad']['location']['country'])
        print(str(api_json[i]['pad']['location']['statename']))
        if str(api_json[i]['pad']['location']['statename']) == "None":
            padlocation = str(api_json[i]['pad']['location']['country'])
        print(padlocation)

        launch_date = str(api_json[i]['win_open'])
        if launch_date == "None":
            if str(api_json[i]['est_date']['month']) != "None":
                day = '0'
                month = '0'
                if int(api_json[i]['est_date']['month']) < 10:
                    month = month + str(api_json[i]['est_date']['month'])
                else:
                    month = str(api_json[i]['est_date']['month'])

                if str(api_json[i]['est_date']['day']) != "None":
                    if int(api_json[i]['est_date']['day']) < 10:
                        day = day + str(api_json[i]['est_date']['day'])
                    else:
                        day = str(api_json[i]['est_date']['day'])
                else:
                    day = "??"

                launch_date = month + '-' + day + '-' + str(api_json[i]['est_date']['year'])

        if str(api_json[i]['quicktext']) != "None":
            parts = str(api_json[i]['quicktext']).split('- ')
            for x in parts:
                if "https" in x:
                    livestream = x

        print("Livestream link: " + livestream)
        l = Launch(
            str(api_json[i]['name']),
            str(api_json[i]['provider']['name']),
            str(api_json[i]['vehicle']['name']),
            str(api_json[i]['pad']['location']['name']),
            padlocation,
            str(api_json[i]['launch_description']),
            launch_date,
            livestream
        )
        txts.append(rocket + ' #' + str(i+1) + ' - <i>' + str(api_json[i]['name']) + '</i> ' + rocket \
                    + '\n' + l.getFormattedText())
    
    providers_list = ["spacex", "ula", "nasa", "roscosmos", "jaxa", "china", "astra", "virgin", "rocketlab"]
    selected = ""
    for i in range(0, len(providers_list)):
        print("Lower data: " + str(api_json[0]['provider']['name']).lower())
        print("Item in list: " + providers_list[i])
        if providers_list[i] in str(api_json[0]['provider']['name']).lower():
            selected = providers_list[i] + '.jpg'
            break

    button_list = [
        InlineKeyboardButton("Watch Livestream (if available)", url=livestream)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

    context.bot.send_photo(chat_id=update.effective_chat.id, 
                            photo=open('imgs/' + selected, 'rb'),
                            caption=txts[0], 
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup)

@send_typing_action
def info(update, context):
    pass
    text = "<b>Launchpad Bot</b> for Telegram by @simocosimo\n\n" \
            "Hi! I really hope you're liking the bot. It is a work in progress, I want to improve" \
            " it as much as possible, in style and in informations. Bare in mind that " \
            " space launches are usually subject to change in schedule, so take the dates" \
            " with a grain of salt. \nFeel free to tweet me at <a href='https://twitter.com/simocosimo'>@simocosimo</a> for problems" \
            " or to ask for a particular function that, according to you, could be useful!\nLet's hope" \
            " we'll not have problems, Houston!"
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=text, 
                            parse_mode=ParseMode.HTML)

@send_typing_action
def helpCommand(update, context):
    pass
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
    PORT = os.environ.get('PORT')
    TOKEN = os.environ["TOKEN"]
    NAME = "launchpad-telegram-bot"
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Setup the logging part of the bot
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    #logger = logging.getLogger(__name__)

    #start_handler = CommandHandler('start', start)
    #dispatcher.add_handler(start_handler)

    nextFive_handler = CommandHandler('launches', launches)
    dispatcher.add_handler(nextFive_handler)

    #nextOne_handler = CommandHandler('next', nextLaunch)
    #dispatcher.add_handler(nextOne_handler)

    nextPic_handler = CommandHandler('next', nextLaunch)
    dispatcher.add_handler(nextPic_handler)

    info_handler = CommandHandler('info', info)
    dispatcher.add_handler(info_handler)

    #help_handler = CommandHandler('help', helpCommand)
    #dispatcher.add_handler(help_handler)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()

if __name__ == '__main__':
    main()
    