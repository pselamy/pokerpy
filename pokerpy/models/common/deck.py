from pokerpy.models.common.card.rank import Rank
from pokerpy.models.common.card.suit import Suit

from pokerpy.models.common import card


class Deck(object):
    def __init__(self):
        self.cards = [card.Card(rank=rank, suit=suit) for suit in Suit for rank in Rank]
