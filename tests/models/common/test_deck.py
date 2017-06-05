import unittest
from itertools import product

from mockito import mock

from pokerpy.models.common.card import Card
from pokerpy.models.common.deck import Deck
from pokerpy.models.common.rank import Rank
from pokerpy.models.common.suit import Suit


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.cards = [mock(dict(rank=rank, suit=suit), spec=Card, strict=True) for rank, suit in product(Rank, Suit)]
        self.deck = Deck(cards=self.cards)

    def test_cards(self):
        self.assertCountEqual(self.cards, self.deck.cards)
