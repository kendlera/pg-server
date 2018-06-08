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
		can_decide, msg = self.is_turn(player_id, Phase.BUILD_GENERATORS)
		if not can_decide:
			return False, msg