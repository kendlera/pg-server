import requests
import time
import threading
import sys
import os
import json

import auction_helper as AH
import buy_resource_helper as RH
import build_generator_helper as GH
import bureaucracy_helper as BH
from constants import SERVER_HOST, SERVER_PORT

server_url = SERVER_HOST + SERVER_PORT


class Player:
    def __init__(self, name=""):
        self.name = name
        response = requests.post(server_url + "/register", data={"player_name": name})
        self.player_token = response.cookies

    def is_my_turn(self):
        response = requests.get(server_url + "/turn_info").json()
        player_turn = response.get('current_player')
        print(player_turn)
        if player_turn == self.name:
            return True
        return False

    def do_auction(self):
        print("im in the auction")
        market_state = requests.get(server_url + "/market").json()
        #print(json.dumps(market_state, indent=4))
        my_info = requests.get(server_url + "/my_info", cookies=self.player_token).json()
        all_player_info = requests.get(server_url + "/player_info").json()
        auction_state = requests.get(server_url + "/auction").json()
        AH.main(my_info, market_state, auction_state, all_player_info, self.player_token)




    def do_buy_resources(self):
        print("im in the buy resource")
        resource_state = requests.get(server_url + "/resources").json()
        #print(json.dumps(resource_state))
        my_info = requests.get(server_url + "/my_info", cookies=self.player_token).json()
        #all_player_info = requests.get(server_url + "/player_info").json()
        RH.main(player, my_info, self.player_token)
        #new_state = requests.get(server_url + '/resources').json()



    def do_build_generators(self):
        print('im building generators')
        my_info = requests.get(server_url + "/my_info", cookies=self.player_token).json()
        all_player_info = requests.get(server_url + "/player_info").json()
        GH.main(player, my_info, self.player_token)

    def do_bureaucracy_phase(self):
        print('do bureaucracy')
        my_info = requests.get(server_url + "/my_info", cookies=self.player_token).json()
        all_player_info = requests.get(server_url + "/player_info").json()
        BH.main(player, my_info, self.player_token)


    def do_turn(self):
        # Wait until it's my turn
        while not self.is_my_turn():
            time.sleep(1)
        phase = requests.get(server_url + "/turn_info").json().get('phase')
        print(phase)
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


def try_connect(MAX_RETRIES=5):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            requests.get(server_url + '/turn_info')
            break
        except requests.exceptions.ConnectionError as e:
            time.sleep(5)
            print('Retrying connection...')
            retries += 1


# Testing
if __name__ == "__main__":
    #customize here
    player_name = sys.argv[1]
    try_connect()
    player = Player(player_name)
    while True:
        player.do_turn()
