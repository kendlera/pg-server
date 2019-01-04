#!/usr/bin/env python3
# file: player.py
# author: Erik Brakke
# description: Sample player to play the game.  It'll probably lose
# but it's a good starting point
import requests
import time
import sys

# Change this to the address of the server you're running against
SERVER_URL = 'http://127.0.0.1:5050'

class Player:
    # Each one of these players will be able to play a full game
    # All logic will just live in here, but feel free to split things out
    # for resuability
    def __init__(self, name):
        if not type or type(name) is not str:
            raise Exception('Name must be supplied as a string')
        self.name = name
        # Register
        response = requests.post(SERVER_URL + "/register", json={'player_name': name})
        if not response.ok:
           raise Exception('Could not register player.  Please try again')
        # Use this to identify which player you are
        self.player_token = response.cookies
    
    def do_turn(self):
        """Check to see if it is player turn and then do the turn"""
        # Wait until it's player turn
        while not self._is_my_turn():
            time.sleep(1)
        phase = requests.get(SERVER_URL + "/turn_info").json()['phase']
        if phase == 'AUCTION':
            self._auction()
        elif phase == 'BUY_RESOURCES':
            self._buy()
        elif phase == 'BUILD_GENERATORS':
            self._build()
        elif phase == 'BUREAUCRAY':
            self._power()
        else:
            raise Exception('Unrecognized phase ' + phase)
    
    def _is_my_turn(self):
        """Check if it is my turn"""
        response = requests.get(SERVER_URL + "/turn_info").json()
        player_turn = response.get('current_player')
        if player_turn == self.name:
            return True
        return False
    
    def _auction(self):
        """Do the auction phase"""
        # Need to know the state of the market
        market_state = requests.get(SERVER_URL + '/market').json()
        my_info = requests.get(SERVER_URL + '/my_info', cookies=self.player_token).json()['info']
        auction_state = requests.get(SERVER_URL + '/auction').json()

        # If no auction is in progress we can start the bidding
        if auction_state['auction_in_progress'] == False:
            # Bid on the cheapest powerplant
            powerplant_id = market_state['current_market'][0]['market_cost']
            payload = {'player_name': self.name, 'powerplant_id': powerplant_id, 'bid': powerplant_id}
            response = requests.post(SERVER_URL + '/bid', json=payload, cookies=self.player_token).json()
            if response.get('status') != 'SUCCESS':
                print('Invalid move')
        # Need to bid on the current powerplant
        else:
            powerplant_id = auction_state['powerplant']['market_cost']
            current_bid = auction_state['current_bid']
            
            # Don't bid 3 over the max of the current market
            max_bid = market_state['current_market'][-1]['market_cost'] + 3
            # workaround since server doesn't support passing on the first bid, so this will just pass
            bid = max_bid if (current_bid > max_bid) else current_bid + 1
            payload = {'player_name': self.name, 'powerplant_id': powerplant_id, 'bid': bid}
            response = requests.post(SERVER_URL + '/bid', json=payload, cookies=self.player_token).json()
            if response.get('status') != 'SUCCESS':
                print('Invalid move')



    def _buy(self):
        """Do the buy phase"""
        # Get info we need
        resources_state = requests.get(SERVER_URL + '/resources').json()
        my_info = requests.get(SERVER_URL + '/my_info', cookies=self.player_token).json()['info']

        # Only buy enough to power 1 generator
        my_powerplants = my_info['powerplants']
        cheapest_plant = sorted(my_powerplants, key=lambda x: x['resource_cost'])[0]
        # If resources type is hybrid, Just buy coal
        resource_to_buy = 'COAL' if cheapest_plant['resource_type'] == 'HYBRID' else cheapest_plant['resource_type'] 
        payload = {'player_name': self.name, resource_to_buy: cheapest_plant['resource_cost']}
        response = requests.post(SERVER_URL + '/buy', json=payload, cookies=self.player_token).json()
        if response.get('status') != 'SUCCESS':
            print('Invalid move')

    def _build(self):
        pass
    def _power(self):
        pass

def start_game(name):
    player = Player(name)
    while True:
        player.do_turn()

if __name__ == "__main__":
    player_name = sys.argv[1]
    start_game(sys.argv[1])