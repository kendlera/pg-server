import json
from components.rType import RType
import logging
import os
logger = logging.getLogger('resources')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

CURRENT = os.path.dirname(__file__)
REFILL_RATE = os.path.join(CURRENT, "data/replenish_rates.json")
RESOURCE_SLOTS = os.path.join(CURRENT, "data/resource_slots.json")

class Resources:

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
		returns dictionary of 
		{
		  phase_int : { RType : rate_int, RType : rate_int, ...},
		  ....
		}
		'''
		with open(REFILL_RATE, 'r') as f:
			data = json.load(f)

		rates = data[board_type][str(num_players)]
		processed = {1 : {}, 2 : {}, 3 : {}}
		for r_type in rates:
			for phase in rates[r_type]:
				processed[int(phase)].update({RType(int(r_type)): rates[r_type][phase]})
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

	def refresh_market(self, owned_by_players):
		'''
		refills the current market as part of phase 5
		owned_by_players : dictionary of resources curretly owned by game players
		'''
		for r in RType:
			if r == RType.HYBRID or r == RType.CLEAN:
				continue
			amount_refill = self.refresh_rate[self.phase][r]
			self.currently_available[r] += amount_refill
			total_available = self.total_tokens[r] - owned_by_players[r]
			if self.currently_available[r] > total_available:
				can_refill = amount_refill - (self.currently_available[r] - total_available)
				logger.info("Only able to refill {} / {} {}.".format(can_refill, amount_refill, r.name)) 
				self.currently_available[r] = total_available

	def cost_to_buy(self, rtype, num):
		'''
		builds list of the cost of all available resources
		then returns the sum of the cheapest ones
		'''
		if rtype == RType.CLEAN:
			return 0
		available = self.currently_available[rtype]
		if available < num:
			return None		# not enough resources available
		costs = []
		i = len(self.slots) - 1
		while len(costs) < available:
			for x in range(self.slots[i][rtype]): # how many of the resource is in this bucket
				costs.append(i+1)
				if len(costs) == available:
					break
			i -= 1
		return sum(sorted(costs)[:num])