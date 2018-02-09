import datetime
import populartimes

import openMensaParser
from config import Config


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


def get_canteen(canteen_name):
    """
    return canteens for the given name
    """

    canteens = openMensaParser.get_canteens()
    data = [x for x in canteens if canteen_name.lower() in str(x['name']).lower()]

    return data


def get_popular_times(canteen_name):
    canteen = get_canteen(canteen_name)[0]  # use only one canteen, because parsing of popularity takes pretty long
    search_radius = 0.001
    coordinates = canteen['coordinates']
    pop_times = populartimes.get(Config.GMAPS_API_KEY, ['restaurant'], (coordinates[0]-search_radius,coordinates[1]-search_radius), (coordinates[0]+search_radius,coordinates[1]+search_radius))

    # if current popularity is available compare it to normal popularity
    canteen_population = pop_times[0]

    # get normal population
    now = datetime.datetime.now()
    day_name = now.strftime('%A')
    day_data = [x for x in canteen_population['populartimes'] if x['name'] == day_name][0]
    normal_popularity = day_data['data'][now.hour] - 1

    if 'current_popularity' in canteen_population:
        current_popularity = canteen_population['current_popularity']

        if current_popularity > normal_popularity:
            return('{name}: Voller als sonst: {curr}% zu {normal}%'
                   .format(name = canteen['name'],curr = current_popularity, normal = normal_popularity))
        else:
            return('{name}: Leerer als sonst: {curr}% zu {normal}%'
                   .format(name = canteen['name'], curr = current_popularity, normal = normal_popularity))

    return '{name}: Keine live Werte vorhanden. Normal: {normal}%'\
        .format(name=canteen['name'], normal = normal_popularity)