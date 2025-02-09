from controllers.routing import route
from controllers.controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session
from components.phase import Phase
from components.rType import RType
import uuid
import json
import threading
import logging

# Set up root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('pg_server.PlayController')
TIMEOUT_VALUE = 20 # how many seconds each player gets to make a decision
'''
manages player action requests
'''

class PlayController(Controller):
	def __init__(self, app, service, ruler):
		Controller.__init__(self, 'play', __name__)
		self.app = app
		self.game = service
		self.verifier = ruler
		# Set up controller-specific logger
		self.logger = logging.getLogger('pg_server.PlayController')
		self.logger.setLevel(logging.DEBUG)
		# Add file handler if not already present
		if not self.logger.handlers:
			fh = logging.FileHandler('server.log')
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			fh.setFormatter(formatter)
			self.logger.addHandler(fh)
		
		# this is how we will deal with turn time-outs
		# every time a valid request is made, we will reset this timer
		self.timeout_master = threading.Timer(3, self.player_timeout)
		self.first_pass = False 	# we need this to pad the first players response. TODO: find something cleaner?
		self.timeout_master.start()
		self.logger.info("PlayController initialized")

	def player_timeout(self):
		'''
		if this function triggers, we pass the current player's turn for taking too long
		'''
		if not self.game.started:
			# game has not yet started; it's no one's turn!
			self.timeout_master = threading.Timer(3, self.player_timeout)
			self.timeout_master.start()
			return
		elif self.first_pass:
			logger.info("Current player took too long to respond; passing the turn")
			self.game.resolve_turn()
		else:
			self.first_pass = True
		self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
		self.timeout_master.start()

	def pass_the_bid(self, name, player_id):
		self.timeout_master.cancel()
		msg = "{} deliberately passed on the bid".format(name)
		logger.info(msg)
		self.game.auction_pass(player_id)
		self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
		self.timeout_master.start()
		return json.dumps({"status" : "SUCCESS", "msg" : msg})

	@route("/bid", methods=['POST'])
	def bid(self):
		if 'player_id' not in session:
			logger.warning("Bid attempt without player_id in session")
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		
		try:
			player_id = session['player_id']
			name = self.game.get_player_name(player_id)
			logger.info(f"Received bid request from {name} (id: {player_id})")
			
			player_req = request.get_json()
			logger.debug(f"Bid request data: {player_req}")
			
			try:
				bid = player_req["bid"]
				bid = int(bid)
				logger.debug(f"Parsed bid amount: {bid}")
			except (KeyError, ValueError, TypeError) as e:
				error_msg = "Missing 'bid' parameter" if isinstance(e, KeyError) else \
						"'bid' must be a valid integer" if isinstance(e, ValueError) else \
						"Your content must be sent as json!"
				logger.warning(f"Bid validation failed: {error_msg}")
				return json.dumps({"status": "FAIL", "msg": error_msg})
			
			can_decide, msg = self.verifier.is_turn(player_id, Phase.AUCTION)
			logger.debug(f"Turn verification for {name}: can_decide={can_decide}, msg={msg}")
			
			if can_decide and not self.game.auction.auction_in_progress and bid == -1:
				logger.debug(f"Player {name} attempting to pass without auction in progress")
				# special case! You cannot pass the turn in the first round 
				if not self.verifier.player_can_pass(player_id):
					logger.info(f"Player {name} tried to pass in first round")
					return json.dumps({"status": "FAIL", "msg":"You cannot pass on bidding in the first round!"})
				# we don't need the other parameters
				return self.pass_the_bid(name, player_id)
			
			try:
				powerplant_id = player_req["powerplant_id"]
				powerplant_id = int(powerplant_id)
				logger.debug(f"Parsed powerplant_id: {powerplant_id}")
			except (KeyError, ValueError) as e:
				error_msg = "Missing 'powerplant_id' parameter" if isinstance(e, KeyError) else \
						"'powerplant_id' must be a valid integer"
				logger.warning(f"Powerplant validation failed: {error_msg}")
				return json.dumps({"status": "FAIL", "msg": error_msg})

			trash_id = None
			if self.verifier.player_has_3_plants(player_id) and bid > -1:
				logger.debug(f"Player {name} has 3 plants, checking for trash parameter")
				try:
					trash_id = player_req["trash"]
					trash_id = int(trash_id)
					logger.debug(f"Parsed trash_id: {trash_id}")
				except (KeyError, ValueError) as e:
					error_msg = "Missing 'trash' parameter" if isinstance(e, KeyError) else \
							"'trash' must be a valid integer"
					logger.warning(f"Trash validation failed: {error_msg}")
					return json.dumps({"status": "FAIL", "msg": error_msg})

			if not can_decide:
				logger.info(f"Player {name} tried to bid out of turn: {msg}")
				return json.dumps({"status": "FAIL", "msg": msg})
			
			# resolve that we have a valid event!
			logger.debug("Valid bid event, canceling timeout")
			self.timeout_master.cancel()
			
			if bid == -1:
				logger.info(f"Player {name} chose to pass")
				return self.pass_the_bid(name, player_id)

			is_valid, msg = self.verifier.is_valid_bid(player_id, powerplant_id, bid, trash_id)
			logger.debug(f"Bid validation: is_valid={is_valid}, msg={msg}")
			
			if not is_valid:
				self.game.auction_pass(player_id)
				self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
				self.timeout_master.start()
				logger.info(f"Player {name} submitted invalid bid: {msg}")
				return json.dumps({"status": "FAIL", "msg" : msg})
			
			self.game.auction_bid(player_id, bid, powerplant_id, trash_id)
			self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
			self.timeout_master.start()
			msg = f"{name} successfully bid {bid} on Powerplant {powerplant_id}"
			logger.info(msg)
			return json.dumps({"status": "SUCCESS", "msg" : msg})
			
		except Exception as e:
			logger.error(f"Unexpected error in bid endpoint: {str(e)}", exc_info=True)
			return json.dumps({"status": "FAIL", "msg": "Server error processing bid"})

	@route("/buy", methods=['POST'])
	def buy(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUY_RESOURCES)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg}) 

		# logger.info("Valid Event! Canceling timeout.")
		self.timeout_master.cancel()

		resp = {}
		player_req = request.get_json()
		if player_req is None:
			return json.dumps({"status": "FAIL", "msg": "Your content must be sent as json!"}) 
		for item in player_req:
			if item.lower() == "oil":
				r_type = RType.OIL 
			elif item.lower() == "gas":
				r_type = RType.GAS 
			elif item.lower() == "uranium":
				r_type = RType.URANIUM 
			elif item.lower() == "coal":
				r_type = RType.COAL
			else: 
				resp[item] = {"status": "FAIL", "msg": "Unable to parse as 'oil' or 'gas' or 'coal' or 'uranium'"}
				continue
			resp[item] = {}
			try:
				amount = player_req[item]
				amount = int(amount)
			except ValueError:
				resp[item]["status"] = "FAIL"
				resp[item]["msg"] = "{} requested an invalid integer {}".format(item, player_req[item])
				continue
			logger.info("{} has requested {} {}".format(name, amount, r_type.name))
			can_buy, msg, num_buy = self.verifier.can_buy_resources(player_id, r_type, amount)
			if not can_buy:
				resp[item]["status"] = "FAIL"
				resp[item]["msg"] = msg
			else:
				resp[item]["status"] = "SUCCESS"
				resp[item]["msg"] = "Bought {} resources".format(num_buy)
			if num_buy > 0:
				cost = self.game.buy_resources(player_id, r_type, num_buy)
				logger.info("{} purchased {} {} for {} money".format(name, num_buy, r_type.name, cost))
				resp[item]["amount"] = num_buy 
				resp[item]["cost"] = cost 
		self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
		self.timeout_master.start()
		self.game.next_turn()
		return json.dumps(resp)


	@route("/build", methods=['POST'])
	def build(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		data = request.get_json()
		try:
			paths = data["paths"]
			assert(type(paths) == list)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'paths' parameter", "cost": 0})
		except AssertionError:
			return json.dumps({"status": "FAIL", "msg":"'paths' must be a list"})
		except TypeError:
			return json.dumps({"status": "FAIL", "msg":"Your content must be sent as json!"})

		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUILD_GENERATORS)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg, "cost": 0})
		else:
			# resolve that we have a valid event!
			# logger.info("Valid Event! Canceling timeout.")
			self.timeout_master.cancel()

		if len(paths) == 0:
			msg = "{} submitted no cities to purchase; passing the turn".format(name)
			logger.info(msg)
			self.game.next_turn()
			self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
			self.timeout_master.start()
			return json.dumps({"status": "SUCCESS", "msg": msg, "cost": 0})

		status = []
		msgs = []
		total_cost = 0
		for path in paths:
			legal_action, msg = self.verifier.is_valid_build(player_id, path)
			if not legal_action:
				status.append('FAIL')
				msgs.append(msg)
				continue

			cost = self.game.build_generator(player_id, path)
			msg = "{} built a generator in {} for {} money".format(name, path[-1], cost)
			logger.info(msg)
			status.append('SUCCESS')
			msgs.append(msg)
			total_cost += cost
		self.game.next_turn()
		self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
		self.timeout_master.start()
		return json.dumps({"status": status, "msg": msgs, "cost": total_cost})

	@route("/power", methods=['POST'])
	def power(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUREAUCRACY)
		data = request.get_json()
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg, "cost": 0})
		try:
			powerplants = data["powerplants"]
			assert(type(powerplants) == list)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'powerplants' Parameter"})
		except AssertionError:
			return json.dumps({"status": "FAIL", "msg":"'powerplants' must be a list"})
		except TypeError:
			return json.dumps({"status": "FAIL", "msg":"Your content must be sent as json!"})
		if self.verifier.plants_are_hybrid(player_id, powerplants):
			try:
				num_oil = data["num_oil"]
				num_oil = int(num_oil)
				assert(num_oil >= 0)
			except BadRequestKeyError:
				return json.dumps({"status": "FAIL", "msg":"Missing 'num_oil' parameter"})
			except ValueError:
				return json.dumps({"status": "FAIL", "msg":"'num_oil' must be an integer"})
			except AssertionError:
				return json.dumps({"status": "FAIL", "msg":"'num_oil' must be a non-negative integer"})
		else:
			num_oil = 0
		# logger.info("Valid Event! Canceling timeout.")
		self.timeout_master.cancel()
		if len(powerplants) == 0:
			amount = self.game.player_powered(player_id, 0)
			self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
			self.timeout_master.start()
			return json.dumps({"status": "SUCCESS", "msg": "Powered no powerplants", "profit": amount})

		status = []
		msgs = []
		total_power = 0
		for plant in powerplants:
			can_power, msg, remaining_oil = self.verifier.player_can_power(player_id, plant, num_oil)
			if not can_power:
				status.append("FAIL")
				msgs.append(msg)
			else:
				status.append("SUCCESS")
				power = self.game.plant_powered(player_id, plant, num_oil-remaining_oil)
				msgs.append("Powerplant {} generated {} power".format(plant, power))
				total_power += power 
		profit = self.game.player_powered(player_id, total_power)
		self.timeout_master = threading.Timer(TIMEOUT_VALUE, self.player_timeout)
		self.timeout_master.start()
		return json.dumps({"status":status, "msg": msgs, "profit": profit})

