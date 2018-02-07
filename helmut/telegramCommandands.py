import logging
import json
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent

import openMensaParser
import helpers


def vegan_command(bot, update):
    result = helpers.vegan_meals()

    bot.send_message(chat_id=update.message.chat_id, text=result, parse_mode='Markdown')
    logging.info("Send /vegan to id: {} with text: {}".format(update.message.chat_id, result))


def get_meals_for_canteen(bot, update, args):
    result = helpers.get_meals(args[0])

    bot.send_message(chat_id=update.message.chat_id, text=result, parse_mode='Markdown')
    logging.info("Send /essen {} to id: {} with text: {}".format(args[0], update.message.chat_id, result))


def inline_mode(bot, update):
    """
    Using inline query mode for:
        canteen name
        vegan meals in all canteens
    """
    query = update.inline_query.query
    if not query:
        return
    results = list()

    # check if query is an canteen name
    # minimum length of query so not all canteens are loaded every time
    if len(query) > 2:
        canteens = openMensaParser.get_canteens()
        for canteen in canteens:
            if query in canteen['name'].lower():
                results.append(
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title=canteen['name'],
                        input_message_content=InputTextMessageContent(helpers.get_meals(canteen['name']),
                                                                      parse_mode='Markdown')
                    )
                )

        # check if query is vegan
        if query in "vegan":
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title='vegan meals',
                    input_message_content=InputTextMessageContent(helpers.vegan_meals(), parse_mode='Markdown')
                )
            )

    if query in "cat":
        from telegram import InlineQueryResultPhoto
        import urllib.request
        url = urllib.request.urlopen("http://thecatapi.com/api/images/get?type=jpg&format=src&size=small").geturl()
        results.append(
            InlineQueryResultPhoto(
                id=uuid4(),
                photo_url=url,
                thumb_url=url,
            )
        )

    bot.answer_inline_query(update.inline_query.id, results)

