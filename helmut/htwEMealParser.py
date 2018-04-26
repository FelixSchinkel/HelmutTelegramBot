import urllib.request
import json

import datetime

parse_date = []
all_meals = []


def get_meals(canteen_name):
    meals = check_for_new_meals()
    # now return all meals matching the canteen name
    result = str()
    for meal in meals:
        if canteen_name.lower() in meal['canteen'].lower():
            result += "- {meal} _{price}_ {emoji}\n".format(
                meal=meal['title'],
                price=get_price(meal),
                emoji=get_emoji(meal))

    if len(result) == 0:
        result = "Keine Mensa für *{}* gefunden.".format(canteen_name)

    return result


def get_vegan_meals():
    meals = check_for_new_meals()
    result = str()
    for meal in meals:
        if any("vegan" in x for x in meal['information']):
            result += "-*{canteen}*: {meal} _{price}_ {emoji}\n".format(
                canteen=meal['canteen'],
                meal=meal['title'],
                price=get_price(meal),
                emoji=get_emoji(meal))

    if len(result) == 0:
        result = "Zum Glück gibt's heut nischt veganes!!!"
    return result


def check_for_new_meals():
    global parse_date
    global all_meals
    if not parse_date or parse_date != datetime.date.today():
        parse_date = datetime.date.today()

        link = "https://rubu2.rz.htw-dresden.de/API/emeal/meals"
        with urllib.request.urlopen(link) as response:
            all_meals = json.loads(response.read().decode())

    return all_meals


def get_price(meal):
    if meal['studentPrice'] == 0:
        return ""
    price = str(meal['studentPrice'])
    if len(price) == 1:
        price += "."
    if len(price) <= 4:
        price += "0" * (4 - len(price))
    return price + "€"


def get_emoji(meal):
    emoji = str()
    # check for keywords and return the appropriate emoji
    for i in meal['information']:
        if "vegan" in i:
            emoji += "🌱"
            continue
        elif "vegetarian" in i:
            emoji += "🥕"
            continue
        elif "beef" in i:
            emoji += "🐮"
            continue
        elif "pork" in i:
            emoji += "🐷"
            continue
        elif "alcohol" in i:
            emoji += "🍸"
            continue
    return emoji


if __name__ == "__main__":
    get_meals("zelt")
