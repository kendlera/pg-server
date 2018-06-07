import unittest
from components.market import Market

class TestMarket(unittest.TestCase):

	def test_init(self):
		settings = {"num_players":4}
		market = Market(settings)
		self.assertEqual(len(market.deck), 30)