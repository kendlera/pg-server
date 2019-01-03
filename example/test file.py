import json
import requests
import time
import threading
import sys
import os
from constants import SERVER_HOST, SERVER_PORT

server_url = SERVER_HOST + SERVER_PORT

cities_board = requests.get(server_url + "/board").json()
player_cities = requests.get(server_url + "/player_info").json()
occupied_cities = []
for c in player_cities['info']:
    print(c)
    occupied_cities.append([c['name'],c['cities']])
#print(json.dumps(cities_board))
#print(cities_board[0][1])
print(occupied_cities)
#convert occupied cities to no buy list
no_buy_list = []
for p in occupied_cities:
    for c in p[1]:
        no_buy_list.append(c)
print(no_buy_list)



