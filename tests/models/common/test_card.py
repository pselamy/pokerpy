import unittest
from _ast import Constant
from random import choice

from pokerpy.models.common.card import Card
from pokerpy.models.common.rank import Rank
from pokerpy.models.common.suit import Suit


class TestCard(unittest.TestCase):
    def setUp(self):
        self.constants = Constant()
        self.rank = choice(list(Rank))
        self.suit = choice(list(Suit))
        self.card = Card(rank=self.rank, suit=self.suit)

    def test_rank(self):
        self.assertEquals(self.rank, self.card.rank)

    def test_suit(self):
        self.assertEquals(self.suit, self.card.suit)
