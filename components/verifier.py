'''
determines if the request being made is valid
rule enforcer
'''
from components.phase import Phase
from components.rType import RType

class Verifier:
	def __init__(self, game):
		self.game = game

	def is_turn(self, player_id, phase_num):
		if self.game.phase != phase_num:
			return False, "Wrong phase! Currently in phase {}".format(self.game.phase)
		# auctions are a special case; it might be someone's turn who is not the lead bidder
		if self.game.phase == Phase.AUCTION and self.game.auction.auction_in_progress:
			if self.game.auction.can_bid[self.game.auction.current_bidder] != player_id:
				name = self.game.get_player_name(self.game.auction.can_bid[self.game.auction.current_bidder])
				return False, "It is not your turn! {}'s turn to bid".format(name)
			else:
				return True, ""
		if self.game.player_order.index(player_id) != self.game.current_player:
			name = self.game.get_player_name(self.game.player_order[self.game.current_player])
			return False, "It is not your turn. {}'s turn to go".format(name)
		return True, ""

	def player_has_3_plants(self, player_id):
		for player in self.game.players:
			if player.player_id == player_id:
				return (len(player.powerplants) == 3)

	def player_can_pass(self, player_id):
		for player in self.game.players:
			if player.player_id == player_id:
				return (len(player.powerplants) > 0)

	def is_valid_bid(self, player_id, powerplant_id, bid, trash_id):
		for player in self.game.players:
			if player.player_id == player_id:
				if bid > player.money:
					return False, "You cannot make bid of {}; you have {} money".format(bid, player.money)
				else:
					break
		if trash_id is not None:
			owned, found = [False, False]
			for player in self.game.players:
				if player.player_id == player_id:
					found = True 
					for powerplant in player.powerplants:
						if powerplant["market_cost"] == trash_id:
							owned = True
							break
				if found:
					break
			if not owned:
				return False, "You do not own powerplant {}! Submit a valid plant to trash.".format(trash_id)
		if self.game.auction.auction_in_progress:
			if powerplant_id != self.game.auction.currently_for_bid:
				return False, "You must bid on current powerplant {}".format(self.game.auction.currently_for_bid)
			if bid <= self.game.auction.current_bid:
				return False, "Your bid must be greater than current bid of {}".format(self.game.auction.current_bid)
			return True, ""
		else:
			in_market = False
			for plant in self.game.market.currently_available:
				if plant["market_cost"] == powerplant_id:
					in_market = True
					break
			if not in_market:
				return False, "Powerplant {} is not in current market".format(powerplant_id)
			if bid < powerplant_id:
				return False, "Bid is {} and must be at least {}".format(bid, powerplant_id)
			return True, ""

	def can_buy_resources(self, player_id, r_type, amount):
		'''
		returns True if the player can perform this action 
				str indicating errors
				int indicating how many resources the player can buy
		'''
		available = self.game.resources.currently_available[r_type]
		if available == 0:
			return False, "There are no resources of this type available", 0
		for player in self.game.players:
			if player.player_id == player_id:
				can_hold = player.additional_amount_can_hold(r_type)
		num_can_buy = 0
		while num_can_buy < amount and num_can_buy < available and num_can_buy < can_hold:
			cost = self.game.resources.cost_to_buy(r_type, num_can_buy+1)
			if self.game.player_can_afford(player_id, cost):
				num_can_buy += 1
			else:
				return False, "Player can only afford {} resources even though requested {}".format(num_can_buy, amount), num_can_buy
		if num_can_buy == amount:
			return True, "", amount 
		elif num_can_buy == available:
			return False, "Only {} of this resource is available!".format(available), available
		elif num_can_buy == can_hold:
			return False, "Player can only hold {} more resources on current powerplants".format(can_hold), can_hold

	def is_valid_build(self, player_id, path):
		if self.game.board.num_cities(player_id) == 0:
			return self.game.board.can_build(player_id, path[0])
		in_city, msg = self.game.board.player_in_city(player_id, path[0])
		if not in_city:
			return False, msg 
		cost_of_path = self.game.board.cost_of_path(path)
		if cost_of_path == -1:
			return False, "Invalid 'path'"
		can_build, msg = self.game.board.can_build(player_id, path[-1])
		if not can_build:
			return False, msg
		cost_to_build = self.game.board.cost_of_city(path[-1])
		if self.game.player_can_afford(player_id, cost_to_build + cost_of_path):
			return True, ""
		for player in self.game.players:
			if player.player_id == player_id:
				return False, "{} cost to build is more than player has; currently {} money".format(cost_to_build+cost_of_path, player.money)

	def plants_are_hybrid(self, player_id, powerplants):
		'''
		returns true if any of the submitted powerplants are hybrid type plants
		'''
		for player in self.game.players:
			if player.player_id == player_id:
				for plant in player.powerplants:
					if plant["resource_type"] == RType.HYBRID and plant["market_cost"] in powerplants:
						return True 
				return False

	def player_can_power(self, player_id, powerplant_id, num_oil):
		'''
		returns True if player_id has the resources to power the indicated powerplant
		'''
		for player in self.game.players:
			if player.player_id == player_id:
				for plant in player.powerplants:
					if plant["market_cost"] == powerplant_id:
						if plant["resource_type"] == RType.CLEAN:
							return True, "", num_oil
						elif plant["resource_type"] == RType.HYBRID:
							needed = plant["resource_cost"]
							if num_oil >= needed:
								needed_gas = 0 
								remaining_oil = num_oil - needed
								needed_oil = needed
							else:
								needed_gas = needed - num_oil
								remaining_oil = 0
							if player.resources[RType.OIL] < needed_oil or player.resources[RType.GAS] < needed_gas:
								return False, "Need {} oil and {} gas!".format(needed_oil, needed_gas), num_oil 
							return True, "", remaining_oil
						else:
							if player.resources[plant["resource_type"]] < plant["resource_cost"]:
								return False, "You do not have enough resources to power!", num_oil 
							else:
								return True, "", num_oil
				return False, "You do not own powerplant {}".format(powerplant_id), num_oil



