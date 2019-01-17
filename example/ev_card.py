


def the_best_card(market_state):
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










