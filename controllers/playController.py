from routing import route
from controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session
import uuid
import json
import sched
import time
import logging
logger = logging.getLogger('playController')
fh = logging.FileHandler('output.log')
logger.addHandler(fh)
'''
manages player action requests
'''

class PlayController(Controller):
	def __init__(self, service, ruler):
        Controller.__init__(self, 'play', __name__)
        self.game = service
        self.verifier = ruler

    @route("/build", methods=['POST'])
    def build(self):
		if 'player_id' not in session:
			return json.dumps({"msg": "You have not joined this game!", "status": "FAIL"})
		player_id = session['player_id']
		name = self.game.get_player_name(player_id)
		try:
			path = request.form["path"]
		except BadRequestKeyError:
			return json.dumps({"status": "FAIL", "msg":"Missing 'path' Parameter"})

		legal_action, msg = self.verifier.is_valid_build(player_id, path)
		if not legal_action:
			return json.dumps({"status": "FAIL", "msg": msg})

		cost = self.game.build_generator(player_id, path)
		msg = "{} built a generator in {} for {} money".format(name, path[-1], cost)
		logger.info(msg)
		return json.dumps({"status": "SUCCEED", "msg": msg, "cost": cost})