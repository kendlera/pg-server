from controllers.routing import route
from controllers.controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session
import uuid
import json
import sched
import time
import logging
logger = logging.getLogger('playerController')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
logger.addHandler(fh)

'''
file that allows registration of players to specific games
'''

class PlayerController(Controller):
	def __init__(self, app, service, key):
		Controller.__init__(self, 'player', __name__)
		print(__name__)
		self.app = app
		self.service = service
		app.secret_key = key
		self.player_count = 0
		self.game_started = False
		self.game_scheduler = sched.scheduler(time.time, time.sleep)
		# schedule the game to start after 60 seconds
		self.game_scheduler.enter(60, 1, self.start_game)

	def start_game(self):
		if not self.game_started:
			logger.info("Starting the game!")
			self.game_started = True 
			self.service.start_game()

	@route("/test", methods=['GET'])
	def test(self):
		print("Hit the endpoint!")
		return json.dumps({"FAIL": 'none'})

	@route("/register", methods=['POST'])
	def join(self):
		if 'player_id' in session:
			name = self.service.get_player_name(session['player_id'])
			return json.dumps({"status": "FAIL", "msg": "You have already joined this game as {}".format(name)})

		if self.game_started:
			return json.dumps({"status":"FAIL", "msg": "The game has already started!"})

		if self.player_count >= 6:
			# we probably will never get here because we start the 
			# game once we get 6 people...
			return json.dumps({"status":"FAIL", "msg": "The game is full!"})

		try:
			name = request.form["player_name"]
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'player_name' Parameter"})

		player_id = uuid.uuid4().hex
		session['player_id'] = player_id 
		self.player_count += 1
		unique_name = self.service.add_player(name, player_id)
		logger.info("Added player {} to the game".format(unique_name))
		if self.player_count >= 6:
			# We have reached the maximum number of players; start the game!
			game_scheduler.enter(3, 1, self.start_game)
		return json.dumps({"status": "SUCCESS", "msg": "{} has joined the game!".format(unique_name)})
