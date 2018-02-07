import logging
import sys

import os
import telegram
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

import telegramCommandands
from config import Config

USAGE_TEXT = """

Usage:
    EXPORT TELEGRAM_API_KEY='Your API Key'
    python mainBot.py
"""


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if Config.TELEGRAM_API_KEY is None:
        print('No Telegram API Key given.' + USAGE_TEXT)

    # check if valid API Token is applied
    updater = Updater(Config.TELEGRAM_API_KEY)
    try:
        status = updater.bot.getMe()
    except telegram.TelegramError:
        print("Api Key not valid!" + USAGE_TEXT)
        return
    else:
        logging.info("Authenticated as: {}".format(status['username']))

    dispatcher = updater.dispatcher

    # configure keywords
    meal_handler = CommandHandler("essen", telegramCommandands.get_meals_for_canteen, pass_args=True)
    meal_handler_vegan = CommandHandler("vegan", telegramCommandands.vegan_command)

    dispatcher.add_handler(meal_handler)
    dispatcher.add_handler(meal_handler_vegan)

    inline_caps_handler = InlineQueryHandler(telegramCommandands.inline_mode)
    dispatcher.add_handler(inline_caps_handler)

    updater.start_polling()

    logging.info("Ready")


if __name__ == "__main__":
    main()
