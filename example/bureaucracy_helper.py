import requests
import random
import json

from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT


def pps_need_to_power(my_info):
    '''given my resource and my PPs and my cities which pps to power'''
    pp_to_power = []
    my_pp = {}
    num_cities = len(my_info['info']['cities'])
    for p in my_info['info']['powerplants']:
        #print(p)
        if p['resource_type'] not in my_pp:
            my_pp[p['resource_type']] = p['resource_cost']
        else:
            my_pp[p['resource_type']] += p['resource_cost']
    for r in my_pp:
        if r == "HYBRID":
            pass
        elif r == 'CLEAN':
            pp_to_power.append(p['market_cost'])
        else:
            if (my_pp[r] <= my_info['info']['resources'][r]) and (my_pp[r] > 0):
                for p in my_info['info']['powerplants']:
                    if p['resource_type'] == r:
                        pp_to_power.append(p['market_cost'])
            else:
                if p['resource_type'] == r:
                    pp_to_power.append(p['market_cost'])
    return pp_to_power

def main(player, my_info, player_token):
    my_info = requests.get(server_url + "/my_info",cookies=player_token).json()
    #print(json.dumps(my_info, indent=4))
    response = choose_power(my_info['info']['name'], player_token)
    #print(json.dumps(my_info, indent=4))
    #print('name = ',my_info['info']['name'], 'money = ', my_info['info']['money'], '   resources = ', my_info['info']['resources'])
    #if response.get('status') != 'SUCCESS':
    print('response msg ', response.get('msg'))
    print('number of turns = ', player.num_turns)

def choose_power(player_name, player_token):
    my_info = requests.get(server_url + "/my_info", cookies=player_token).json()
    payload = dict(player_name=player_name)
    payload['powerplants']= pps_need_to_power(my_info)

    print('bureacracy payload', payload)
    response = requests.post(server_url + "/power", json=payload, cookies=player_token).json()
    #print(response.text)
    return response

