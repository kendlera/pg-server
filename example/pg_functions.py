




def the_best_card(market_state):
    '''takes the current market and calculates an expected value for each card returns card with highest EV'''
    def calc_card_ev():
        #returns a dictionary of expected values of cards
        cards = [['44', 'green', '0', '6'], ['36', 'green', '0', '5'], ['31', 'green', '0', '4'],
                 ['28', 'green', '0', '3'],
                 ['24', 'green', '0', '3'], ['17', 'green', '0', '2'], ['11', 'green', '0', '1'],
                 ['46', 'gas', '2', '7'], ['39', 'gas', '2', '6'], ['34', 'gas', '3', '6'], ['26', 'gas', '1', '4'],
                 ['19', 'gas', '1', '3'], ['16', 'gas', '2', '3'], ['14', 'gas', '1', '2'], ['5', 'gas', '2', '1'],
                 ['40', 'coal', '2', '6'], ['33', 'coal', '3', '6'], ['29', 'coal', '2', '5'], ['27', 'coal', '1', '4'],
                 ['25', 'coal', '2', '5'], ['20', 'coal', '3', '4'], ['15', 'coal', '1', '2'], ['12', 'coal', '2', '2'],
                 ['9', 'coal', '3', '2'], ['7', 'coal', '1', '1'], ['4', 'coal', '2', '1'], ['3', 'coal', '2', '1'],
                 ['42', 'oil', '2', '6'], ['38', 'oil', '3', '6'], ['30', 'oil', '2', '5'], ['23', 'oil', '2', '4'],
                 ['18', 'oil', '2', '3'], ['10', 'oil', '2', '2'], ['6', 'oil', '1', '1'], ['50', 'uranium', '2', '7'],
                 ['37', 'uranium', '2', '6'], ['32', 'uranium', '2', '5'], ['21', 'uranium', '1', '3'],
                 ['13', 'uranium', '1', '2'], ['35', 'hybrid', '2', '5'], ['22', 'hybrid', '3', '5'],
                 ['8', 'hybrid', '2', '3']]

        # weights to resources  should change by game phase
        power_costs = {'green': 0.01, 'uranium': 6, 'coal': 2, 'hybrid': 3, 'gas': 4, 'oil': 5}
        # scale factor kinda worthless
        scale_factor = 5
        ev_cards = {}
        for c in cards:
            # approximation of expected value
            ev = (int(c[0]) + int(power_costs[c[1]]) * int(c[2]) * scale_factor) / int(c[3])
            ev_cards[c[0]] = ev

        return ev_cards

    ev_cards = calc_card_ev()
    cur_mkt_pp = []
    for pp in market_state['current_market']:
        cur_mkt_pp.append(pp['market_cost'])
    cur_mkt_ev = []
    for cp in cur_mkt_pp:
        cur_mkt_ev.append([cp, ev_cards[str(cp)]])
    best_card_ev = max([a[1] for a in cur_mkt_ev])
    for evc in cur_mkt_ev:
        if evc[1] == best_card_ev:
            bc = evc[0]
    return bc

def cur_cheapest_res(my_info, resource_state):
    '''takes my_info and current resources and returns best resource given current powerplants'''
    cur_best = []
    for p in my_info['info']['powerplants']:
        if p['resource_type'] == 'HYBRID':
            if resource_state['GAS'] > resource_state['COAL']:
                type_resource = 'GAS'
            else:
                type_resource = 'OIL'
        else:
            type_resource = p['resource_type']
        print('resource type  ', p['resource_type'])
        cur_best.append([p['market_cost'], p['resource_cost'],type_resource, p['generators'], (p['generators']/how_much_to_buy(resource_state,p['resource_cost'],type_resource))])
    def take_third(elem):
        return elem[4]
    cur_best.sort(key=take_third, reverse=True)
    return cur_best


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
        hypo_resource[h[2]] -= h[1]
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
        return 0.0001
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

def generate_pg_graph(game_board):
    """included countries list:  color, nodes, edges and costs  returns game_graph"""

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

def choose_cheapest_cities(start_board, player, player_token):
    players_cities = []
    for p in all_city_info['info']['name']:
        for c in city_info['info']['name'][p]['cities']:
            players_cities.append(c)
    best_start_cities = ['Rhein-Main', 'Vlaanderen', 'Praha', 'Munchen', 'Berlin', 'Warszawa']
    if len(my_cities) == 0:
        for c in best_start_cities:
            if c not in players_cities:
                return c
    else:
        first_poss_cities_to_gen = []
        second_poss_cities_to_gen = []
        third_poss_cities_to_gen = []

        for c in my_city_info:
            for nc in start_board[c]:
                first_poss_cities_to_gen.append([nc, start_board[c][nc]])
        for nc in first_poss_cities_to_gen:
            for nnc in start_board[nc[0]]:
                second_poss_cities_to_gen.append([nnc, nc[1] + start_board[nc[0]][nnc]])
        for nnc in second_poss_cities_to_gen:
            for nnnc in start_board[nnc[0]]:
                third_poss_cities_to_gen.append([nnnc, nnc[1] + start_board[nnc[0]][nnnc]])

        all_poss_cities = first_poss_cities_to_gen + second_poss_cities_to_gen + third_poss_cities_to_gen
        legal_cities = []

        for c in all_poss_cities:
            if c[0] not in players_cities:
                legal_cities.append(c)

        def second(elem):
            return elem[1]

        legal_cities.sort(key=second)
        return  legal_cities[0][0]

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

def choose_cheapest_cities(start_board, player, player_token):
    my_city_info = requests.get(server_url + "/my_info", cookies=player_token).json()
    my_cities = my_city_info['info']['cities']
    players_cities = []
    all_city_info = requests.get(server_url + "/player_info").json()
    for p in all_city_info['info']:
        for c in p['cities']:
            players_cities.append(c)
    best_start_cities = ['Rhein-Main', 'Vlaanderen', 'Praha', 'Munchen', 'Berlin', 'Warszawa']
    if len(my_cities) == 0:
        for c in best_start_cities:
            if c not in players_cities:
                return [c]
    else:
        first_poss_cities_to_gen = []
        second_poss_cities_to_gen = []
        third_poss_cities_to_gen = []

        for c in my_cities:
            for nc in start_board[c]:
                first_poss_cities_to_gen.append([c, nc, start_board[c][nc]])
        for nc in first_poss_cities_to_gen:
            for nnc in start_board[nc[1]]:
                second_poss_cities_to_gen.append([nc[0], nc[1], nnc, nc[2] + start_board[nc[1]][nnc]])
        for nnc in second_poss_cities_to_gen:
            for nnnc in start_board[nnc[2]]:
                third_poss_cities_to_gen.append([nnc[0], nnc[1], nnc[2], nnnc, nnc[3] + start_board[nnc[2]][nnnc]])


        all_poss_cities = first_poss_cities_to_gen + second_poss_cities_to_gen + third_poss_cities_to_gen
        legal_cities = []

        for c in all_poss_cities:
            if c[-2] not in players_cities:
                legal_cities.append(c)

        def last(elem):
            return elem[-1]

        legal_cities.sort(key=last)
        cost = legal_cities[0].pop(-1)

        return legal_cities[0]


