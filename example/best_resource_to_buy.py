import min_resource as min_resource

#my_info = requests.get(server_url + "/my_info", cookies=player_token).json()

# my_info = {
#     "info": {
#         "money": 17,
#         "cities": [
#             "Bucuresti"
#         ],
#         "name": "player_three",
#         "resources": {
#             "URANIUM": 0,
#             "GAS": 0,
#             "OIL": 0,
#             "COAL": 4
#         },
#         "powerplants": [
#             {
#                 "resource_cost": 2,
#                 "generators": 1,
#                 "market_cost": 4,
#                 "resource_type": "COAL",
#                 "type": "dark"
#             },
#             {
#                 "resource_cost": 1,
#                 "generators": 2,
#                 "market_cost": 13,
#                 "resource_type": "URANIUM",
#                 "type": "dark"
#             },
#             {
#                 "resource_cost": 1,
#                 "generators": 3,
#                 "market_cost": 21,
#                 "resource_type": "URANIUM",
#                 "type": "light"
#             }
#         ]
#     }
# }

def cur_cheapest_res(my_info, resource_state):
    cur_best = []
    #print('res', resource_state)
    for p in my_info['info']['powerplants']:
        #print(p['resource_cost'],p['resource_type'])
        cur_best.append([p['market_cost'], p['resource_cost'],p['resource_type'], p['generators'], (p['generators']/min_resource.how_much_to_buy(resource_state,p['resource_cost'],p['resource_type']))])
    def take_third(elem):
        return elem[4]
    cur_best.sort(key=take_third, reverse=True)
    return  cur_best


# what = 'COAL'
# to_buy = 4
#resource_state = {"OIL": 16, "URANIUM": 5, "GAS": 18, "COAL": 23}

def best_poss_res(my_info, resource_state):
    #sorted list of cheapest to power  [card id, res, #to buy, price, # gens to power
    cheapest_to_power = []
    hypo_resource = resource_state
    best_to_buy = cur_cheapest_res(my_info, resource_state)
    for h in best_to_buy:
        if h[2] == 'HYBRID':
            h[2] = 'gas'
        cost = min_resource.how_much_to_buy(hypo_resource, h[1], h[2])
        hypo_resource[h[2]] -= h[1]
        cheapest_to_power.append([h[0], h[2], h[1], cost, h[3]])
    #print(hypo_resource)
    return cheapest_to_power






#
# print(cur_cheapest_res(my_info, resource_state))
# print(best_poss_res(my_info, resource_state))




