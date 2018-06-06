import json
import sys
sys.path.append('../../')
from components.rType import RType


'''
class RType(Enum):
	GAS = 0
	OIL = 1
	COAL = 2
	URANIUM = 3
	HYBRID = 4
	CLEAN = 5
'''

def get_player_count(string):
	if string == "two_players":
		return 2
	elif string == "three_players":
		return 3
	elif string == "four_players":
		return 4
	elif string == "five_players":
		return 5
	elif string == "six_players":
		return 6

def edit_replenish():
	with open("replenish_rate.json", 'r') as f:
		rates = json.load(f)

	new_dict = { "europe" : {}, "usa" : {} }
	for player_num in rates["europe"]:
		rate = rates["europe"][player_num]
		player_int = get_player_count(player_num)
		new_dict["europe"][player_int] = {}
		new_dict["europe"][player_int][RType.COAL.value] = {}
		new_dict["europe"][player_int][RType.OIL.value] = {}
		new_dict["europe"][player_int][RType.GAS.value] = {}
		new_dict["europe"][player_int][RType.URANIUM.value] = {}
		new_dict["europe"][player_int][RType.COAL.value][1] = rate["coal"]["turn_1"]
		new_dict["europe"][player_int][RType.COAL.value][2] = rate["coal"]["turn_2"]
		new_dict["europe"][player_int][RType.COAL.value][3] = rate["coal"]["turn_3"]
		new_dict["europe"][player_int][RType.OIL.value][1] = rate["oil"]["turn_1"]
		new_dict["europe"][player_int][RType.OIL.value][2] = rate["oil"]["turn_2"]
		new_dict["europe"][player_int][RType.OIL.value][3] = rate["oil"]["turn_3"]
		new_dict["europe"][player_int][RType.GAS.value][1] = rate["gas"]["turn_1"]
		new_dict["europe"][player_int][RType.GAS.value][2] = rate["gas"]["turn_2"]
		new_dict["europe"][player_int][RType.GAS.value][3] = rate["gas"]["turn_3"]
		new_dict["europe"][player_int][RType.URANIUM.value][1] = rate["uranium"]["turn_1"]
		new_dict["europe"][player_int][RType.URANIUM.value][2] = rate["uranium"]["turn_2"]
		new_dict["europe"][player_int][RType.URANIUM.value][3] = rate["uranium"]["turn_3"]

		new_dict["usa"][player_int] = {}
		new_dict["usa"][player_int][RType.COAL.value] = {}
		new_dict["usa"][player_int][RType.OIL.value] = {}
		new_dict["usa"][player_int][RType.GAS.value] = {}
		new_dict["usa"][player_int][RType.URANIUM.value] = {}
		new_dict["usa"][player_int][RType.COAL.value][1] = rate["coal"]["turn_1"]
		new_dict["usa"][player_int][RType.COAL.value][2] = rate["coal"]["turn_2"]
		new_dict["usa"][player_int][RType.COAL.value][3] = rate["coal"]["turn_3"]
		new_dict["usa"][player_int][RType.OIL.value][1] = rate["oil"]["turn_1"]
		new_dict["usa"][player_int][RType.OIL.value][2] = rate["oil"]["turn_2"]
		new_dict["usa"][player_int][RType.OIL.value][3] = rate["oil"]["turn_3"]
		new_dict["usa"][player_int][RType.GAS.value][1] = rate["gas"]["turn_1"]
		new_dict["usa"][player_int][RType.GAS.value][2] = rate["gas"]["turn_2"]
		new_dict["usa"][player_int][RType.GAS.value][3] = rate["gas"]["turn_3"]
		new_dict["usa"][player_int][RType.URANIUM.value][1] = rate["uranium"]["turn_1"]
		new_dict["usa"][player_int][RType.URANIUM.value][2] = rate["uranium"]["turn_2"]
		new_dict["usa"][player_int][RType.URANIUM.value][3] = rate["uranium"]["turn_3"]
	with open("better_rates.json", 'w') as f:
		json.dump(new_dict, f, indent=2)

# edit_replenish()