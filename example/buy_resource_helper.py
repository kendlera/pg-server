import requests
import random
import json



from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT


def cur_cheapest_res(my_info, resource_state):
    cur_best = []
    for p in my_info['info']['powerplants']:
        if p['resource_type'] == 'HYBRID':
            if resource_state['GAS'] > resource_state['OIL']:
                type_resource = 'GAS'
            else:
                type_resource = 'OIL'
        else:
            type_resource = p['resource_type']
        #print('resource type  ', p['resource_type'])
        cur_best.append([p['market_cost'], p['resource_cost'],type_resource, p['generators'], int(p['generators']/(how_much_to_buy(resource_state, p['resource_cost'], type_resource)+.0001))])
    def take_third(elem):
        return elem[4]
    cur_best.sort(key=take_third, reverse=True)
    return  cur_best



def best_poss_res(my_info, resource_state):
    #sorted list of cheapest to power  [card id, res, #to buy, price, # gens to power
    cheapest_to_power = []
    hypo_resource = resource_state
    best_to_buy = cur_cheapest_res(my_info, resource_state)
    for h in best_to_buy:
        if h[2] == 'HYBRID':
            if resource_state['GAS'] > resource_state['OIL']:
                h[2] = 'GAS'
            else:
                h[2] = 'OIL'
        cost = how_much_to_buy(hypo_resource, h[1], h[2])
        if h[2] != 'CLEAN':
            hypo_resource[h[2]] -= h[1]
        else:
            hypo_resource[h[2]] = h[1]
        cheapest_to_power.append([h[0], h[2], h[1], cost, h[3]])
    return cheapest_to_power



def how_much_to_buy(resource_state, to_buy, what):

    bin_dic = {'COAL': [[9, 0], [9, 0],  [8, 0], [8, 0],  [7, 0], [7, 0],
                [6, 0], [6, 0], [6, 0], [5, 0], [5, 0], [5, 0],  [4, 0], [4, 0], [4, 0],  [3, 0], [3, 0],
                [3, 0], [3, 0], [2, 0], [2, 0], [2, 0], [2, 0], [1, 0], [1, 0], [1, 0], [1, 0]],
    'GAS': [[8, 0], [8, 0], [8, 0], [7, 0], [7, 0], [7, 0],
                [6, 0], [6, 0], [6, 0], [5, 0], [5, 0], [5, 0],  [4, 0], [4, 0], [4, 0],  [3, 0], [3, 0],
                [3, 0],  [2, 0], [2, 0], [2, 0],  [1, 0], [1, 0], [1, 0]],
    'OIL':[[9, 0], [9, 0], [9, 0], [9, 0], [8, 0], [8, 0],  [7, 0], [7, 0], [6, 0],
                [6, 0], [5, 0], [5, 0],  [4, 0], [4, 0],  [3, 0], [3, 0],
                 [2, 0], [2, 0],  [1, 0], [1, 0]],
    'URANIUM': [[9, 0], [9, 0],  [8, 0], [8, 0],  [7, 0], [7, 0],  [6, 0],
                  [5, 0],  [4, 0], [3, 0],  [2, 0],  [1, 0]]}

    if what == "CLEAN":
        return 0
    elif to_buy > resource_state[what]:
        return "sorry only "+ str(resource_state[what])+' ' + what +" to buy"

    def fill_bin(what):
        for i in range(resource_state[what]):
            bin_dic[what][i][1] = 1

    fill_bin(what)
    monies = [a[0]*a[1] for a in bin_dic[what] if a[1]>0]
    run_sum = 0
    for i in range(len(monies)-1, len(monies)- to_buy-1, -1):
        run_sum += monies[i]
    return run_sum


def main(player_name, my_info, player_token):
    my_info = requests.get(server_url + "/my_info",cookies=player_token).json()
    res_to_buy = requests.get(server_url + "/resources").json()
    print('resource state ', res_to_buy)
    res_desired = best_poss_res(my_info,res_to_buy)
    payload = dict(player_name=my_info['info']['name'])
    for r in res_desired:
        payload[r[1]]= r[2]
    print('buy_resource payload', payload)
    response = buy_resource(my_info['info']['name'],player_token, payload)
    #if response.get('status') != 'SUCCESS':
    print('response msg ', response.get('msg'))


def buy_resource(player_name, player_token, payload):
    response = requests.post(server_url + "/buy", json=payload, cookies=player_token).json()
    return response
