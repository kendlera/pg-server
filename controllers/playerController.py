from routing import route
from controller import Controller
from werkzeug.exceptions import BadRequestKeyError
from flask import request, session

'''
file that allows registration of players to specific games
'''

class PlayerController(Controller):
	def __init__(self, app, service):
        Controller.__init__(self, 'player', __name__)
        self.app = app
        self.service = service
        app.secret_key = ""

    @route("/register", methods=['POST'])
    def index(self):
    	try:
			name = request.form["player_name"]
		except BadRequestKeyError:
			return json.dumps({"failed":"Missing 'scanname' Parameter"})
