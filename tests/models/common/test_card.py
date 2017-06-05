import unittest
from random import choice

from pokerpy.common.constant import Constant
from pokerpy.models.common.card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.constants = Constant()
        self.face = choice(list(self.constants.FACES))
        self.suit = choice(list(self.constants.SUITS))
        self.card = Card(face=self.face, suit=self.suit)

    def test_face(self):
        self.assertEquals(self.face, self.card.face)

    def test_suit(self):
        self.assertEquals(self.suit, self.card.suit)
