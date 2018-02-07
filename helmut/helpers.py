import openMensaParser


def get_price(price):
    if price is None:
        return ""
    return format(price, '.2f') + ' €'


def get_meals(canteen_name):
    canteens = openMensaParser.get_canteens()
    result = str()
    for canteen in canteens:
        if canteen_name.lower() in canteen['name'].lower():
            if canteen['closed']:
                result += "{} hat heut zu.\n".format(canteen['name'])
            else:
                result += "*{canteen}*\n\t".format(canteen=canteen['name'])
                for meal in canteen['meals']:
                    result += "-{meal} _{price}_ {emoji}\n\t".format(meal=meal['name'],
                                                             price=get_price(meal['prices']['students']),
                                                                     emoji = get_emojis_for_ingredients(meal['notes']))

    if not result:
        result = "Konnte für {} keine Mensa finden.".format(canteen_name)

    return result


def vegan_meals():
    canteens = openMensaParser.get_canteens()
    result = str()
    # filter out all vegan meals
    for canteen in canteens:
        if canteen['closed']:
            continue

        vegan_meals_list = [meal for meal in canteen['meals'] if any("vegan" in n for n in meal['notes'])]
        if vegan_meals_list:
            result += "*{canteen}*\n".format(canteen=canteen['name'])
            for meal in vegan_meals_list:
                result += "\t -{meal} _{price}_ {emoji}\n".format(meal=meal['name'],
                                                          price=get_price(meal['prices']['students']),
                                                                  emoji = get_emojis_for_ingredients(meal['notes']))

    # when there is no vegan food ...
    if not result:
        result = "Nischt veganes heut! 🌱"

    return result

def get_emojis_for_ingredients(ingredients):
    emoji = ""
    # check for keywords and return the appropriate emoji
    for i in ingredients:
        if "vegan" in i:
            emoji += "🌱"
            continue
        elif "vegetarisch" in i:
            emoji += "🥕"
            continue
        elif "Rindfleisch" in i:
            emoji += "🐮"
            continue
        elif "Schweinefleisch" in i:
            emoji += "🐷"
            continue
        elif "Alkohol" in i:
            emoji += "🍸"
            continue
        # elif "Knoblauch" in i:    # TODO no suitable emoji?
        #     emoji = emoji + ""
        #     continue

    return emoji

def get_popular_times():
    pass