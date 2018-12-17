import os
import sys


class Settings:
    def __init__(self):
        pass

    HOST = "127.0.0.1" 			# ip address of server
    PORT = 5050 				# port of server
    DEBUG = True 				# Flask parameter
    BASE_PATH = os.getcwd() 	# probably don't need to change this
    KEY = 'something secret' 	# this is the key we use to sign user cookies.

    