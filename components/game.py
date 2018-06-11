'''
manages different components of the game
'''
from market import Market 
from board import Board 
from resources import Resources 
from phase import Phase
import random

class Game:
	'''
	determine player order
	auction power plants (in order)
	buy resources (reverse order!)
	build generators (reverse order!)
	bureaucracy
	'''

	def __init__(self):
		self.market = None
		self.players = []
		self.resources = None
		self.step = 1
		self.phase = Phase.DETERMINE_PLAYER_ORDER
		self.current_player = 0 	# which player's turn it is w.r.t the player_order index
		self.player_order = []

	def get_player_name(self, player_id):
		for player in self.players:
			if player.player_id == player_id:
				return player.name

	def player_can_afford(self, player_id, amount):
		for player in self.players:
			if player.player_id == player_id:
				return (player.money >= amount)

	def add_player(self, name, player_id):
		existing_names = [player.name for player in self.players]
		while name in existing_names:
			name = name + "!" # avoid duplicate names by adding exclamation marks
		player = Player(name, player_id)
		self.players.append(player)
		return name

	def start_game(self):
		'''
		kicks off the game
		'''
		settings = {'board_type': 'europe', 'num_players': len(self.players)}
		self.market = Market(settings)
		self.resources = Resources(settings)
		self.board = Board(settings)
		self.phase_one()

	def next_turn(self):
		'''
		advances the turn/phase
		'''
		if self.current_turn < (len(player_order) -1):
			# we are still in the same phase 
			self.current_player += 1 
		else:
			self.current_player = 0 
			if self.phase == Phase.AUCTION:
				self.player_order.reverse()
				self.phase = Phase.BUY_RESOURCES 
			elif self.phase == Phase.BUY_RESOURCES:
				self.phase == Phase.BUILD_GENERATORS 
			elif self.phase == Phase.BUILD_GENERATORS:
				self.phase = Phase.BUREAUCRACY 
				self.phase_five()

	def phase_one(self):
		'''
		determine player order
		'''
		if self.player_order == []:
			# it's the first round! we randomly choose
			players = [player.player_id for player in self.players]
			random.shuffle(players)
			self.player_order = players 
		else:
			self.player_order = []
			not_yet_picked = [player.player_id for player in self.players]
			while len(self.player_order) != len(self.players):
				top = max(not_yet_picked, key=lambda x: self.board.num_cities(x))
				num_cities = self.board.num_cities(top)
				ties = [player for player in self.players if self.board.num_cities(player.player_id) == top]
				rank = sorted(ties, key=lambda x: x.highest_powerplant(), reverse=True)
				for player in rank:
					self.player_order.append(player.player_id)
					not_yet_picked.remove(player.player_id)
		self.phase = Phase.AUCTION

	def build_generator(self, player_id, path):
		'''
		build a generator in the designated city
		'''
		cost_to_build = self.board.player_purchase(player_id, path)
		for player in self.players:
			if player.player_id == player_id:
				player.money -= cost_to_build
		num_owned_cities = self.board.num_cities(player_id)
		if num_owned_cities >= self.market.currently_available[0]["market_cost"]:
			self.market.trash_low_powerplants(num_owned_cities)

	def phase_five(self):
		'''
		bureaucracy
		'''
		self.phase = Phase.DETERMINE_PLAYER_ORDER
		self.phase_one()