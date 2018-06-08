import networkx as nx 

EDGELIST = "/Users/akendler/Documents/pg-server/components/data/map_costs.edgelist"
class Board:

	def __init__(self, phase=1):
		'''
		edgelist: path to file where map is stored
		phase: current phase of the game; should always be 1
		'''
		if edgelist is None:
			edgelist = EDGELIST
		self.board = nx.read_weighted_edgelist(edgelist)
		self._initialize_costs()
		self.phase = phase

	def _initialize_costs(self):
		for city in self.board.nodes():
			self.board.node[city]["cost"] = 10
			self.board.node[city]["slots"] = []


	def num_cities(self, player_id):
		count = 0
		for city in self.board.nodes():
			if player_id in self.board.node[city]['slots']:
				count += 1
		return count

	def player_in_city(self, player_id, city):
		if city not in self.board.nodes():
			return False, "{} not a valid city name".format(city)
		slots = self.board.node[city]["slots"]
		if player_id in slots:
			return True, "{} in {}".format(player_id, city)
		else:
			return False, "{} not in {}".format(player_id, city)

	def can_build(self, player_id, city):
		'''
		Determines if player_id can build in city
		'''
		if city not in self.board.nodes():
			return False, "{} not valid city name".format(city)
		slots = self.board.node[city]["slots"]
		if len(slots) >= self.phase:
			return False, "{} already has {} generators built".format(city, len(slots))
		if player_id in slots:
			return False, "{} has already built in {}".format(player_id, city) 
		return True, "{} can build in {}".format(player_id, city)

	def cost_of_path(self, path):
		'''
		given a list of city names returns the cost to travel
		if the path is invalid, returns -1
		'''
		total_cost = 0
		for step in range(len(path) - 1):
			if path[step] not in self.board.nodes():
				logger.info("{} not valid city".format(path[step]))
				return -1
			if path[step+1] in self.board.neighbors(path[step]):
				# add cost
				cost = self.board[path[step]][path[step+1]]['weight']
				total_cost += cost
			else:
				logger.info("{} and {} are not connected!".format(path[step], path[step+1]))
				return -1
		return total_cost
