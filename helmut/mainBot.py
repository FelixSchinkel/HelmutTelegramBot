import logging
import sys
from telegram.ext import Updater, CommandHandler

import telegramCommandands


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if len(sys.argv) < 2:
        print("Token needed!! Aborting")
        return

    updater = Updater(sys.argv[1])
    dispatcher = updater.dispatcher

    meal_handler = CommandHandler("essen", telegramCommandands.get_meals_for_canteen, pass_args=True)
    meal_handler_vegan = CommandHandler("vegan", telegramCommandands.vegan_command)
    dispatcher.add_handler(meal_handler)
    dispatcher.add_handler(meal_handler_vegan)
    updater.start_polling()

    logging.info("Ready")


if __name__ == "__main__":
    main()
