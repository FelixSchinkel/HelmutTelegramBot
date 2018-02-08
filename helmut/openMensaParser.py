import urllib.request
import json
import datetime
import logging

from config import Config

parse_date = []
global_canteens = []


def get_canteens():

    # first check, if the meals are already up to date
    global parse_date
    global global_canteens
    if not parse_date or parse_date != datetime.date.today():
        parse_date = datetime.date.today()
        # find all suitable canteens near to the given position
        link = "{api}?near[lat]={lat}&near[lng]={long}"\
            .format(api=Config.OPEN_MENSA_URL, lat=Config.POSITION_LAT, long=Config.POSITION_LONG)
        with urllib.request.urlopen(link) as response:
            canteens = json.loads(response.read().decode())

        # now get for each canteen the current meal plan for today and add them to the corresponding canteen
        for i, canteen in enumerate(canteens):
            # remove city from canteen name
            canteen['name'] = canteen['name'].split(',')[1]

            date = datetime.datetime.today().strftime("%d-%m-%Y")

            link = "{api}/{canteenId}/days/{date}"\
                .format(api=Config.OPEN_MENSA_URL, canteenId=canteen['id'], date=date)
            with urllib.request.urlopen(link) as response:
                canteen_status = json.loads(response.read().decode())
            if canteen_status['closed']:
                canteens[i].update({'closed': True})
            else:
                canteens[i].update({'closed': False})
                link = "{api}/{canteenId}/days/{date}/meals"\
                    .format(api=Config.OPEN_MENSA_URL, canteenId=canteen['id'], date=date)
                # fetch meals and then add them to canteens
                with urllib.request.urlopen(link) as response:
                    meals = json.loads(response.read().decode())
                canteens[i].update({'meals': meals})

            # #save as json file
            #  with open("canteensJson.txt", "w") as fp:
            #      json.dump(canteens, fp)

            # load json file
            # with open("canteensJson.txt") as fp:
            #     canteens = json.load(fp)

        # save meals om global variable so next time no parse is needed
        global_canteens = canteens
        logging.info("Got all meals for: {}".format(parse_date))
    return global_canteens
