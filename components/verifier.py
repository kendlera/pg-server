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
		if self.game.player_order.index(player_id) != self.game.current_player:
			name = self.game.get_player_name(self.game.player_order[self.game.current_player])
			return False, "It is not your turn. {}'s turn to go".format(name)
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