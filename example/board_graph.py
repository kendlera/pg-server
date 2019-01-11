import requests
import random
import json

from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT

#game_board = requests.get(server_url + "/board").json()

game_board = [["Madrid", "Lisboa", 13.0], ["Madrid", "Bordeaux", 16.0], ["Madrid", "Barcelona", 14.0], ["Milano", "Lyon", 11.0], ["Milano", "Zagreb", 17.0], ["Milano", "Roma", 19.0], ["Milano", "Zurich", 11.0], ["Milano", "Marseille", 13.0], ["Milano", "Munchen", 16.0], ["Izmir", "Ankara", 10.0], ["Izmir", "Istanbul", 8.0], ["Barcelona", "Bordeaux", 15.0], ["Barcelona", "Marseille", 11.0], ["Vlaanderen", "Rhein-Main", 6.0], ["Vlaanderen", "Paris", 7.0], ["Vlaanderen", "Bremen", 10.0], ["Vlaanderen", "Randstad", 4.0], ["Vlaanderen", "Rhein-Ruhr", 4.0], ["Vlaanderen", "London", 15.0], ["Odessa", "Bucuresti", 10.0], ["Odessa", "Kyjiv", 9.0], ["Odessa", "Kharkiv", 13.0], ["Odessa", "Budapest", 25.0], ["Praha", "Rhein-Main", 10.0], ["Praha", "Warszawa", 11.0], ["Praha", "Berlin", 7.0], ["Praha", "Munchen", 8.0], ["Praha", "Wien", 7.0], ["Praha", "Katowice", 8.0], ["Ankara", "Istanbul", 9.0], ["Bremen", "Berlin", 6.0], ["Bremen", "Rhein-Main", 9.0], ["Bremen", "Kobenhavn", 12.0], ["Bremen", "Randstad", 8.0], ["Warszawa", "Kyjiv", 14.0], ["Warszawa", "Katowice", 5.0], ["Warszawa", "Berlin", 11.0], ["Warszawa", "Kobenhavn", 25.0], ["Warszawa", "Minsk", 10.0], ["Warszawa", "Riga", 12.0], ["Beograd", "Zagreb", 9.0], ["Beograd", "Tirane", 15.0], ["Beograd", "Napoli", 18.0], ["Beograd", "Bucuresti", 12.0], ["Beograd", "Sofia", 11.0], ["Beograd", "Budapest", 10.0], ["Wien", "Zagreb", 8.0], ["Wien", "Munchen", 9.0], ["Wien", "Katowice", 8.0], ["Wien", "Budapest", 5.0], ["Oslo", "Kobenhavn", 17.0], ["Oslo", "Stockholm", 13.0], ["Kharkiv", "Kyjiv", 9.0], ["Kharkiv", "Moskwa", 15.0], ["Kharkiv", "Minsk", 16.0], ["Kyjiv", "Katowice", 18.0], ["Kyjiv", "Minsk", 10.0], ["Kyjiv", "Budapest", 21.0], ["Stockholm", "Helsinki", 21.0], ["Stockholm", "Kobenhavn", 18.0], ["Randstad", "London", 18.0], ["Bordeaux", "Lyon", 12.0], ["Bordeaux", "Marseille", 12.0], ["Bordeaux", "Paris", 12.0], ["Glasgow", "Birmingham", 13.0], ["Glasgow", "Dublin", 17.0], ["Paris", "Lyon", 11.0], ["Paris", "Zurich", 14.0], ["Paris", "Rhein-Ruhr", 10.0], ["Paris", "Stuttgart", 14.0], ["Paris", "London", 16.0], ["Lyon", "Zurich", 14.0], ["Lyon", "Marseille", 8.0], ["Roma", "Napoli", 7.0], ["Kobenhavn", "Berlin", 15.0], ["Bucuresti", "Budapest", 16.0], ["Bucuresti", "Sofia", 9.0], ["Bucuresti", "Istanbul", 13.0], ["Rhein-Ruhr", "Stuttgart", 5.0], ["Rhein-Ruhr", "Rhein-Main", 3.0], ["Istanbul", "Sofia", 13.0], ["Birmingham", "London", 4.0], ["Birmingham", "Dublin", 15.0], ["Napoli", "Tirane", 25.0], ["Moskwa", "Sankt-Peterburg", 14.0], ["Moskwa", "Minsk", 14.0], ["Moskwa", "Riga", 18.0], ["Munchen", "Zagreb", 14.0], ["Munchen", "Rhein-Main", 6.0], ["Munchen", "Zurich", 8.0], ["Munchen", "Stuttgart", 4.0], ["Sofia", "Tirane", 13.0], ["Sofia", "Athina", 17.0], ["Katowice", "Budapest", 11.0], ["Riga", "Tallinn", 7.0], ["Riga", "Sankt-Peterburg", 13.0], ["Riga", "Minsk", 8.0], ["Rhein-Main", "Stuttgart", 3.0], ["Rhein-Main", "Berlin", 10.0], ["Zurich", "Stuttgart", 5.0], ["Tallinn", "Sankt-Peterburg", 9.0], ["Budapest", "Zagreb", 7.0], ["Helsinki", "Sankt-Peterburg", 11.0], ["Athina", "Tirane", 16.0]]


def generate_pg_graph(game_board):
    """included countries list:  nodes, edges and costs  returns game_graph"""

    def make_link(G, node1, node2, cost):
        if node1 not in G:
            G[node1] = {}
        (G[node1])[node2] = cost
        if node2 not in G:
            G[node2] = {}
        (G[node2])[node1] = cost
        return G

    G = {}
    for (x,y,z) in game_board: make_link(G,x,y,z)
    return G



# cities_board = requests.get(server_url + "/board").json()
# player_cities = requests.get(server_url + "/city_status").json()
occupied_cities = []
for c in player_cities['info']:
    print(c)
    occupied_cities.append([c['name'],c['cities']])
#print(json.dumps(cities_board))
