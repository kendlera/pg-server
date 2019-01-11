import requests
import random
import json
import ev_card as ev_card

from constants import SERVER_HOST, SERVER_PORT
server_url = SERVER_HOST + SERVER_PORT


def main(player, market_state, auction_state, all_players_state, player_token):
    my_info = requests.get(server_url + "/my_info", cookies=player_token).json()
    #powerplant_id = market_state.get('current_market')[0].get('market_cost')
    powerplant_id = ev_card.the_best_card(market_state)

    current_bid = auction_state.get('current_bid')
    if auction_state.get('auction_in_progress') == False:
        #bid highest ev PP
        response = bid(player.get('info').get('name'), player_token, powerplant_id, powerplant_id)
    else:
        # Auction is in progress
        powerplant_id = auction_state.get('powerplant').get('market_cost')
        current_bid = auction_state.get('current_bid')
        cur_money = my_info['info']['money']
        # if you have enough money (60% of cash) bid +1
        if current_bid < powerplant_id +3:
            # we will bid one higher
            response = bid(player.get('info').get('name'), player_token, current_bid + 1, powerplant_id)
        else:
            #pass
            response = bid(player.get('info').get('name'), player_token, -1, powerplant_id)


    #print('name = ',my_info['info']['name'], 'money = ', my_info['info']['money'], '   market cost = ', powerplant_id, 'current bid', current_bid)


def bid(player_name, player_token, amt, powerplant_id):
    payload = dict(player_name=player_name, powerplant_id=powerplant_id, bid=amt)
    response = requests.post(server_url + "/bid", data=payload, cookies=player_token).json()
    return response

