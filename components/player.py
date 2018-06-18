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

	def additional_amount_can_hold(self, r_type):
		'''
		returns amount of additional r_type player could hold RIGHT NOW
		'''
		if r_type == RType.OIL or r_type == RType.GAS:
			num_oil_can_hold = 0
			num_gas_can_hold = 0
			num_hybrid_slots = 0
			for plant in self.powerplants:
				if plant["resource_type"] == RType.GAS:
					num_gas_can_hold += (2 * plant["resource_cost"])
				elif plant["resource_type"] == RType.OIL:
					num_oil_can_hold += (2 * plant["resource_cost"])
				elif plant["resource_type"] == RType.HYBRID:
					num_hybrid_can_hold += (2 * plant["resource_cost"])
			if r_type == RType.GAS:
				if num_oil_can_hold <= self.resources[RType.OIL]:
					num_hybrid_can_hold -= (self.resources[RType.OIL] - num_oil_can_hold)
				return num_hybrid_can_hold + num_gas_can_hold - self.resources[RType.GAS]
			else:
				if num_gas_can_hold <= self.resources[RType.GAS]:
					num_hybrid_can_hold -= (self.resources[RType.GAS] - num_gas_can_hold)
				return num_hybrid_can_hold + num_oil_can_hold - self.resources[RType.OIL]
		else:
			num = 0
			for plant in self.powerplants:
				if plant["resource_type"] == r_type:
					num += (2 * plant["resource_cost"])
			return num - self.resources[r_type]
