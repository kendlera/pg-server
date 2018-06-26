import unittest
from components.resources import Resources
from components.rType import RType

class TestResources(unittest.TestCase):

	def test_json_load(self):
		'''
		Make sure we loaded in json correctly
		'''
		settings = {"num_players":4, "board_type": "europe"}
		elem = Resources(settings)
		self.assertIsNotNone(elem.slots)
		self.assertEqual(len(elem.slots), 9)

	def test_how_much(self):
		settings = {"num_players":4, "board_type": "europe"}
		elem = Resources(settings)

		cost1 = elem.cost_to_buy(RType.GAS, 3)
		self.assertEqual(cost1, 9)

		cost2 = elem.cost_to_buy(RType.OIL, 9)
		self.assertEqual(cost2, 43)

		cost3 = elem.cost_to_buy(RType.CLEAN, 4)
		self.assertEqual(cost3, 0)
