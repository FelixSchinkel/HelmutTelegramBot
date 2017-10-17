import apiParser


def get_price(price):
    if price is None:
        return ""
    return format(price, '.2f') + ' €'


def get_meals(canteen_name):
    canteens = apiParser.get_canteens()
    result = str()
    for canteen in canteens:
        if canteen_name.lower() in canteen['name'].lower():
            if canteen['closed']:
                result += "{} hat heut zu.\n".format(canteen['name'])
            else:
                result += "*{canteen}*\n\t".format(canteen=canteen['name'])
                for meal in canteen['meals']:
                    result += "-{meal} _{price}_\n\t".format(meal=meal['name'],
                                                             price=get_price(meal['prices']['students']))

    if not result:
        result = "Konnte für {} keine Mensa finden.".format(canteen_name)

    return result


def vegan_meals():
    canteens = apiParser.get_canteens()
    result = str()
    # filter out all vegan meals
    for canteen in canteens:
        if canteen['closed']:
            continue
        for meal in canteen['meals']:
            if any("vegan" in n for n in meal['notes']):
                result += "*{canteen}*\n\t -{meal} _{price}_\n".format(canteen=canteen['name'], meal=meal['name'],
                                                                       price=get_price(meal['prices']['students']))

    # when there is no vegan food ...
    if not result:
        result = "Nischt veganes heut! 🌱"

    return result
