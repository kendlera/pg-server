'''
determines if the request being made is valid
rule enforcer
'''
from phase import Phase

class Verifier:
	def __init__(self, game):
		self.game = game

	def is_turn(self, player_id, phase_num):
		if self.game.phase != phase_num:
			return False, "Wrong phase! Currently in phase {}".format(self.game.phase)
		# auctions are a special case; it might be someone's turn who is not the lead bidder
		if self.game.phase == Phase.AUCTION:
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

	def is_valid_bid(self, player_id, powerplant_id, bid, trash_id):
		if self.game.auction.auction_in_progress:
			if powerplant_id != self.game.auction.currently_for_bid:
				return False, "You must bid on current powerplant {}".format(self.game.auction.currently_for_bid)
			if bid <= self.game.auction.current_bid:
				return False, "Your bid must be greater than current bid of {}".format(self.game.auction.current_bid)
			if trash_id is not None:
				for player in self.game.players:
					if player.player_id == player_id:
						for powerplant in player.powerplants:
							if powerplant["market_cost"] == trash_id:
								return True, ""
						return False, "You do not own powerplant {}! Submit a valid plant to trash.".format(trash_id)
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
			if trash_id is not None:
				for player in self.game.players:
					if player.player_id == player_id:
						for powerplant in player.powerplants:
							if powerplant["market_cost"] == trash_id:
								return True, ""
						return False, "You do not own powerplant {}! Submit a valid plant to trash.".format(trash_id)
			return True, ""

	def is_valid_build(self, player_id, path):
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
		return False, "{} cost to build is more than player has to spend".format(cost_to_build+cost_of_path)