import os
import sys

class Settings:
    def __init__(self):
        pass

    HOST = "127.0.0.1"
    PORT = 5050
    DEBUG = True
    BASE_PATH = os.getcwd()

    # If you would like to log output in a file, change logging to True and desired_log_name to your desired filename
    logging = False
    desired_log_name = 'output.txt'

    if logging:
        file = open(desired_log_name, 'a')
        sys.stdout = file
        sys.stderr = file
