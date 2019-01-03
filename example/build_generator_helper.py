import requests
import random
import json

from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT

nodes = ['Lyon', 'Sofia', 'Istanbul', 'Paris', 'Wien', 'Riga', 'Vlaanderen', 'Bremen', 'Beograd', 'Tallinn', 'Tirane', 'Glasgow', 'Odessa', 'Zagreb', 'Praha', 'Randstad', 'Ankara', 'Berlin', 'Munchen', 'Katowice', 'Oslo', 'Birmingham', 'Moskwa', 'Budapest', 'Rhein-Main', 'Napoli', 'Warszawa', 'Dublin', 'Milano', 'Kharkiv', 'Barcelona', 'Stuttgart', 'Minsk', 'Stockholm', 'Roma', 'Bordeaux', 'Marseille', 'Kyjiv', 'Zurich', 'Madrid', 'Athina', 'Rhein-Ruhr', 'Kobenhavn', 'Helsinki', 'Bucuresti', 'London', 'Sankt-Peterburg', 'Lisboa', 'Izmir']



def main(player, my_info, player_token):
    my_info = requests.get(server_url + "/my_info", cookies=player_token).json()
    #player_info = requests.get(server_url + "/player_info",cookies=player_token).json()
    print(json.dumps(my_info, indent=4))
    response = choose_generator(my_info['info']['name'], player_token)
    print(response)

def choose_generator(player_name, player_token):

    payload = dict(player_name=player_name)
    payload['paths']= [random.choice(nodes)]
    print('payload', payload)
    response = requests.post(server_url + "/build", data=payload, cookies=player_token)
    print(response.status_code)
    return response



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
# player_cities = requests.get(server_url + "/player_info").json()
# occupied_cities = []
# for c in player_cities['info']:
#     print(c)
#     occupied_cities.append([c['name'],c['cities']])
# print(json.dumps(cities_board))


#the_game_graph = generate_pg_graph(pg_cities)