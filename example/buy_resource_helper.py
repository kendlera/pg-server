import requests
import random
import json

from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT


def main(player, my_info, player_token):
    my_info = requests.get(server_url + "/my_info",cookies=player_token).json()
    print(json.dumps(my_info, indent=4))

    res_to_buy = my_info['info']['powerplants'][0]['resource_type']
    # deal with hybrid gas or oil
    if res_to_buy == 'HYBRID':
        res_to_buy = 'OIL'
    # buy resources
    response = buy_resource(player.get('info').get('name'),player_token, 1, res_to_buy)
    if response.get('status') != 'SUCCESS':
        print('if loop', response.get('msg'))

def buy_resource(player_name, player_token, amt, resource_type):
    payload = dict(player_name=player_name)
    payload[resource_type]=amt
    print('payload', payload)
    response = requests.post(server_url + "/buy", data=payload, cookies=player_token).json()
    #print(json.dumps(response, indent=4))
    #print('buy_re function', response)
    return response
