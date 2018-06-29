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
				plants = player.powerplants
				for plant in plants:
					plant_copy = copy.deepcopy(plant)
					# convert our enum type into a string
					plant_copy["resource_type"] = plant_copy["resource_type"].name
					info["powerplants"] = plant_copy
				info["cities"] = self.game.board.cities_owned_by_player(player.player_id)
				resource_copy = {}
				# again change our resource enum into readable string
				for resource in player.resources:
					resource_copy[resource.name] = player.resources[resource]
				info["resources"] = resource_copy
		return info
	
	@route("/player_info", methods=['GET'])
	def player_info(self):
		'''
		returns all the information for all the players
		'''
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
		info = self.get_player_info(session['player_id'])
		return json.dumps({"info": info}) 

	@route("/turn_info", methods=['GET'])
	def turn_info(self):
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		if not self.game.auction.auction_in_progress:
			current_player = self.game.get_player_name(self.game.player_order[self.game.current_player])
		else:
			current_player = self.game.get_player_name(self.game.auction.get_current_bidder())
		current_stage = self.game.phase.name
		return json.dumps({"current_player": current_player, "phase": current_stage}) 

	@route("/auction", methods=['GET'])
	def auction(self):
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started", "aucion_in_progress": False}) 
		if not self.game.auction.auction_in_progress:
			return json.dumps({"aucion_in_progress": False})
		else:
			auction_plant = self.game.auction.currently_for_bid
			plant_copy = None
			for plant in self.game.market.currently_available:
				if plant["market_cost"] == auction_plant:
					plant_copy = copy.deepcopy(plant)
					plant_copy["resource_type"] = plant_copy["resource_type"].name
					break
			return json.dumps({"aucion_in_progress": True, "current_bid": self.game.auction.current_bid, "powerplant": plant_copy})


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
		return json.dumps(list(self.game.board.board.edges.data('weight')))

	@route("/city_state", methods=['GET'])
	def city_state(self):
		'''
		returns the status of each city 
		{ <cityname> : [list of players who have built there], ... }
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		cities = {}
		for city in self.game.board.board.nodes():
			cities[city] = self.game.board.board.node[city]["slots"]
		return json.dumps(cities) 

	@route("/resources", methods=['GET'])
	def resources(self):
		'''
		returns the resources available
		'''
		if not self.game.started:
			return json.dumps({"msg": "The game has not yet started"})
		resource_bank = {}
		for r_type in self.game.resources.currently_available:
			resource_bank[r_type.name] = self.game.resources.currently_available[r_type]
		return json.dumps(resource_bank)

