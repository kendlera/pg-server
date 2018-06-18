import json
from rType import RType

REFILL_RATE = "/Users/akendler/Documents/pg-server/components/data/replenish_rates.json"
RESOURCE_SLOTS = "/Users/akendler/Documents/pg-server/components/data/resource_slots.json"

class Reources:

	def __init__(self, settings):
		self.refresh_rate = self._load_refresh_rate(settings['board_type'], settings['num_players'])
		self.slots = self._load_slots()
		self.currently_available = self._load_resources(settings['board_type'])
		self.total_tokens = resources = {RType.OIL: 20, RType.GAS: 24, RType.COAL: 27, RType.URANIUM: 12}
		self.phase = 1

	def _load_refresh_rate(self, board_type, num_players):
		'''
		loads in a dictionary of the format
		{
		  RType : { phase_int : rate_int, phase_int: rate_int, phase_int: rate_int},
		  ....
		}
		'''
		with open(REFILL_RATE, 'r') as f:
			data = json.load(f)

		rates = data[board_type][str(num_players)]
		processed = {}
		for r_type in rates:
			new_phase_dict = {}
			for phase in rates[r_type]:
				new_phase_dict[int(phase)] = rates[r_type][phase]
			processed[RType(int(r_type))] = new_phase_dict
		return processed

	def _load_slots(self):
		with open(RESOURCE_SLOTS, 'r') as f:
			data = json.load(f)

		new_slots = []
		for slot in data:
			new_capacity = {}
			for r_type in slot:
				new_capacity[RType(int(r_type))] = slot[r_type]
			new_slots.append(new_capacity)
		return new_slots

	def _load_resources(self, board_type):
		if board_type == "europe":
			resources = {RType.OIL: 16, RType.GAS: 18, RType.COAL: 23, RType.URANIUM: 4}
		else:
			resources = {RType.OIL: 14, RType.GAS: 18, RType.COAL: 23, RType.URANIUM: 2}
		return resources

	def cost_to_buy(self, r_type, amount):
		'''
		returns the cost to buy 'amount' of r_type
		returns -1 if not enough resources are available
		'''
		return -1