import requests
import random

server_url = 'http://127.0.0.1:5050'


def main(player, market_state, auction_state, all_players_state, player_token):
    if auction_state.get('auction_in_progress') == False:
        # Bid of new powerplant
        powerplant_id = market_state.get('current_market')[
            0].get('market_cost')
        response = bid(player.get('info').get('name'),
                       player_token, powerplant_id, powerplant_id)
        if response.get('status') != 'SUCCESS':
            print(response.get('msg'))
    else:
        # Auction is in progress
        powerplant_id = auction_state.get('powerplant').get('market_cost')
        current_bid = auction_state.get('current_bid')

        # 30% chance player will bid 1 higher
        if random.random() < .3:
            # we will bid one higher
            response = bid(player.get('info').get('name'),
                           player_token, current_bid + 1, powerplant_id)
            if response.get('status') != 'SUCCESS':
                print(response.get('msg'))
        else:
            if len(player.get('info').get('powerplants')) == 0:
                # Can't pass on the bid
                return
            # Pass on the bid if you don't have a powerplant
            response = bid(player.get('info').get('name'),
                           player_token, -1, powerplant_id)


def bid(player_name, player_token, amt, powerplant_id):
    payload = dict(player_name=player_name,
                   powerplant_id=powerplant_id, bid=amt)
    response = requests.post(
        server_url + "/bid", data=payload, cookies=player_token).json()
    return response
