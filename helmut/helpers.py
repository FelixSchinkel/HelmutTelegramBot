import datetime
import populartimes

from config import Config
import htwEMealParser


# def get_popular_times(canteen_name):
#     canteen = htwEMealParser.get_meals(canteen_name)[0][
#         'canteen']  # use only one canteen, because parsing of popularity takes pretty long
#     search_radius = 0.001
#     coordinates = canteen['coordinates']
#     pop_times = populartimes.get(Config.GMAPS_API_KEY, ['restaurant'],
#                                  (coordinates[0] - search_radius, coordinates[1] - search_radius),
#                                  (coordinates[0] + search_radius, coordinates[1] + search_radius))
#
#     # if current popularity is available compare it to normal popularity
#     canteen_population = pop_times[0]
#
#     # get normal population
#     now = datetime.datetime.now()
#     day_name = now.strftime('%A')
#     day_data = [x for x in canteen_population['populartimes'] if x['name'] == day_name][0]
#     normal_popularity = day_data['data'][now.hour]
#
#     if 'current_popularity' in canteen_population:
#         current_popularity = canteen_population['current_popularity']
#
#         if current_popularity > normal_popularity:
#             return ('{name}: Voller als sonst: {curr}% zu {normal}%'
#                     .format(name=canteen['name'], curr=current_popularity, normal=normal_popularity))
#         else:
#             return ('{name}: Leerer als sonst: {curr}% zu {normal}%'
#                     .format(name=canteen['name'], curr=current_popularity, normal=normal_popularity))
#
#     return '{name}: Keine live Werte vorhanden. Normal: {normal}%' \
#         .format(name=canteen['name'], normal=normal_popularity)
