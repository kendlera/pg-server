import json
import random
import os
from components.rType import RType
from components import DATA_DIR
import logging
logger = logging.getLogger('market')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

CARDS_FILE = os.path.join(DATA_DIR, "powerplants.json")
CURRENT_MARKET_SIZE = 4
FUTURES_MARKET_SIZE = 5 # should be 4 for North America board
NUM_DISCARD_LIGHT = {2:5, 3:6, 4:3, 5:0, 6:0}
NUM_DISCARD_DARK = {2:1, 3:2, 4:1, 5:0, 6:0}

class Market:

	def __init__(self, settings):
		self.currently_available = []
		self.futures_market = []
		self.deck = None
		self.phase = 1
		self.flag_3 = False 	# a flag so we know to switch to phase 3 in bureaucracy
		self._load_powerplants(settings['num_players'])
		self.starting_bidder = None

	def _load_powerplants(self, num_players):
		with open(CARDS_FILE, 'r') as f:
			plants = json.load(f)
		for card in plants:
			card["resource_type"] = RType(card["resource_type"])
		dark = [card for card in plants if card["type"] == "dark"]
		light = [card for card in plants if card["type"] == "light"]

		# Step 1: set up market
		dealt = []
		for x in range(CURRENT_MARKET_SIZE + FUTURES_MARKET_SIZE):
			idx = random.randint(0, len(dark) - 1)
			dealt.append(dark[idx])
			dark = dark[0:idx] + dark[idx+1:]
		self._sort_market(dealt)

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

	def _sort_market(self, powerplants):
		market = sorted(powerplants, key=lambda x: x["market_cost"])
		self.currently_available = market[:CURRENT_MARKET_SIZE]
		self.futures_market = market[CURRENT_MARKET_SIZE:]
		logger.info("Current Market: {}".format([plant["market_cost"] for plant in self.currently_available]))
		logger.info("Future Market: {}".format([plant["market_cost"] for plant in self.futures_market]))

	def update_phase(self, num):
		self.phase = num
		global FUTURES_MARKET_SIZE
		global CURRENT_MARKET_SIZE
		if num == 2:
			FUTURES_MARKET_SIZE = 4
			self.currently_available = self.currently_available[1:]
			self._sort_market(self.currently_available + self.futures_market)
		elif num == 3:
			FUTURES_MARKET_SIZE = 0
			CURRENT_MARKET_SIZE = 6
			self.currently_available = self.currently_available[1:]
			random.shuffle(deck)
			self._sort_market(self.currently_available + self.futures_market)

	def trash_low_powerplants(self, max_cities):
		'''
		removes any powerplants with a market cost lower than 
		the highest number of owned cities
		'''
		if len(self.currently_available) == 0:
			# empty market!
			return
		while self.currently_available[0]["market_cost"] <= max_cities:
			self.currently_available = self.currently_available[1:]
			if len(self.deck) == 0:
				# no more cards!
				continue
			top_card = self.deck[0]
			self.deck[1:]
			if top_card["type"] == "stage3":
				if self.phase == 1:
					# resolve stage 2
					self.currently_available = self.currently_available[1:]
					self.update_phase(2)
					self._sort_market(self.currently_available + self.futures_market)
				self.currently_available = self.currently_available[1:]
				self.update_phase(3)
				random.shuffle(self.deck)
				self._sort_market(self.currently_available + self.futures_market)
			else:
				self._sort_market(self.currently_available + self.futures_market + [top_card])


	def bureaucracy(self):
		'''
		performs the bureaucracy phase for the market 
		returns True if phase 3 was triggered.
		'''
		if self.phase < 3 and not self.flag_3:
			highest_card = self.futures_market[-1]
			self.futures_market = self.futures_market[:-1]
			self.deck.append(highest_card)
			top_card = self.deck[0]
			if top_card["type"] == "stage3":
				if self.phase == 1:
					# resolve phase 2
					self.update_phase(2)
				self.update_phase(3)
				self._sort_market(self.currently_available + self.futures_market)
				return True
			else:
				self._sort_market(self.currently_available + self.futures_market + [top_card])
				return False
		elif self.flag_3:
			self.update_phase(3)
			self.flag_3 = False
			self.currently_available = self.currently_available[1:]
			self._sort_market(self.currently_available + self.futures_market)
			return True
		else:
			# phase 3
			# discard lowest powerplant
			self.currently_available = self.currently_available[1:]
			if len(self.deck) > 0:
				top_card = self.deck[0]
				self.deck = self.deck[1:]
				self._sort_market(self.currently_available + [top_card])
			return False

	def buy(self, powerplant_id):
		for plant in range(CURRENT_MARKET_SIZE):
			if self.currently_available[plant]["market_cost"] == powerplant_id:
				bought_plant = self.currently_available[plant]
				self.currently_available = self.currently_available[0:plant] + self.currently_available[plant+1:]
				top_card = self.deck[0]
				self.deck = self.deck[1:]
				if top_card["type"] == "stage3":
					if self.phase == 1:
						self.update_phase(2)
					random.shuffle(self.deck)
					self.flag_3 = True
				else:
					self._sort_market(self.currently_available + self.futures_market + [top_card])
				return bought_plant





