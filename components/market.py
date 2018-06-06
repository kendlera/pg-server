import json
import random
from rType import RType

CARDS_FILE = "/Users/akendler/Documents/pg-server/components/data/powerplants.json"

class Market:
	CURRENT_MARKET_SIZE = 4
	FUTURES_MARKET_SIZE = 5 # should be 4 for North America board
	NUM_DISCARD_LIGHT = {2:5, 3:6, 4:3, 5:0, 6:0}
	NUM_DISCARD_DARK = {2:1, 3:2, 4:1, 5:0, 6:0}

	def __init__(self, settings):
		self.currently_available = []
		self.futures_market = []
		self.deck = None
		self._load_powerplants(settings['num_players'])

	def _load_powerplants(self, num_players):
		with open(CARDS_FILE, 'r') as f:
			plants = json.load(f)

		dark = [card for card in plants if card["type"] == "dark"]
		light = [card for card in plants if card["type"] == "light"]
		# Step 1: set up market
		dealt = []
		for x in range(CURRENT_MARKET_SIZE + FUTURES_MARKET_SIZE):
			idx = random.randint(0, len(dark) - 1)
			dealt.append(dark[idx])
			dark = dark[0:idx] + dark[idx+1:]
		dealt = sorted(dealt, key=lanbda x: x["market_cost"])

		self.currently_available = dealt[0:CURRENT_MARKET_SIZE]
		self.futures_market = dealt[CURRENT_MARKET_SIZE:]
		# Step 2: random removal
		for x in range(NUM_DISCARD_LIGHT[num_players]):
			idx = random.randint(0, len(light) - 1)
			light = light[0:idx] + light[idx+1:]
		for x in range(NUM_DISCARD_DARK[num_players]):
			idx = random.randint(0, len(dark) - 1)
			dark = dark[0:idx] + dark[idx+1:]
		# Step 3: shuffle all cards together
		cards = light + dark 
		random.shuffle(cards)
		# Step 4: place stage 3 'card' at bottom of deck
		stage3 = [{"type": "stage3"}]
		self.deck = cards + stage3

	def buy(self, powerplant_id):
		for plant in range(CURRENT_MARKET_SIZE):
			if self.currently_available[plant]["market_cost"] == powerplant_id:
				self.currently_available = self.currently_available[0:plant] = self.currently_available[plant+1:]
				top_card = self.deck[0]
				if top_card["type"] == "stage3":
					# do something!
					pass
				else:
					self.currently_available.append(top_card)
					self.currently_available = sorted(self.currently_available, key=lambda x: x["market_cost"])




