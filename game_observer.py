import requests
import time
import json
from datetime import datetime
from tabulate import tabulate
import colorama
from colorama import Fore, Back, Style

# Configuration
SERVER_HOST = "http://127.0.0.1"
SERVER_PORT = ":5050"
server_url = SERVER_HOST + SERVER_PORT

def format_money(amount):
    return f"{Fore.GREEN}${amount}{Style.RESET_ALL}"

def format_resources(resources):
    colors = {
        'COAL': Fore.BLACK + Back.WHITE,
        'OIL': Fore.BLACK + Back.YELLOW,
        'GAS': Fore.BLUE + Back.WHITE,
        'URANIUM': Fore.GREEN + Back.WHITE,
    }
    result = []
    for rtype, amount in resources.items():
        color = colors.get(rtype, '')
        result.append(f"{color}{rtype}:{amount}{Style.RESET_ALL}")
    return " ".join(result)

def format_plant(plant):
    rtype = plant.get('resource_type', 'UNKNOWN')
    colors = {
        'COAL': Fore.BLACK + Back.WHITE,
        'OIL': Fore.BLACK + Back.YELLOW,
        'GAS': Fore.BLUE + Back.WHITE,
        'URANIUM': Fore.GREEN + Back.WHITE,
        'CLEAN': Fore.WHITE + Back.GREEN,
        'HYBRID': Fore.WHITE + Back.MAGENTA
    }
    color = colors.get(rtype, '')
    return f"{color}P{plant['market_cost']}{Style.RESET_ALL}"

def get_game_state():
    """Get all game state information"""
    try:
        turn_info = requests.get(server_url + "/turn_info").json()
        market = requests.get(server_url + "/market").json()
        players = requests.get(server_url + "/player_info").json()
        auction = requests.get(server_url + "/auction").json()
        resources = requests.get(server_url + "/resources").json()
        
        return {
            'turn_info': turn_info,
            'market': market,
            'players': players.get('info', []),
            'auction': auction,
            'resources': resources
        }
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def print_phase_info(state):
    turn_info = state['turn_info']
    if 'msg' in turn_info:
        print(f"{Fore.YELLOW}{turn_info['msg']}{Style.RESET_ALL}")
        return False
        
    current = turn_info['current_player']
    phase = turn_info['phase']
    print(f"{Fore.CYAN}{current}{Style.RESET_ALL} → {Fore.YELLOW}{phase}{Style.RESET_ALL}")
    return True

def print_auction_state(state):
    market = state['market']
    auction = state['auction']
    
    # Print current market (just first row)
    current = market.get('current_market', [])
    if current:
        plants = [format_plant(p) for p in current[:4]]
        print(f"Market: {' '.join(plants)}")
    
    # Print auction if active
    if auction.get('auction_in_progress'):
        plant = auction.get('powerplant', {})
        if plant:
            print(f"Auction: {format_plant(plant)} at {format_money(auction['current_bid'])}")

def print_resources_state(state):
    resources = state['resources']
    if 'msg' in resources:
        return
        
    # Just show the cheapest available of each type
    cheapest = {}
    for rtype, buckets in resources.items():
        for cost, capacity, amount in buckets:
            if amount > 0:
                cheapest[rtype] = cost
                break
    
    if cheapest:
        parts = []
        for rtype, cost in cheapest.items():
            colors = {
                'COAL': Fore.BLACK + Back.WHITE,
                'OIL': Fore.BLACK + Back.YELLOW,
                'GAS': Fore.BLUE + Back.WHITE,
                'URANIUM': Fore.GREEN + Back.WHITE,
            }
            color = colors.get(rtype, '')
            parts.append(f"{color}{rtype}:{format_money(cost)}{Style.RESET_ALL}")
        print(f"Resources: {' '.join(parts)}")

def print_player_state(state, active_player=None):
    players = state['players']
    
    headers = ["Player", "$", "Resources", "Plants"]
    rows = []
    
    for player in players:
        name = player['name']
        prefix = "→ " if name == active_player else "  "
        money = format_money(player['money'])
        resources = format_resources(player['resources'])
        plants = " ".join(format_plant(p) for p in player['powerplants'])
        if not plants:
            plants = "-"
            
        rows.append([prefix + name, money, resources, plants])
    
    print(tabulate(rows, headers=headers, tablefmt="simple"))

def main():
    colorama.init()
    print(f"{Fore.GREEN}Starting Game Observer...{Style.RESET_ALL}")
    
    while True:
        try:
            # Clear screen (platform independent)
            print("\033[H\033[J", end="")
            
            # Get and print game state
            state = get_game_state()
            if state:
                print(f"{Back.BLUE}{datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
                
                if print_phase_info(state):
                    active_player = state['turn_info']['current_player']
                    phase = state['turn_info']['phase']
                    
                    # Show relevant info based on phase
                    if phase == 'AUCTION':
                        print_auction_state(state)
                    elif phase == 'BUY_RESOURCES':
                        print_resources_state(state)
                        
                    print()  # Blank line before player state
                    print_player_state(state, active_player)
            
            # Wait before next update
            time.sleep(1)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Stopping observer...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()