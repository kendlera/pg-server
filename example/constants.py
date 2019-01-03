import os

SERVER_HOST = os.environ.get('POWER_GRID_HOST') or 'http://127.0.0.1'
SERVER_PORT = os.environ.get('POWER_GRID_PORT') or ':5050'
