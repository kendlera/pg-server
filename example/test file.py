# import json
# import requests
# import time
# import threading
# import sys
# import os
# from constants import SERVER_HOST, SERVER_PORT
#
# server_url = SERVER_HOST + SERVER_PORT
#
# cities_board = requests.get(server_url + "/board").json()
# player_cities = requests.get(server_url + "/player_info").json()
# occupied_cities = []
# for c in player_cities['info']:
#     print(c)
#     occupied_cities.append([c['name'],c['cities']])
# #print(json.dumps(cities_board))
# #print(cities_board[0][1])
# print(occupied_cities)
# #convert occupied cities to no buy list
# no_buy_list = []
# for p in occupied_cities:
#     for c in p[1]:
#         no_buy_list.append(c)
# print(no_buy_list)
#
'Rhein-Main', 'Berlin', 'Praha', 'Minsk', 'Riga', 'Warszawa', 'Bordeaux', 'Lyon', 'Paris'

all_city_info = {
    "info": [
        {
            "name": "player_one",
            "resources": {
                "COAL": 0,
                "GAS": 2,
                "URANIUM": 0,
                "OIL": 0
            },
            "powerplants": [
                {
                    "type": "dark",
                    "resource_cost": 2,
                    "resource_type": "GAS",
                    "market_cost": 5,
                    "generators": 1
                }
            ],
            "money": 36,
            "cities": ['Rhein-Main']
        },
        {
            "name": "player_two",
            "resources": {
                "COAL": 0,
                "GAS": 0,
                "URANIUM": 0,
                "OIL": 1
            },
            "powerplants": [
                {
                    "type": "dark",
                    "resource_cost": 1,
                    "resource_type": "OIL",
                    "market_cost": 6,
                    "generators": 1
                }
            ],
            "money": 38,
            "cities": ['Berlin']
        },
        {
            "name": "player_three",
            "resources": {
                "COAL": 2,
                "GAS": 0,
                "URANIUM": 0,
                "OIL": 0
            },
            "powerplants": [
                {
                    "type": "dark",
                    "resource_cost": 2,
                    "resource_type": "COAL",
                    "market_cost": 4,
                    "generators": 1
                }
            ],
            "money": 37,
            "cities": ['Riga']
        }
    ]
}
players_cities = []
for p in all_city_info['info']:
   for c in p['cities']:
       players_cities.append(c)


#print(players_cities)


# my_info = {
#     "info": {
#             "cities": ["Munchen","Stuttgart","Rhein-Main"],
#             "name": "player_one",
#             "resources": {"URANIUM": 0,"OIL": 0,"COAL": 8,"GAS": 2},
#             "powerplants": [
#                         {"resource_cost": 1, "resource_type": "HYBRID", "generators": 1, "type": "dark", "market_cost": 6},
#                         {"resource_cost": 3, "resource_type": "COAL", "generators": 2, "type": "dark", "market_cost": 9},
#                         {"resource_cost": 1, "resource_type": "COAL", "generators": 2, "type": "dark", "market_cost": 15}
#                        ],
#             "money": 12.0
#             }
#           }

my_info = {
    "info": {
        "cities": [
            "Wien",
            "Budapest",
            "Praha"
        ],
        "powerplants": [
            {
                "type": "dark",
                "generators": 1,
                "resource_type": "COAL",
                "market_cost": 3,
                "resource_cost": 2
            },
            {
                "type": "dark",
                "generators": 2,
                "resource_type": "COAL",
                "market_cost": 9,
                "resource_cost": 3
            },
            {
                "type": "dark",
                "generators": 1,
                "resource_type": "COAL",
                "market_cost": 7,
                "resource_cost": 1
            }
        ],
        "name": "player_one",
        "resources": {
            "OIL": 0,
            "URANIUM": 0,
            "GAS": 0,
            "COAL": 4
        },
        "money": 7.0
    }
}



def pps_need_to_power(my_info):
    '''given my resource and my PPs and my cities which pps to power'''
    pp_to_power = []
    sum_my_pp = {}
    num_cities = len(my_info['info']['cities'])
    for p in my_info['info']['powerplants']:
        #print(p)
        if p['resource_type'] not in sum_my_pp:
            sum_my_pp[p['resource_type']] = p['resource_cost']
        else:
            sum_my_pp[p['resource_type']] += p['resource_cost']
    for r in sum_my_pp:
        if r == "HYBRID":
            pass
        else:
            if sum_my_pp[r] <= my_info['info']['resources'][r]:
                for p in my_info['info']['powerplants']:
                    if p['resource_type'] == r:
                        pp_to_power.append(p['market_cost'])
            else:
                if p['resource_type'] == r:
                    pp_to_power.append(p['market_cost'])

    return pp_to_power

print(pps_need_to_power(my_info))

