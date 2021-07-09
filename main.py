#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater

from handlerUtils import MessageHandlers,ErrorHandler,CommandHandlers

from configUtils import ConfigUtils

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def main():

    #TODO: handle Argparse and config.
    #Use telegram.ext.DictPersistence to save the default data.
    configs = ConfigUtils.init()

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(configs["token"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Set userdata for dispatcher.
    # on different commands - answer in Telegram
    CommandHandlers.init(dp)

    # on noncommand i.e message - echo the message on Telegram
    MessageHandlers.init(dp)

    #Error handler
    ErrorHandler.init(dp)

    # Set the bot's list of commands
    # TODO: move to handlers
    cmdlist = [ ('/start', 'Get started with this bot.'),
                ('/help', 'See all available commands and descriptions'),
                ('/download', 'Start downloading your own music!')]

    updater.bot.set_my_commands(cmdlist)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
