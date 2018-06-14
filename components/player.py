from rType import RType

class Player:

	def __init__(self, player_name, player_id, money=50):
		self.player_name = player_name
		self.player_id = player_id
		self.money = money
		self.powerplants = []
		self.resources = {RType.GAS : 0, RType.URANIUM : 0, RType.OIL : 0, RType.COAL : 0}
		self.can_bid = True 	# determines if a player can bid on auctions for the round

	def highest_powerplant(self):
		'''
		used to determine player order
		'''
		max_plant = max(self.powerplants, key=lambda x: x["market_cost"])
		return max_plant["market_cost"]

	def trash_powerplant(self, trash_id):
		for plant in range(len(self.powerplants)):
			if self.powerplants[plant]["market_cost"] == trash_id:
				self.powerplants = self.powerplants[:plant] + self.powerplants[plant+1:]
				return
