import networkx as nx 
import logging
import os
import json
import random
from components import DATA_DIR
logger = logging.getLogger('board')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

EDGELIST = os.path.join(DATA_DIR, "map.edgelist")
CITYCOLORS = os.path.join(DATA_DIR, "city_colors.json")
class Board:

	def __init__(self, settings, phase=1):
		'''
		edgelist: path to file where map is stored
		phase: current phase of the game; should always be 1
		'''
		self.board = nx.read_weighted_edgelist(EDGELIST)
		invalid_cities = self._random_choose_play_area(settings['num_players'])
		self._strip_cities(invalid_cities)
		self._initialize_costs()
		self.phase = phase

	def _initialize_costs(self):
		for city in self.board.nodes():
			self.board.node[city]["cost"] = 10
			self.board.node[city]["slots"] = []

	def _strip_cities(self, invalid_cities):
		for city in invalid_cities:
			self.board.remove_node(city)

	def _random_choose_play_area(self, num_players):
		'''
		based on the number of players registered, we chose a 
		subset of cities to play with. The regions must be contiguous! 
		Returns list of cities that we later remove from the board.
		'''
		num_areas = [0, 0, 0, 3, 4, 5, 5][num_players]
		if num_areas == 5:
			# if we need to pick 5, we can also just remove a random 1
			colors = ['brown', 'red', 'purple', 'blue', 'yellow', 'green']
			valid_colors = colors.remove(random.choice(colors))
		else:
			eur_connections = [('brown', 'red'), ('brown', 'purple'),  ('brown', 'yellow'),  ('brown', 'green'),  ('brown', 'orange'), ('purple', 'red'), ('red', 'yellow'), ('yellow', 'blue'), ('yellow', 'green'), ('blue', 'green'), ('orange', 'green')]
			valid_colors = list(random.choice(eur_connections))
			while len(valid_colors) < num_areas:
				# get connections with exactly 1 already chosen color
				candidates = [link for link in eur_connections if (bool(link[0] in valid_colors) ^ bool(link[1] in valid_colors))]
				link = random.choice(candidates)
				if link[0] in valid_colors:
					valid_colors.append(link[1])
				else:
					valid_colors.append(link[0])
		with open(CITYCOLORS, 'r') as colorfile:
			city_colors = json.load(colorfile)
		invalid_cities = []
		for color in city_colors:
			if color not in valid_colors:
				invalid_cities += city_colors[color]
		return invalid_cities

	def cities_owned_by_player(self, player_id):
		'''
		returns a list of cities owned by the player
		'''
		cities = [city for city in self.board.nodes() if player_id in self.board.node[city]["slots"]]
		return cities

	def num_cities(self, player_id):
		'''
		returns the number of cities owned by a player
		'''
		cities = self.cities_owned_by_player(player_id)
		return len(cities)

	def update_cost(self, city):
		purchased = self.board.node[city]
		if purchased["cost"] == 10:
			purchased["cost"] = 15 
		elif purchased["cost"] == 15:
			purchased["cost"] = 20
		elif purchased["cost"] == 20:
			purchased["cost"] = -1 

	def player_purchase(self, player_id, path):
		'''
		allows the player to purchase a slot in the city designated
		'''
		city_name = path[-1]
		purchased = self.board.node[city_name]
		path_cost = self.cost_of_path(path)
		city_cost = self.cost_of_city(city_name)
		purchased["slots"].append(player_id)
		self.update_cost(city_name)
		return path_cost + city_cost

	def player_in_city(self, player_id, city):
		'''
		Returns True if player_id has a generator in city
		'''
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

	def cost_of_city(self, city):
		if city not in self.board.nodes():
			logger.info("{} not valid city name".format(city))
			return -1 
		return self.board.node[city]["cost"]

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
