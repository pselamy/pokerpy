from itertools import product

from pokerpy.models.common.card import Card
from pokerpy.models.common.rank import Rank
from pokerpy.models.common.suit import Suit


class Deck(object):
    def __init__(self, cards):
        self.__cards = cards
