from routing import route
from controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session
from components.phase import Phase
from components.rType import RType
import uuid
import json
import sched
import time
import logging
logger = logging.getLogger('playController')
fh = logging.FileHandler('output.log')
logger.addHandler(fh)
TIMEOUT_VALUE = 20 # how many seconds each player gets to make a decision
'''
manages player action requests
'''

class PlayController(Controller):
	def __init__(self, service, ruler):
        Controller.__init__(self, 'play', __name__)
        self.game = service
        self.verifier = ruler
        # this is how we will deal with turn time-outs
        # every time a valid request is made, we will reset this timer
        self.timeout_master = sched.scheduler(time.time, time.sleep)
        # we give the first player an extra 10 seconds to make the first decision
        self.current_turn_event = self.timeout_master(TIMEOUT_VALUE + 10, 1, self.player_timeout)

    def player_timeout(self):
    	'''
    	if this function triggers, we pass the current player's turn for taking too long
    	'''
    	logger.info("Current player took too long to respond; passing the turn")
    	self.game.resolve_turn()

    @route("/bid", methods=['POST'])
    def bid(self):
    	if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		try:
			bid = request.form["bid"]
			bid = int(bid)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'bid' parameter")
		except ValueError:
			return json.dumps({"status": "FAIL", "msg":"'bid' must be a valid integer"})
		try:
			powerplant_id = request.form["powerplant_id"]
			powerplant_id = int(powerplant_id)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'powerplant_id' parameter")
		except ValueError:
			return json.dumps({"status": "FAIL", "msg":"'powerplant_id' must be a valid integer"})
		if self.verifier.player_has_3_plants(player_id):
			try:
				trash_id = request.form["trash"]
			except BadRequestKeyError:
				return json.dumps({"status": "FAIL", "msg":"Missing 'trash' parameter")
		else:
			trash_id = None
		can_decide, msg = self.verifier.is_turn(player_id, Phase.AUCTION)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg})
		else:
			# resolve that we have a valid event!
			logger.info("Valid Event! Canceling timeout.")
			self.timeout_master.cancel(self.current_turn_event)
		if bid == -1:
			msg = "{} deliberately passed on the bid".format(name)
			logger.info(msg)
			self.game.auction_pass(player_id)
			self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
			return json.dumps({"status" : "SUCCESS", "msg" : msg)

		is_valid, msg = self.verifier.is_valid_bid(player_id, powerplant_id, bid):
		if not is_valid:
			self.game.auction_pass(player_id)
			self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
			logger.info("{} submitted an invalid bid; {}".format(name, msg))
			return json.dumps({"status": "FAIL", "msg" : msg})
		else:
			self.game.auction_bid(player_id, bid, powerplant_id, trash_id)
			self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
			msg = "{} successfully bid {} on Powerplant {}".format(name, bid, powerplant_id)
			logger.info(msg)
			return json.dumps({"status": "SUCCESS", "msg" : msg})

	@route("/buy", methods=['POST'])
    def build(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUY_RESOURCES)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg}) 

		logger.info("Valid Event! Canceling timeout.")
		self.timeout_master.cancel(self.current_turn_event)

		resp = {}
		msgs = []
		did_fail = False
		for item in request.form:
			if item.lower() == "oil":
				r_type = RType.OIL 
			elif item.lower() == "gas":
				r_type = RType.GAS 
			elif item.lower() == "uranium":
				r_type = RType.URANIUM 
			elif item.lower() == "coal":
				r_type == RType.COAL
			else: 
				continue
			try:
				amount = request.form[item]
				amount = int(amount)
			except ValueError:
				msgs.append("{} requested an invalid integer {}".format(item, request.form[item]))
				continue
			can_buy, msg, num_buy = self.verifier.can_buy_resources(player_id, r_type, amount)
			if not can_buy:
				did_fail = True
			elif num_buy > 0:
				self.game.buy_resources(player_id, r_type, num_buy)


    @route("/build", methods=['POST'])
    def build(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		try:
			paths = request.form["paths"]
			assert(type(paths) == list)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'paths' parameter", "cost": 0})
		except AssertionError:
			return json.dumps({"status": "FAIL", "msg":"'paths' must be a list"})

		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUILD_GENERATORS)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg, "cost": 0})
		else:
			# resolve that we have a valid event!
			logger.info("Valid Event! Canceling timeout.")
			self.timeout_master.cancel(self.current_turn_event)

		if len(paths) == 0:
			msg = "{} submitted no cities to purchase; passing the turn".format(name)
			logger.info(msg)
			self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
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
		self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
		return json.dumps({"status": status, "msg": msgs, "cost": total_cost})

	@route("/power", methods=['POST'])
    def power(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		can_decide, msg = self.verifier.is_turn(player_id, Phase.BUREAUCRACY)
		if not can_decide:
			return json.dumps({"status": "FAIL", "msg": msg, "cost": 0})
		try:
			powerplants = request.form["powerplants"]
			assert(type(powerplants)) == list)
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'powerplants' Parameter"})
		except AssertionError:
			return json.dumps({"status": "FAIL", "msg":"'powerplants' must be a list"})
		if self.verifier.plants_are_hybrid(player_id, powerplants):
			try:
				num_oil = request.form["num_oil"]
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
		logger.info("Valid Event! Canceling timeout.")
		self.timeout_master.cancel(self.current_turn_event)
		if len(powerplants) == 0:
			amount = self.game.player_powered(player_id, 0)
			self.current_turn_event = self.timeout_master.enter(TIMEOUT_VALUE, 1, self.player_timeout)
			return json.dumps({"status": "SUCCESS", "msg": "Powered no powerplants", "profit": amount})

		status = []
		msgs = []
		total_power = 0
		for plant in powerplants:
			can_power, msg, remaining_oil = self.verifier.player_can_power(player_id, plant, num_oil)
			if not can_power:
				status.append("FAIL")
				msg.append(msg)
			else:
				status.append("SUCCESS")
				power = self.game.plant_powered(player_id, plant, num_oil-remaining_oil)
				msg.append("Powerplant {} generated {} power".format(plant, power))
				total_power += power 
		profit = self.game.player_powered(player_id, total_power)
		logger.info("{} powered {} generators for {} money".format(name, total_power, profit))
		return json.dumps({"status":status, "msg": msgs, "profit": profit})

