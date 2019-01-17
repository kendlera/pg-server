


def cur_cheapest_res(my_info, resource_state):
    cur_best = []
    for p in my_info['info']['powerplants']:
        cur_best.append([p['market_cost'], p['resource_cost'],p['resource_type'], p['generators'], (p['generators']/how_much_to_buy(resource_state,p['resource_cost'],p['resource_type']))])
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
            if resource_state['GAS'] > resource_state['COAL']:
                h[2] = 'gas'
            else:
                h[2] = 'coal'
        cost = min_resource.how_much_to_buy(hypo_resource, h[1], h[2])
        hypo_resource[h[2]] -= h[1]
        cheapest_to_power.append([h[0], h[2], h[1], cost, h[3]])
    return cheapest_to_power









