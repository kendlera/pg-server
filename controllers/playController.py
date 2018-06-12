from routing import route
from controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session
from components.phase import Phase
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
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'bid' Parameter")
		try:
			powerplant_id = request.form["powerplant_id"]
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'powerplant_id' Parameter")
		if self.verifier.player_has_3_plants(player_id):
			try:
				trash_id = request.form["trash"]
			except BadRequestKeyError:
				return json.dumps({"status": "FAIL", "msg":"Missing 'trash' Parameter")
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


    @route("/build", methods=['POST'])
    def build(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		try:
			path = request.form["path"]
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'paths' Parameter", "cost": 0})

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