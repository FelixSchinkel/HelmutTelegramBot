import urllib.request
import json
import datetime


def get_canteens():
    apiLoc = "http://openmensa.org/api/v2/canteens"

    # find all suitable canteens near to the WU11
    link = "{api}?near[lat]={lat}&near[lng]={long}".format(api=apiLoc, lat=51.029183, long=13.749062)
    with urllib.request.urlopen(link) as response:
        canteens = json.loads(response.read().decode())

    # now get for each canteen the current meal plan for today and add them to the corresponding canteen
    for i, canteen in enumerate(canteens):
        date = datetime.datetime.today().strftime("%d-%m-%Y")

        link = "{api}/{canteenId}/days/{date}/meals".format(api=apiLoc, canteenId=canteen['id'], date=date)
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

    return canteens


if __name__ == "__main__":
    get_canteens()
