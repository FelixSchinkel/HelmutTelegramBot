import urllib.request
import json
import datetime
import logging

parse_date = []
global_canteens = []


def get_canteens():
    api_loc = "http://openmensa.org/api/v2/canteens"

    # first check, if the meals are alrady up to date
    global parse_date
    global global_canteens
    if not parse_date or parse_date != datetime.date.today():
        parse_date = datetime.date.today()
        # find all suitable canteens near to the WU11
        link = "{api}?near[lat]={lat}&near[lng]={long}".format(api=api_loc, lat=51.029183, long=13.749062)
        with urllib.request.urlopen(link) as response:
            canteens = json.loads(response.read().decode())

        # now get for each canteen the current meal plan for today and add them to the corresponding canteen
        for i, canteen in enumerate(canteens):
            # remove city from canteen name
            canteen['name'] = canteen['name'].split(',')[1]

            date = datetime.datetime.today().strftime("%d-%m-%Y")

            link = "{api}/{canteenId}/days/{date}".format(api=api_loc, canteenId=canteen['id'], date=date)
            with urllib.request.urlopen(link) as response:
                canteen_status = json.loads(response.read().decode())
            if canteen_status['closed']:
                canteens[i].update({'closed': True})
            else:
                canteens[i].update({'closed': False})
                link = "{api}/{canteenId}/days/{date}/meals".format(api=api_loc, canteenId=canteen['id'], date=date)
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


if __name__ == "__main__":
    get_canteens()
