pg_cities = [["Istanbul", "Ankara", 9.0], ["Istanbul", "Sofia", 13.0], ["Istanbul", "Izmir", 8.0],
             ["Istanbul", "Bucuresti", 13.0], ["Bremen", "Rhein-Main", 9.0], ["Bremen", "Kobenhavn", 12.0],
             ["Bremen", "Vlaanderen", 10.0], ["Bremen", "Randstad", 8.0], ["Bremen", "Berlin", 6.0],
             ["Rhein-Ruhr", "Rhein-Main", 3.0], ["Rhein-Ruhr", "Vlaanderen", 4.0], ["Rhein-Ruhr", "Paris", 10.0],
             ["Rhein-Ruhr", "Stuttgart", 5.0], ["London", "Vlaanderen", 15.0], ["London", "Paris", 16.0],
             ["London", "Randstad", 18.0], ["London", "Birmingham", 4.0], ["Athina", "Tirane", 16.0],
             ["Athina", "Sofia", 17.0], ["Bordeaux", "Barcelona", 15.0], ["Bordeaux", "Lyon", 12.0],
             ["Bordeaux", "Marseille", 12.0], ["Bordeaux", "Paris", 12.0], ["Bordeaux", "Madrid", 16.0],
             ["Zagreb", "Wien", 8.0], ["Zagreb", "Munchen", 14.0], ["Zagreb", "Milano", 17.0],
             ["Zagreb", "Beograd", 9.0], ["Zagreb", "Budapest", 7.0], ["Madrid", "Lisboa", 13.0],
             ["Madrid", "Barcelona", 14.0], ["Birmingham", "Glasgow", 13.0], ["Birmingham", "Dublin", 15.0],
             ["Vlaanderen", "Paris", 7.0], ["Vlaanderen", "Rhein-Main", 6.0], ["Vlaanderen", "Randstad", 4.0],
             ["Praha", "Katowice", 8.0], ["Praha", "Warszawa", 11.0], ["Praha", "Berlin", 7.0],
             ["Praha", "Wien", 7.0], ["Praha", "Rhein-Main", 10.0], ["Praha", "Munchen", 8.0],
             ["Kyjiv", "Kharkiv", 9.0], ["Kyjiv", "Odessa", 9.0], ["Kyjiv", "Warszawa", 14.0],
             ["Kyjiv", "Katowice", 18.0], ["Kyjiv", "Minsk", 10.0], ["Kyjiv", "Budapest", 21.0],
             ["Rhein-Main", "Stuttgart", 3.0], ["Rhein-Main", "Berlin", 10.0], ["Rhein-Main", "Munchen", 6.0],
             ["Milano", "Zurich", 11.0], ["Milano", "Roma", 19.0], ["Milano", "Munchen", 16.0],
             ["Milano", "Marseille", 13.0], ["Milano", "Lyon", 11.0], ["Tirane", "Napoli", 25.0],
             ["Tirane", "Sofia", 13.0], ["Tirane", "Beograd", 15.0], ["Katowice", "Wien", 8.0],
             ["Katowice", "Warszawa", 5.0], ["Katowice", "Budapest", 11.0], ["Berlin", "Warszawa", 11.0],
             ["Berlin", "Kobenhavn", 15.0], ["Tallinn", "Riga", 7.0], ["Tallinn", "Sankt-Peterburg", 9.0],
             ["Riga", "Minsk", 8.0], ["Riga", "Moskwa", 18.0], ["Riga", "Sankt-Peterburg", 13.0],
             ["Riga", "Warszawa", 12.0], ["Munchen", "Zurich", 8.0], ["Munchen", "Stuttgart", 4.0],
             ["Munchen", "Wien", 9.0], ["Warszawa", "Minsk", 10.0], ["Warszawa", "Kobenhavn", 25.0],
             ["Odessa", "Kharkiv", 13.0], ["Odessa", "Bucuresti", 10.0], ["Odessa", "Budapest", 25.0],
             ["Glasgow", "Dublin", 17.0], ["Sofia", "Beograd", 11.0], ["Sofia", "Bucuresti", 9.0],
             ["Stuttgart", "Zurich", 5.0], ["Stuttgart", "Paris", 14.0], ["Izmir", "Ankara", 10.0],
             ["Oslo", "Stockholm", 13.0], ["Oslo", "Kobenhavn", 17.0], ["Kharkiv", "Moskwa", 15.0],
             ["Kharkiv", "Minsk", 16.0], ["Lyon", "Zurich", 14.0], ["Lyon", "Marseille", 8.0],
             ["Lyon", "Paris", 11.0], ["Minsk", "Moskwa", 14.0], ["Budapest", "Bucuresti", 16.0],
             ["Budapest", "Wien", 5.0], ["Budapest", "Beograd", 10.0], ["Beograd", "Bucuresti", 12.0],
             ["Beograd", "Napoli", 18.0], ["Sankt-Peterburg", "Moskwa", 14.0],
             ["Sankt-Peterburg", "Helsinki", 11.0], ["Roma", "Napoli", 7.0], ["Paris", "Zurich", 14.0],
             ["Helsinki", "Stockholm", 21.0], ["Kobenhavn", "Stockholm", 18.0], ["Marseille", "Barcelona", 11.0]]

my_info = {
    "info": {
        "name": "player_two",
        "money": 26.0,
        "cities": [
            "Rhein-Main",
            "Stuttgart",
            "Rhein-Ruhr"
        ],
        "powerplants": [
            {
                "generators": 5,
                "market_cost": 22,
                "type": "light",
                "resource_type": "HYBRID",
                "resource_cost": 3
            },
            {
                "generators": 3,
                "market_cost": 24,
                "type": "light",
                "resource_type": "CLEAN",
                "resource_cost": 0
            },
            {
                "generators": 5,
                "market_cost": 30,
                "type": "light",
                "resource_type": "OIL",
                "resource_cost": 2
            }
        ],
        "resources": {
            "COAL": 0,
            "OIL": 2,
            "URANIUM": 0,
            "GAS": 2
        }
    }
}

resource_state = {'GAS': 11, 'OIL': 7, 'COAL': 15, 'URANIUM': 5}

market_state = {'current_market': [{'resource_cost': 0, 'market_cost': 17, 'resource_type': 'CLEAN', 'generators': 2, 'type': 'light'}, {'resource_cost': 0, 'market_cost': 24, 'resource_type': 'CLEAN', 'generators': 3, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 25, 'resource_type': 'COAL', 'generators': 5, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 25, 'resource_type': 'COAL', 'generators': 5, 'type': 'light'}], 'top_color': 'light',
                'futures_market': [{'resource_cost': 1, 'market_cost': 27, 'resource_type': 'COAL', 'generators': 4, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 30, 'resource_type': 'OIL', 'generators': 5, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 32, 'resource_type': 'URANIUM', 'generators': 5, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 40, 'resource_type': 'COAL', 'generators': 6, 'type': 'light'}, {'resource_cost': 2, 'market_cost': 40, 'resource_type': 'COAL', 'generators': 6, 'type': 'light'}]}
#print(len(market_state['futures_market']))

city_occupied = {'Kyjiv': [], 'Milano': ['player_one'], 'London': [], 'Praha': ['player_two'], 'Ankara': [], 'Kobenhavn': [], 'Bucuresti': [], 'Oslo': [], 'Rhein-Main': ['player_one'], 'Tirane': [], 'Lyon': ['player_three'], 'Istanbul': [], 'Randstad': ['player_three'], 'Minsk': [], 'Zagreb': [], 'Roma': [], 'Budapest': ['player_two'], 'Marseille': [], 'Stuttgart': ['player_one'], 'Beograd': [], 'Paris': ['player_three'], 'Kharkiv': [], 'Sofia': [], 'Birmingham': [], 'Napoli': [], 'Moskwa': [], 'Warszawa': [], 'Lisboa': [], 'Glasgow': [], 'Munchen': ['player_one'], 'Odessa': [], 'Berlin': ['player_two'], 'Helsinki': [], 'Wien': ['player_two'], 'Stockholm': [], 'Barcelona': [], 'Athina': [], 'Riga': [], 'Zurich': ['player_one'], 'Bordeaux': [], 'Sankt-Peterburg': [], 'Tallinn': [], 'Rhein-Ruhr': ['player_three'], 'Bremen': ['player_two'], 'Madrid': [], 'Vlaanderen': ['player_three'], 'Izmir': [], 'Dublin': [], 'Katowice': []}

all_player_info = {
    "info": [
        {
            "resources": {
                "OIL": 0,
                "GAS": 0,
                "COAL": 1,
                "URANIUM": 0
            },
            "powerplants": [
                {
                    "type": "dark",
                    "market_cost": 4,
                    "resource_type": "COAL",
                    "resource_cost": 2,
                    "generators": 1
                },
                {
                    "type": "dark",
                    "market_cost": 7,
                    "resource_type": "COAL",
                    "resource_cost": 1,
                    "generators": 1
                },
                {
                    "type": "light",
                    "market_cost": 18,
                    "resource_type": "OIL",
                    "resource_cost": 2,
                    "generators": 3
                }
            ],
            "money": 48.0,
            "name": "player_one",
            "cities": [
                "Berlin",
                "Bremen",
                "Praha"
            ]
        },
        {
            "resources": {
                "OIL": 0,
                "GAS": 1,
                "COAL": 0,
                "URANIUM": 0
            },
            "powerplants": [
                {
                    "type": "dark",
                    "market_cost": 5,
                    "resource_type": "GAS",
                    "resource_cost": 2,
                    "generators": 1
                },
                {
                    "type": "dark",
                    "market_cost": 14,
                    "resource_type": "GAS",
                    "resource_cost": 1,
                    "generators": 2
                },
                {
                    "type": "dark",
                    "market_cost": 12,
                    "resource_type": "COAL",
                    "resource_cost": 2,
                    "generators": 2
                },
                {
                    "type": "light",
                    "market_cost": 20,
                    "resource_type": "COAL",
                    "resource_cost": 3,
                    "generators": 4
                }
            ],
            "money": 32.0,
            "name": "player_two",
            "cities": [
                "Stuttgart",
                "Rhein-Main",
                "Munchen"
            ]
        },
        {
            "resources": {
                "OIL": 0,
                "GAS": 0,
                "COAL": 0,
                "URANIUM": 0
            },
            "powerplants": [
                {
                    "type": "dark",
                    "market_cost": 13,
                    "resource_type": "URANIUM",
                    "resource_cost": 1,
                    "generators": 2
                },
                {
                    "type": "light",
                    "market_cost": 19,
                    "resource_type": "GAS",
                    "resource_cost": 1,
                    "generators": 3
                },
                {
                    "type": "dark",
                    "market_cost": 15,
                    "resource_type": "COAL",
                    "resource_cost": 1,
                    "generators": 2
                }
            ],
            "money": 37.0,
            "name": "player_three",
            "cities": [
                "Rhein-Ruhr",
                "Vlaanderen",
                "Randstad"
            ]
        }
    ]
}


def how_much_to_buy(resource_state, to_buy, what):
    '''given current resource state answers the question, how much to buy 7 oil'''
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


# print(how_much_to_buy(resource_state, 4, 'COAL'))
# print(how_much_to_buy(resource_state, 24, 'COAL'))
# print(how_much_to_buy(resource_state, 4, 'CLEAN'))


def cur_cheapest_res(my_info, resource_state):
    '''returns sorted list of generators cheapest to most expensive to power'''
    cur_best = []
    for p in my_info['info']['powerplants']:
        if p['resource_type'] == 'HYBRID':
            gas_cost = [p['market_cost'], p['resource_cost'],'GAS', p['generators'], (p['generators']/(how_much_to_buy(resource_state,p['resource_cost'],'GAS')+.0001))]
            oil_cost = [p['market_cost'], p['resource_cost'], 'OIL', p['generators'], (p['generators'] / (how_much_to_buy(resource_state, p['resource_cost'], 'OIL') + .0001))]
            if gas_cost >= oil_cost:
                cur_best.append(oil_cost)
            else:
                cur_best.append(gas_cost)
        else:
            cur_best.append([p['market_cost'], p['resource_cost'],p['resource_type'], p['generators'], (p['generators']/(how_much_to_buy(resource_state,p['resource_cost'],p['resource_type'])+.0001))])
    def take_third(elem):
        return elem[4]
    cur_best.sort(key=take_third, reverse=True)
    return  cur_best

#print(cur_cheapest_res(my_info, resource_state))


def the_best_card(market_state):
    '''takes the current market and calculates an expected value for each card returns card with highest EV single int()'''
    def calc_card_ev():
        #returns a dictionary of expected values of cards
        cards = [['44', 'green', '0', '6'], ['36', 'green', '0', '5'], ['31', 'green', '0', '4'],['28', 'green', '0', '3'],
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

#print(the_best_card(market_state))

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
        elif h[2] == 'CLEAN':
            cheapest_to_power.append([h[0], h[2], h[1], 0, h[3]])
        if h[2] != 'CLEAN':
            cost = how_much_to_buy(hypo_resource, h[1], h[2])
            hypo_resource[h[2]] -= h[1]
            cheapest_to_power.append([h[0], h[2], h[1], cost, h[3]])
    return cheapest_to_power


#print(best_poss_res(my_info, resource_state))


def how_much_to_buy(resource_state, to_buy, what):
    '''given current resource state answers the question, how much to buy 7 oil'''
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


# print(how_much_to_buy(resource_state, 4, 'COAL'))
# print(how_much_to_buy(resource_state, 24, 'COAL'))
# print(how_much_to_buy(resource_state, 4, 'CLEAN'))


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

start_board = generate_pg_graph(pg_cities)

def choose_cheapest_cities(start_board, my_info, all_player_info):
    '''returns a payload with cheapest start and ending city.  if no cities then chooses from list of 6 good cities'''
    players_cities = []
    my_cities = [c for c in my_info['info']['cities']]
    for p in all_player_info['info']:
        for c in p['cities']:
            if c not in players_cities:
                players_cities.append(c)
    best_start_cities = ['Rhein-Main', 'Vlaanderen', 'Praha', 'Munchen', 'Berlin', 'Warszawa']
    if len(my_info['info']['cities']) == 0:
        for c in best_start_cities:
            if c not in players_cities:
                return c
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
        #print(legal_cities)
        #cost = legal_cities[2]
        #total_cost = cost + 10
        #return legal_cities[:20]

print(choose_cheapest_cities(start_board, my_info, all_player_info))

def cur_cheapest_res(my_info, resource_state):
    '''returns sorted list of generators cheapest to most expensive to power'''
    cur_best = []
    for p in my_info['info']['powerplants']:
        if p['resource_type'] == 'HYBRID':
            gas_cost = [p['market_cost'], p['resource_cost'],'GAS', p['generators'], (p['generators']/(how_much_to_buy(resource_state,p['resource_cost'],'GAS')+.0001))]
            oil_cost = [p['market_cost'], p['resource_cost'], 'OIL', p['generators'], (p['generators'] / (how_much_to_buy(resource_state, p['resource_cost'], 'OIL') + .0001))]
            if gas_cost >= oil_cost:
                cur_best.append(oil_cost)
            else:
                cur_best.append(gas_cost)
        else:
            cur_best.append([p['market_cost'], p['resource_cost'],p['resource_type'], p['generators'], (p['generators']/(how_much_to_buy(resource_state,p['resource_cost'],p['resource_type'])+.0001))])
    def take_third(elem):
        return elem[4]
    cur_best.sort(key=take_third, reverse=True)
    return  cur_best

#print(cur_cheapest_res(my_info, resource_state))




