from flask import Flask
from flask_restful import Resource, Api
import settings
from controllers import infoConroller, playerController
from os import sys, path

# web server that wraps the expression scanner
class WebServer(Flask):
    def __init__(self, import_name):
        Flask.__init__(self, import_name)
        self.config.from_object(settings.Settings)
        self.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self._initialize()

    # additional initialization
    def _initialize(self):
        self.register_blueprint(infoController.InfoController(self.service))
        self.register_blueprint(playerController.PlayerController(self, self.service))

    # override run
    def run(self):
        Flask.run(self, host=self.config['HOST'], port=self.config['PORT'], debug=self.config['DEBUG'], use_reloader=False, threaded=True)

# makes the python file runnable from the python command line eg. python webServer.py
# creates an instance of the web server and run
if __name__ == "__main__":
    server = WebServer(__name__)
    server.run()
