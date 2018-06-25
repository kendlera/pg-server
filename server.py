from flask import Flask
import settings
from controllers import infoController, playerController, playController
from components import game, verifier
from os import sys, path
import logging
logger = logging.getLogger('pg_server')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# web server that wraps the expression scanner
class WebServer(Flask):
    def __init__(self, import_name):
        Flask.__init__(self, import_name)
        self.config.from_object(settings.Settings)
        self.game_service = game.Game()
        self.ruler = verifier.Verifier(self.game_service)
        self._initialize()

    # additional initialization
    def _initialize(self):
        self.register_blueprint(infoController.InfoController(self, self.game_service))
        self.register_blueprint(playController.PlayController(self, self.game_service, self.ruler))
        self.register_blueprint(playerController.PlayerController(self, self.game_service, self.config['KEY']))

    # override run
    def run(self):
        logger.info("Server started at {}:{}".format(self.config['HOST'], self.config['PORT']))
        Flask.run(self, host=self.config['HOST'], port=self.config['PORT'], debug=self.config['DEBUG'], use_reloader=False, threaded=True)

# makes the python file runnable from the python command line eg. python webServer.py
# creates an instance of the web server and run
if __name__ == "__main__":
    server = WebServer(__name__)
    server.run()
