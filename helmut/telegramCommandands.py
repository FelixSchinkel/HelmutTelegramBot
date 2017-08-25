import logging
import apiParser


def get_price(price):
    if price is None:
        return ""
    return format(price, '.2f') + ' €'


def vegan_command(bot, update):
    canteens = apiParser.get_canteens()

    result = str()
    # filter out all vegan meals
    for canteen in canteens:
        for meal in canteen['meals']:
            if any("vegan" in n for n in meal['notes']):
                result += "{}\n\t -{} {}\n".format(canteen['name'], meal['name'], get_price(meal['prices']['students']))

    # should never happen, but just in case...
    if not result:
        result = "Nischt veganes heut!"
    bot.send_message(chat_id=update.message.chat_id, text=result)
    logging.info("Send /vegan to id: {} with text: {}".format(update.message.chat_id, result))


def get_meals_for_canteen(bot, update, args):
    canteens = apiParser.get_canteens()

    result = str()

    for canteen in canteens:
        if args[0].lower() in canteen['name'].lower():
            result += "{}:\n\t".format(canteen['name'])
            for meal in canteen['meals']:
                result += "-{} {}\n\t".format(meal['name'], get_price(meal['prices']['students']))

    if not result:
        result = "Konnte für {} keine Mensa finden. Spasst".format(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=result)
    logging.info("Send /essen {} to id: {} with text: {}".format(args[0], update.message.chat_id, result))
