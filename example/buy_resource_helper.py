import requests
import random
import json
from best_resource_to_buy import best_poss_res


from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT


def main(player_name, my_info, player_token):
    my_info = requests.get(server_url + "/my_info",cookies=player_token).json()
    res_to_buy = requests.get(server_url + "/resources").json()
    res_desired = best_poss_res(my_info,res_to_buy)
    payload = dict(player_name=player_name)
    for r in res_desired:
        payload[r[1]]= r[2]

    response = buy_resource(my_info['info']['name'],player_token, payload)
    if response.get('status') != 'SUCCESS':
        print('if loop', response.get('msg'))


def buy_resource(player_name, player_token, payload):
    #print('payload', payload)
    response = requests.post(server_url + "/buy", data=payload, cookies=player_token).json()
    return response
