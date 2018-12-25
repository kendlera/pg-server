import requests
import time
import threading
import sys

import auction_helper

server_url = "http://127.0.0.1:5050"


class Player:
    def __init__(self, name=""):
        self.name = name
        response = requests.post(
            server_url + "/register", data={"player_name": name})
        self.player_token = response.cookies

    def is_my_turn(self):
        response = requests.get(server_url + "/turn_info").json()
        player_turn = response.get('current_player')
        if player_turn == self.name:
            return True
        return False

    def do_auction(self):
        market_state = requests.get(server_url + "/market").json()
        my_info = requests.get(server_url + "/my_info",
                               cookies=self.player_token).json()
        all_player_info = requests.get(server_url + "/player_info").json()
        auction_state = requests.get(server_url + "/auction").json()
        auction_helper.main(my_info, market_state, auction_state,
                            all_player_info, self.player_token)
        new_state = requests.get(server_url + '/auction').json()
        print(new_state)

    def do_buy_resources(self):
        pass

    def do_build_generators(self):
        pass

    def do_bureaucracy_phase(self):
        pass

    def do_turn(self):
        # Wait until it's my turn
        while not self.is_my_turn():
            time.sleep(1)
        phase = requests.get(server_url + "/turn_info").json().get('phase')
        if phase == 'AUCTION':
            self.do_auction()
        elif phase == 'BUY_RESOURCES':
            self.do_buy_resources()
        elif phase == 'BUILD_GENERATORS':
            self.do_build_generators()
        elif phase == 'BUREAUCRACY':
            self.do_bureaucracy_phase()
        else:
            print('Unrecognized phase ' + phase)


# Testing
if __name__ == "__main__":
    player_name = sys.argv[1]
    player = Player(player_name)
    while True:
        player.do_turn()
