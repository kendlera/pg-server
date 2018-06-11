import unittest
from components.board import Board

class TestBoard(unittest.TestCase):

	def test_init(self):
		'''
		make sure we can load the board without error
		'''
		settings = {}
		board = Board(settings)


	def test_path_cost(self):
		board = Board({})
		path1 = ["Kharkiv", "Kyjiv", "Budapest", "Bucuresti"]
		path1_cost = board.cost_of_path(path1)
		self.assertEqual(path1_cost, 46)

		path2 = ["Kyjiv"]
		path2_cost = board.cost_of_path(path2)
		self.assertEqual(path2_cost, 0)

		path3 = ["Paris", "Bordeaux", "Zurich"]
		path3_cost = board.cost_of_path(path3)
		self.assertEqual(path3_cost, -1)

		path4_cost = board.cost_of_path([])
		self.assertEqual(path4_cost, 0)

	def test_city_cost(self):
		board = Board({})
		city1_cost = board.cost_of_city("Zurich")
		self.assertEqual(city1_cost, 10)

		city2_cost = board.cost_of_city("Abcdef")
		self.assertEqual(city2_cost, -1)

		board.update_cost("Zurich")
		city3_cost = board.cost_of_city("Zurich")
		self.assertEqual(city3_cost, 15)

		board.update_cost("Zurich")
		board.update_cost("Zurich")
		city4_cost = board.cost_of_city("Zurich")
		self.assertEqual(city4_cost, -1)

	def test_purchasing(self):
		board = Board({})
		player_id = "xxx"
		cost1 = board.player_purchase(player_id, ["Kharkiv"])
		self.assertEqual(cost1, 10)

		cost2 = board.player_purchase(player_id, ["Kharkiv", "Kyjiv"])
		self.assertEqual(cost2, 19)

		cost3 = board.player_purchase(player_id, ["Kyjiv", "Budapest"])
		self.assertEqual(cost3, 31)

		cities = board.cities_owned_by_player(player_id)
		self.assertTrue("Kharkiv" in cities)
		self.assertTrue("Kyjiv" in cities)
		self.assertTrue("Budapest" in cities)
		self.assertEqual(len(cities), 3)

