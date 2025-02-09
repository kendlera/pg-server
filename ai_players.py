import requests
import time
import sys
import os
import random
import logging
from enum import Enum

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ai_players.log')
    ]
)
logger = logging.getLogger('AI_Players')

# Configuration
SERVER_HOST = "http://127.0.0.1"
SERVER_PORT = ":5050"
server_url = SERVER_HOST + SERVER_PORT

class Phase(Enum):
    AUCTION = "AUCTION"
    BUY_RESOURCES = "BUY_RESOURCES"
    BUILD_GENERATORS = "BUILD_GENERATORS"
    BUREAUCRACY = "BUREAUCRACY"

class BaseAI:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(f'AI_Players.{name}')
        self.logger.info(f"Initializing {name}")
        
        response = requests.post(
            server_url + "/register", 
            data={"player_name": name}
        )
        response_data = response.json()
        self.logger.info(f"Registration response: {response_data}")
        
        # Update name if server assigned a unique one
        if response_data.get('status') == 'SUCCESS' and 'name' in response_data:
            original_name = self.name
            self.name = response_data['name']
            self.logger.info(f"Server assigned unique name: '{self.name}' (was '{original_name}')")
            
        self.player_token = response.cookies
        self.logger.debug(f"Received cookies: {dict(response.cookies)}")
        self.logger.info(f"Received player token: {self.player_token}")
        
    def is_my_turn(self):
        response = requests.get(server_url + "/turn_info").json()
        current_player = response.get('current_player')
        current_phase = response.get('phase')
        
        # Handle "game not started" response
        if 'msg' in response:
            self.logger.debug(f"Turn check response has message: {response['msg']}")
            return False
            
        is_turn = current_player == self.name
        self.logger.info(f"Turn check - My name: {self.name}, Current player: {current_player}, Phase: {current_phase}, Is my turn: {is_turn}")
        return is_turn

    def get_game_state(self):
        self.logger.debug("Fetching game state...")
        
        # Get all states
        market = requests.get(server_url + "/market").json()
        my_info_response = requests.get(server_url + "/my_info", cookies=self.player_token).json()
        players = requests.get(server_url + "/player_info").json()
        auction = requests.get(server_url + "/auction").json()
        turn_info = requests.get(server_url + "/turn_info").json()
        
        # Log responses for debugging
        self.logger.debug(f"my_info response: {my_info_response}")
        
        # Handle potential error responses
        if 'msg' in my_info_response:
            self.logger.warning(f"Error in my_info: {my_info_response['msg']}")
            my_info = {'money': 50, 'powerplants': [], 'resources': {}}  # Default state
        else:
            my_info = my_info_response
            
        state = {
            'market': market,
            'my_info': my_info,
            'players': players,
            'auction': auction,
            'turn_info': turn_info
        }
        
        self.logger.debug(f"Current phase: {state['turn_info'].get('phase')}")
        return state

    def do_turn(self):
        try:
            state = self.get_game_state()
            phase = state['turn_info'].get('phase')
            self.logger.info(f"Starting my turn in phase: {phase}")
            
            if phase == Phase.AUCTION.value:
                self.do_auction()
            elif phase == Phase.BUY_RESOURCES.value:
                self.do_buy_resources()
            elif phase == Phase.BUILD_GENERATORS.value:
                self.do_build_generators()
            elif phase == Phase.BUREAUCRACY.value:
                self.do_bureaucracy()
            else:
                self.logger.error(f"Unknown phase: {phase}")
        except Exception as e:
            self.logger.error(f"Error during turn: {str(e)}", exc_info=True)

    def can_afford(self, cost):
        money = self.get_game_state()['my_info']['money']
        self.logger.debug(f"Checking if can afford {cost} with {money} money")
        return money >= cost

    def make_request(self, method, endpoint, **kwargs):
        """Helper to make requests with logging"""
        url = server_url + endpoint
        self.logger.info(f"Making {method} request to {endpoint}")
        self.logger.debug(f"Request details: {kwargs}")
        
        if 'cookies' not in kwargs:
            kwargs['cookies'] = self.player_token

        response = requests.request(method, url, **kwargs)
        self.logger.info(f"Response status: {response.status_code}")
        self.logger.debug(f"Response body: {response.text}")
        
        return response

class GreedyAI(BaseAI):
    def calculate_max_bid(self, plant):
        """Calculate maximum bid we're willing to make for a plant"""
        base_cost = plant.get('market_cost', 0)
        generators = plant.get('generators', 0)
        resource_cost = plant.get('resource_cost', 1)
        
        # Value based on power generation and resource efficiency
        value = base_cost * (generators / resource_cost)
        
        # Add a small random factor to prevent AI deadlock
        max_bid = int(value * 1.5 + random.randint(0, 2))
        self.logger.debug(f"Calculated max bid {max_bid} for plant {plant}")
        return max_bid

    def do_auction(self):
        self.logger.info("Starting auction phase")
        state = self.get_game_state()
        self.logger.debug(f"Full game state: {state}")
        
        # Extract auction and market info, with defaults
        auction = state.get('auction', {})
        market = state.get('market', {})
        
        self.logger.info(f"Market state: {market}")
        self.logger.info(f"Auction state: {auction}")
        
        if auction.get('auction_in_progress'):
            # Get current plant details from auction
            current_plant = auction.get('powerplant', {})
            plant_id = current_plant.get('market_cost')
            current_bid = auction.get('current_bid', 0)
            self.logger.info(f"Auction in progress for plant {current_plant} at {current_bid}")
            
            # Calculate maximum we're willing to bid
            max_bid = self.calculate_max_bid(current_plant)
            next_bid = current_bid + 1
            
            if self.can_afford(next_bid) and next_bid <= max_bid:
                self.logger.info(f"Bidding {next_bid} (max {max_bid})")
                response = self.make_request('POST', "/bid", json={
                    'powerplant_id': plant_id,
                    'bid': next_bid
                })
                self.logger.info(f"Bid response: {response.text}")
            else:
                reason = "cannot afford" if not self.can_afford(next_bid) else "exceeds max bid"
                self.logger.info(f"Passing ({reason})")
                response = self.make_request('POST', "/bid", json={
                    'bid': -1,
                    'powerplant_id': 0
                })
                self.logger.info(f"Pass response: {response.text}")
        else:
            self.logger.info("No auction in progress, may start new auction")
            available_plants = market.get('current_market', [])
            self.logger.info(f"Available plants: {available_plants}")
            
            # Filter for affordable plants
            affordable_plants = []
            for plant in available_plants:
                cost = plant.get('market_cost', 0)
                max_bid = self.calculate_max_bid(plant)
                self.logger.debug(f"Plant {cost}: max bid {max_bid}")
                if self.can_afford(cost) and cost <= max_bid:
                    affordable_plants.append(plant)
            
            self.logger.info(f"Affordable plants: {affordable_plants}")
            
            if affordable_plants:
                # Find most expensive affordable plant
                plant = max(affordable_plants, key=lambda x: x.get('market_cost', 0))
                cost = plant.get('market_cost', 0)
                self.logger.info(f"Starting auction for plant: {plant}")
                
                response = self.make_request('POST', "/bid", json={
                    'powerplant_id': cost,
                    'bid': cost
                })
                self.logger.info(f"Initial bid response: {response.text}")
            else:
                self.logger.info("No affordable plants within max bid limits, passing")
                response = self.make_request('POST', "/bid", json={
                    'bid': -1,
                    'powerplant_id': 0
                })
                self.logger.info(f"Pass response: {response.text}")

    def do_buy_resources(self):
        self.logger.info("Starting buy resources phase")
        state = self.get_game_state()
        resources_needed = {}
        
        for plant in state['my_info']['powerplants']:
            if plant['resource_type'] != 'CLEAN':
                rtype = plant['resource_type'].lower()
                if rtype not in resources_needed:
                    resources_needed[rtype] = 0
                resources_needed[rtype] += plant['resource_cost']
        
        self.logger.info(f"Buying resources: {resources_needed}")
        response = self.make_request('POST', "/buy", json=resources_needed)

    def get_city_info(self):
        """Get current board state and costs"""
        try:
            board_data = requests.get(server_url + "/board").json()
            self.logger.debug(f"Board data: {board_data}")
        except Exception as e:
            self.logger.error(f"Error getting board data: {e}")
            board_data = []
            
        try:
            city_status = requests.get(server_url + "/city_status").json()
            self.logger.debug(f"City status: {city_status}")
            if isinstance(city_status, dict) and 'msg' in city_status:
                self.logger.warning(f"City status returned message: {city_status['msg']}")
                city_status = {}
        except Exception as e:
            self.logger.error(f"Error getting city status: {e}")
            city_status = {}
        
        # Build city graph
        cities = {}
        for edge in board_data:
            if not isinstance(edge, (list, tuple)) or len(edge) < 3:
                self.logger.warning(f"Invalid edge data: {edge}")
                continue
                
            city1, city2, cost = edge[:3]
            cities[city1] = cities.get(city1, {'name': city1, 'connections': [], 'owners': []})
            cities[city2] = cities.get(city2, {'name': city2, 'connections': [], 'owners': []})
            cities[city1]['connections'].append((city2, cost))
            cities[city2]['connections'].append((city1, cost))
        
        # Add ownership info
        for city_name, owners in city_status.items():
            if city_name in cities:
                cities[city_name]['owners'] = owners if isinstance(owners, list) else []
                
        return cities

    def find_buildable_cities(self, cities):
        """Find cities we can build in"""
        buildable = []
        try:
            for city_name, city_info in cities.items():
                owners = city_info.get('owners', [])
                if self.name not in owners:  # We don't already own it
                    # Look for connections to our existing cities
                    connected = False
                    if not owners:  # No owners means starting city is ok
                        connected = True
                    else:
                        owned_cities = [c for c, info in cities.items() if self.name in info.get('owners', [])]
                        if not owned_cities:  # First city is ok anywhere
                            connected = True
                        else:
                            for owned_city in owned_cities:
                                if any(conn[0] == owned_city for conn in city_info['connections']):
                                    connected = True
                                    break
                    
                    if connected:
                        buildable.append(city_name)
                        
        except Exception as e:
            self.logger.error(f"Error finding buildable cities: {e}")
            
        return buildable

    def do_build_generators(self):
        self.logger.info("Starting build generators phase")
        state = self.get_game_state()
        
        try:
            # Get board state
            cities = self.get_city_info()
            self.logger.info(f"Found cities: {list(cities.keys())}")
            self.logger.debug(f"Full city info: {cities}")
            
            # Find cities we can build in
            buildable_cities = self.find_buildable_cities(cities)
            self.logger.info(f"Buildable cities: {buildable_cities}")
            
            # For now, just try direct paths to buildable cities
            paths = [[city] for city in buildable_cities]
            self.logger.info(f"Building paths: {paths}")
            
            if paths:
                response = self.make_request('POST', "/build", json={
                    'paths': paths
                })
                self.logger.info(f"Build response: {response.text}")
            else:
                # Even with no paths, we need to send an empty list to pass the turn
                response = self.make_request('POST', "/build", json={
                    'paths': []
                })
                self.logger.info("No valid paths, passing build phase")
                
        except Exception as e:
            self.logger.error(f"Error during build phase: {e}", exc_info=True)
            # Send empty paths list to pass turn on error
            response = self.make_request('POST', "/build", json={
                'paths': []
            })
            self.logger.info("Error occurred, passing build phase")

    def do_bureaucracy(self):
        self.logger.info("Starting bureaucracy phase")
        state = self.get_game_state()
        my_info = state['my_info']
        
        powerplants = my_info.get('powerplants', [])
        self.logger.info(f"My powerplants: {powerplants}")
        
        # For hybrid plants, check our resource stocks to decide what to use
        has_hybrid = any(p.get('resource_type') == 'HYBRID' for p in powerplants)
        
        if has_hybrid:
            # If we have hybrid plants, count our resources
            resources = my_info.get('resources', {})
            oil_amount = resources.get('OIL', 0)
            gas_amount = resources.get('GAS', 0)
            
            # Use more oil if we have more oil than gas
            num_oil = 2 if oil_amount > gas_amount else 0
            self.logger.info(f"Using {num_oil} oil for hybrid plants (have {oil_amount} oil, {gas_amount} gas)")
            
            powerplant_ids = [p['market_cost'] for p in powerplants]
            response = self.make_request('POST', "/power", json={
                'powerplants': powerplant_ids,
                'num_oil': num_oil
            })
        else:
            powerplant_ids = [p['market_cost'] for p in powerplants]
            response = self.make_request('POST', "/power", json={
                'powerplants': powerplant_ids,
                'num_oil': 0  # No hybrid plants, so no oil needed
            })
            
        self.logger.info(f"Power response: {response.text}")

class ResourceAI(BaseAI):
    def do_auction(self):
        self.logger.info("Starting auction phase")
        state = self.get_game_state()
        self.logger.debug(f"Full game state: {state}")
        
        # Extract auction and market info, with defaults
        auction = state.get('auction', {})
        market = state.get('market', {})
        
        self.logger.info(f"Market state: {market}")
        self.logger.info(f"Auction state: {auction}")
        
        if auction.get('auction_in_progress'):
            plant_id = auction.get('plant_id')
            current_bid = auction.get('current_bid', 0)
            self.logger.info(f"Auction in progress for plant {plant_id} at {current_bid}")
            
            try:
                # Find plant details in market
                available_plants = market.get('current_market', [])
                plant = next((p for p in available_plants if p.get('market_cost') == plant_id), None)
                
                if plant:
                    # Calculate efficiency
                    resource_cost = plant.get('resource_cost', 1)  # Default to 1 to avoid division by zero
                    generators = plant.get('generators', 0)
                    efficiency = generators / resource_cost if resource_cost > 0 else float('inf')
                    self.logger.info(f"Plant efficiency: {efficiency}")
                    
                    if efficiency > 1.5 and self.can_afford(current_bid + 1):
                        self.logger.info(f"Bidding {current_bid + 1}")
                        response = self.make_request('POST', "/bid", json={
                            'powerplant_id': plant_id,
                            'bid': current_bid + 1
                        })
                        self.logger.info(f"Bid response: {response.text}")
                    else:
                        self.logger.info("Plant not efficient enough or too expensive")
                        response = self.make_request('POST', "/bid", json={
                            'bid': -1,
                            'powerplant_id': 0
                        })
                        self.logger.info(f"Pass response: {response.text}")
                else:
                    self.logger.warning(f"Could not find plant {plant_id} in market!")
                    response = self.make_request('POST', "/bid", json={
                        'bid': -1,
                        'powerplant_id': 0
                    })
                    self.logger.info(f"Pass response: {response.text}")
                    
            except Exception as e:
                self.logger.error(f"Error processing plant efficiency: {str(e)}")
                response = self.make_request('POST', "/bid", json={
                    'bid': -1,
                    'powerplant_id': 0
                })
                self.logger.info(f"Pass response after error: {response.text}")
        else:
            self.logger.info("No auction in progress, may start new auction")
            available_plants = market.get('current_market', [])
            self.logger.info(f"Available plants: {available_plants}")
            
            # Filter for affordable plants
            affordable_plants = []
            for plant in available_plants:
                cost = plant.get('market_cost', 0)
                resource_cost = plant.get('resource_cost', 1)
                generators = plant.get('generators', 0)
                efficiency = generators / resource_cost if resource_cost > 0 else float('inf')
                
                self.logger.debug(f"Plant {cost}: efficiency {efficiency}")
                if self.can_afford(cost):
                    affordable_plants.append((plant, efficiency))
            
            self.logger.info(f"Affordable plants: {affordable_plants}")
            
            if affordable_plants:
                # Find most efficient affordable plant
                plant, efficiency = max(affordable_plants, key=lambda x: x[1])
                cost = plant.get('market_cost', 0)
                self.logger.info(f"Starting auction for plant: {plant} (efficiency: {efficiency})")
                
                response = self.make_request('POST', "/bid", json={
                    'powerplant_id': cost,
                    'bid': cost
                })
                self.logger.info(f"Initial bid response: {response.text}")
            else:
                self.logger.info("No affordable plants, passing")
                response = self.make_request('POST', "/bid", json={
                    'bid': -1,
                    'powerplant_id': 0
                })
                self.logger.info(f"Pass response: {response.text}")

    def do_buy_resources(self):
        self.logger.info("Starting buy resources phase")
        state = self.get_game_state()
        resources_needed = {}
        
        for plant in state['my_info']['powerplants']:
            if plant['resource_type'] != 'CLEAN':
                rtype = plant['resource_type'].lower()
                if rtype not in resources_needed:
                    resources_needed[rtype] = 0
                resources_needed[rtype] += plant['resource_cost']
        
        self.logger.info(f"Buying resources: {resources_needed}")
        response = self.make_request('POST', "/buy", json=resources_needed)

    def do_build_generators(self):
        self.logger.info("Starting build generators phase")
        state = self.get_game_state()
        
        try:
            # Get board state
            cities = self.get_city_info()
            self.logger.info(f"Found cities: {list(cities.keys())}")
            self.logger.debug(f"Full city info: {cities}")
            
            # Find cities we can build in
            buildable_cities = self.find_buildable_cities(cities)
            self.logger.info(f"Buildable cities: {buildable_cities}")
            
            # For now, just try direct paths to buildable cities
            paths = [[city] for city in buildable_cities]
            self.logger.info(f"Building paths: {paths}")
            
            if paths:
                response = self.make_request('POST', "/build", json={
                    'paths': paths
                })
                self.logger.info(f"Build response: {response.text}")
            else:
                # Even with no paths, we need to send an empty list to pass the turn
                response = self.make_request('POST', "/build", json={
                    'paths': []
                })
                self.logger.info("No valid paths, passing build phase")
                
        except Exception as e:
            self.logger.error(f"Error during build phase: {e}", exc_info=True)
            # Send empty paths list to pass turn on error
            response = self.make_request('POST', "/build", json={
                'paths': []
            })
            self.logger.info("Error occurred, passing build phase")

    def do_bureaucracy(self):
        self.logger.info("Starting bureaucracy phase")
        state = self.get_game_state()
        
        powerplants = state['my_info'].get('powerplants', [])
        self.logger.info(f"My powerplants: {powerplants}")
        
        # Sort by efficiency
        powerplants = sorted(
            powerplants,
            key=lambda p: p.get('generators', 0) / p.get('resource_cost', 1) if p.get('resource_cost', 1) > 0 else float('inf'),
            reverse=True
        )
        
        # For hybrid plants, check our resource stocks to decide what to use
        has_hybrid = any(p.get('resource_type') == 'HYBRID' for p in powerplants)
        
        if has_hybrid:
            # If we have hybrid plants, count our resources
            resources = state['my_info'].get('resources', {})
            oil_amount = resources.get('OIL', 0)
            gas_amount = resources.get('GAS', 0)
            
            # Use more oil if we have more oil than gas
            num_oil = 2 if oil_amount > gas_amount else 0
            self.logger.info(f"Using {num_oil} oil for hybrid plants (have {oil_amount} oil, {gas_amount} gas)")
            
            powerplant_ids = [p.get('market_cost') for p in powerplants]
            response = self.make_request('POST', "/power", json={
                'powerplants': powerplant_ids,
                'num_oil': num_oil
            })
        else:
            powerplant_ids = [p.get('market_cost') for p in powerplants]
            response = self.make_request('POST', "/power", json={
                'powerplants': powerplant_ids,
                'num_oil': 0  # No hybrid plants, so no oil needed
            })
            
        self.logger.info(f"Power response: {response.text}")

def try_connect(max_retries=5):
    logger = logging.getLogger('AI_Players.connection')
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(server_url + '/player_info')
            logger.info(f"Connected to server, response: {response.status_code}")
            return True
        except requests.exceptions.ConnectionError:
            retries += 1
            logger.warning(f'Connection failed, attempt {retries}/{max_retries}')
            time.sleep(5)
    return False

if __name__ == "__main__":
    logger.info("Starting AI players")
    
    if not try_connect():
        logger.error("Could not connect to server")
        sys.exit(1)

    try:
        # Create all players first
        num_players = 3  # Default to 3 players to ensure game starts
        players = [
            GreedyAI("GreedyAI_1"),
            GreedyAI("GreedyAI_2"),
            ResourceAI("ResourceAI_1")
        ]

        # Wait a bit to ensure game starts
        logger.info("Waiting for game to start...")
        time.sleep(5)
        
        # Keep track of whose turn it is
        last_player = None
        
        # Run all players' turns in sequence
        while True:
            try:
                # Get current turn info once
                turn_info = requests.get(server_url + "/turn_info").json()
                current_player = turn_info.get('current_player')
                
                # Log if turn changed
                if current_player != last_player:
                    logger.info(f"Turn changed from {last_player} to {current_player}")
                    last_player = current_player
                
                # Let each player check if it's their turn
                for player in players:
                    if player.name == current_player:
                        logger.info(f"It's {player.name}'s turn")
                        player.do_turn()
                        break
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error during game loop: {str(e)}", exc_info=True)
                time.sleep(1)
                
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)