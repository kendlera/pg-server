'''
manages different components of the game
'''
from components.player import Player
from components.market import Market 
from components.board import Board 
from components.resources import Resources 
from components.auction import Auction
from components.phase import Phase
from components.rType import RType
import random
import logging
logger = logging.getLogger('game')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

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
		self.auction = Auction()  # since auction doesn't require any player settings, we can initialize it right away
		self.step = 1
		self.phase = Phase.DETERMINE_PLAYER_ORDER
		self.current_player = 0 	# which player's turn it is w.r.t the player_order index
		self.player_order = []
		self.started = False

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
		self.started = True

	def next_turn(self):
		'''
		advances the turn/phase
		'''
		if self.current_player < (len(self.player_order) -1):
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
				# wait to trigger phase_five() until all players have powered
				self.player_order.reverse()
			elif self.phase == Phase.BUREAUCRACY:
				self.phase_five()

	def resolve_turn(self):
		'''
		resolves the current turn due to lack of response from user
		'''
		if self.phase == Phase.AUCTION:
			if self.auction.auction_in_progress:
				current = self.auction.can_bid[self.auction.current_bidder]
			else:
				current = self.player_order[self.current_player]
			self.auction_pass(current)
		elif self.phase == Phase.BUY_RESOURCES or self.phase == Phase.BUILD_GENERATORS:
			self.next_turn()
		elif self.phase == Phase.BUREAUCRACY:
			self.player_powered(self.player_order[self.current_player], 0)

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

	def auction_pass(self, player_id):
		'''
		player_id passed on the current auction 
		'''
		if not self.auction.auction_in_progress:
			# the player is the leader! They can no longer bid
			for player in self.players:
				if player.player_id == player_id:
					player.can_bid = False
			self.next_turn()
		else:
			self.auction.can_bid.remove(player_id)
			if len(self.auction.can_bid) == 1:
				self.auction.auction_in_progress = False
				# someone has won the bid!
				winner = self.auction.can_bid[0]
				for player in self.players:
					if player.player_id == winner:
						player.can_bid = False 
						won_plant = self.market.buy(self.auction.currently_for_bid)
						player.powerplants.append(won_plant)
						player.money -= self.auction.current_bid
						logger.info("{} won the auction! Bought powerplant {} for {} money".format(player.player_name, self.auction.currently_for_bid, self.auction.current_bid))
						if self.auction.to_be_trashed is not None:
							logger.info("{} has too many plants! Trashing powerplant {}".format(player.player_name, self.auction.to_be_trashed))
							player.trash_powerplant(self.auction.to_be_trashed)
						if player.player_id == self.player_order[self.current_player]:
							self.next_turn()
						break
			else:
				self.auction.advance_bid()


	def auction_bid(self, player_id, bid, powerplant, trash_id):
		'''
		player_id submitted 'bid' money for the current auction or
		is starting a new auction
		'''
		if self.auction.auction_in_progress:
			self.auction.current_bid = bid 
			self.auction.winning_bidder = player_id 
			self.auction.to_be_trashed = trash_id
			self.auction.advance_bid()
		else:
			biddable_players = [player.player_id for player in self.players if player.can_bid]
			if len(biddable_players) == 1:
				# special case; there is no auction
				for player in self.players:
					if player.player_id == player_id:
						player.can_bid = False 
						won_plant = self.market.buy(powerplant)
						player.powerplants.append(won_plant)
						player.money -= self.auction.current_bid
						logger.info("{} won the auction! Bought powerplant {} for {} money".format(player.player_name, powerplant, bid))
						if trash_id is not None:
							logger.info("{} has too many plants! Trashing powerplant {}".format(player.player_name, self.auction.to_be_trashed))
							player.trash_powerplant(trash_id)
						self.next_turn()
						return
			else:
				self.auction.can_bid = [player_code for player_code in self.player_order if player_code in biddable_players]
				name = self.get_player_name(player_id)
				self.auction.current_bidder = 1
				logger.info("{} started an auction for powerplant {}".format(name, powerplant))
				self.auction.currently_for_bid = powerplant 
				self.auction.winning_bidder = player_id 
				self.auction.bid = bid 
				self.auction.to_be_trashed = trash_id
				self.auction.auction_in_progress = True

	def buy_resources(self, player_id, r_type, amount):
		cost = self.resources.cost_to_buy(r_type, amount)
		self.resources.currently_available[r_type] -= amount 
		name = self.get_player_name(player_id)
		for player in self.players:
			if player.player_id == player_id:
				player.money -= cost 
				player.resources[r_type] += amount
				logger.info("{} aquired {} of resource type {} for {} money".format(name, amount, r_type, cost))
				return

	def build_generator(self, player_id, path):
		'''
		build a generator in the designated city
		'''
		cost_to_build = self.board.player_purchase(player_id, path)
		for player in self.players:
			if player.player_id == player_id:
				player.money -= cost_to_build
				break
		num_owned_cities = self.board.num_cities(player_id)
		if num_owned_cities >= self.market.currently_available[0]["market_cost"]:
			self.market.trash_low_powerplants(num_owned_cities)

	def plant_powered(self, player_id, plant_id, num_oil):
		'''
		'powers' the given powerplant and returns the amount 
		of energy that was generated
		'''
		for player in self.players:
			if player.player_id == player_id:
				for plant in player.powerplants:
					if plant["market_cost"] == plant_id:
						if plant["resource_type"] == RType.HYBRID:
							needed = plant["resource_cost"]
							needed_gas = needed - num_oil 
							player.resources[RType.OIL] -= num_oil 
							player.resources[RType.GAS] -= needed_gas 
						elif plant["resource_type"] != RType.CLEAN:
							player.resources[plant["resource_type"]] -= plant["resource_cost"]
						return plant["generators"]

	def player_powered(self, player_id, num_powered):
		'''
		player powers generators for money
		'''
		amounts = [10,22,33,44,54,64,73,82,90,98,105,112,118,124,129,134,138,142,145,148,150] 
		for player in self.players:
			if player.player_id == player_id:
				num_cities = self.board.num_cities(player_id)
				amount = amounts[min(num_cities, num_powered)] 
				player.money += amount 
				name = self.get_player_name(player_id)
				logger.info("{} powered {} generators for {} money".format(name, num_powered, amount))
				self.next_turn()
				return amount

	def phase_five(self):
		'''
		bureaucracy
		'''
		# refresh resource market
		owned_resources = {RType.OIL:0, RType.GAS:0, RType.COAL:0, RType.URANIUM:0}
		for player in self.players:
			for resource in player.resources:
				owned_resources[resource] += player.resources[resource]
		self.resources.refresh_market(owned_resources)
		# prune market
		step3 = self.market.bureaucracy()
		if step3:
			self.step = 3
			self.resources.phase = 3
			self.board.phase = 3
		self.phase = Phase.DETERMINE_PLAYER_ORDER
		self.phase_one()