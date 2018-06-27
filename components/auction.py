

class Auction:
	'''
	Decided to make an Auction class rather than implement it as part of the Market 

	Reasoning: that the auction is something that affects the content of the Market, but
	is a separate event that happens
	'''

	def __init__(self):
		self.auction_in_progress = False
		self.current_bid = 0
		self.currently_for_bid = 0	# the market price of the powerplant currently for bid 
		self.winning_bidder = None  # the player_id of the player who submitted the last bid 
		self.can_bid = [] 			# list of players who are still bidding on this powerplant
		self.current_bidder = 0 
		self.to_be_trashed = 0 		# the market price of the powerplant owned by the winning_bidder to be trashed if won

	def advance_bid(self):
		self.current_bidder = (self.current_bidder + 1) % len(self.can_bid)

	def get_current_bidder(self):
		return self.can_bid[self.current_bidder]