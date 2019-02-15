from flask import session
from controllers.routing import route
from controllers.controller import Controller
from components.rType import RType
import copy
import json

'''
file allowing player to request information about various components of the board
should be only GET requests
'''

class InfoController(Controller):

	def __init__(self, app, service):
		Controller.__init__(self, 'info', __name__)
		self.app = app
		self.game = service

	def get_player_info(self, player_id):
		info = {}
		for player in self.game.players:
			if player.player_id == player_id:
				info["name"] = player.name
				info["money"] = player.money
				info["powerplants"] = []
				plants = player.powerplants
				for plant in plants:
					plant_copy = copy.deepcopy(plant)
					# convert our enum type into a string
					plant_copy["resource_type"] = plant_copy["resource_type"].name
					info["powerplants"].append(plant_copy)
				info["cities"] = self.game.board.cities_owned_by_player(player.player_id)
				resource_copy = {}
				# again change our resource enum into readable string
				for resource in player.resources:
					resource_copy[resource.name] = player.resources[resource]
				info["resources"] = resource_copy
				info["can_bid"] = player.can_bid
		return info
	
	@route("/player_info", methods=['GET'])
	def player_info(self):
		'''
		returns all the information for all the players
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		all_players = []
		for player in self.game.players:
			all_players.append(self.get_player_info(player.player_id))
		return json.dumps({"info": all_players})

	@route("/my_info", methods=['GET'])
	def my_info(self):
		'''
		returns the information for the requesting player
		'''
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		info = self.get_player_info(session['player_id'])
		return json.dumps({"info": info}) 

	@route("/turn_info", methods=['GET'])
	def turn_info(self):
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		if not self.game.auction.auction_in_progress:
			if self.game.current_player == -1:
				# currently re-calculating for BUREAURACY
				current_player = "Calculating..."
			else:
				current_player = self.game.get_player_name(self.game.player_order[self.game.current_player])
		else:
			current_player = self.game.get_player_name(self.game.auction.get_current_bidder())
		current_stage = self.game.phase.name
		return json.dumps({"current_player": current_player, "phase": current_stage, "stage": self.game.step}) 

	@route("/auction", methods=['GET'])
	def auction(self):
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started", "auction_in_progress": False}) 
		if not self.game.auction.auction_in_progress:
			return json.dumps({"auction_in_progress": False})
		else:
			auction_plant = self.game.auction.currently_for_bid
			plant_copy = None
			for plant in self.game.market.currently_available:
				if plant["market_cost"] == auction_plant:
					plant_copy = copy.deepcopy(plant)
					plant_copy["resource_type"] = plant["resource_type"].name
					break
			return json.dumps({"auction_in_progress": True, "current_bid": self.game.auction.current_bid, "powerplant": plant_copy})


	@route("/market", methods=['GET'])
	def market(self):
		'''
		returns the current market, the futures market, and the color of the top card
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		if len(self.game.market.currently_available) == 0:
			return json.dumps({"current_market": []}) 
		current_market = []
		for plant in self.game.market.currently_available:
			plant_copy = copy.deepcopy(plant)
			plant_copy["resource_type"] = plant_copy["resource_type"].name 
			current_market.append(plant_copy)
		if len(self.game.market.deck) == 0:
			top_color = None
		else:
			top_color = self.game.market.deck[0]["type"]
			if top_color == "stage3":
				top_color = "light"
		futures_market = []
		if len(self.game.market.futures_market) > 0:
			for plant in self.game.market.futures_market:
				plant_copy = copy.deepcopy(plant)
				plant_copy["resource_type"] = plant_copy["resource_type"].name 
				futures_market.append(plant_copy)
			return json.dumps({"current_market": current_market, "futures_market": futures_market, "top_color": top_color}) 
		return json.dumps({"current_market": current_market, "top_color": top_color}) 

	@route("/board", methods=['GET'])
	def board(self):
		'''
		returns the mapping of cities to each other and
		their link costs
		list of lists: [ [city_1, city_2, cost_between], [city_1, city_2, cost_between], ... ]
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		return json.dumps(list(self.game.board.board.edges(data='weight')))

	@route("/city_status", methods=['GET'])
	def city_state(self):
		'''
		returns the status of each city 
		{ <cityname> : [list of players who have built there], ... }
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		cities = {}
		for city in self.game.board.board.nodes():
			players = self.game.board.board.node[city]["slots"]
			cities[city] = [self.game.get_player_name(x) for x in players]
		return json.dumps(cities) 

	@route("/resources", methods=['GET'])
	def resources(self):
		'''
		returns the resources available
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		resource_buckets = {
			"COAL": [(9, 2, 0), (8, 2, 0), (7, 2, 0), (6, 3, 0), (5, 3, 0), (4, 3, 0), (3, 4, 0), (2, 4, 0), (1, 4, 0)],
			"GAS": [(8, 3, 0), (7, 3, 0), (6, 3, 0), (5, 3, 0), (4, 3, 0), (3, 4, 0), (2, 4, 0), (1, 4, 0)],
			"OIL": [(9, 4, 0), (8, 2, 0), (7, 2, 0), (6, 2, 0), (5, 2, 0), (4, 2, 0), (3, 2, 0), (2, 2, 0), (1, 2, 0)],
			"URANIUM": [(9, 2, 0), (8, 2, 0), (7, 2, 0), (6, 1, 0), (5, 1, 0), (4, 1, 0), (3, 1, 0), (2, 1, 0), (1, 1, 0)]
		}
		def _fill_bucket(remaining_resources, bucket):
			cost, capacity, _ = bucket
			if capacity > remaining_resources:
				return (cost, capacity, remaining_resources), 0
			else:
				return (cost, capacity, capacity), remaining_resources - capacity
		for r_type in self.game.resources.currently_available:
			remaining_resources = self.game.resources.currently_available[r_type]
			current_bucket_index = 0
			while remaining_resources > 0:
				resource_buckets[r_type.name][current_bucket_index], \
				remaining_resources = _fill_bucket(remaining_resources, resource_buckets[r_type.name][current_bucket_index])
				current_bucket_index += 1

		return json.dumps(resource_buckets)

