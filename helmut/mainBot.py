import logging
import sys

import telegram
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

import telegramCommandands

USAGE_TEXT = """

Usage:
    python mainBot.py API_KEY
"""


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if len(sys.argv) < 2:
        print("Api Key needed!" + USAGE_TEXT)
        return

    # check if valid API Token is applied
    updater = Updater(sys.argv[1])
    try:
        status = updater.bot.getMe()
    except telegram.TelegramError:
        print("Api Key not valid!" + USAGE_TEXT)
        return
    else:
        logging.info("Authenticated as: {}".format(status['username']))

    dispatcher = updater.dispatcher

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
