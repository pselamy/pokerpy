import unittest
from itertools import product
from random import randint

from mockito import mock

from pokerpy.common.constant import Constant
from pokerpy.models.common import card
from pokerpy.models.common.deck import Deck


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.constants = Constant()
        self.cards = set(self.__get_test_cards())
        self.deck = Deck(cards=self.cards)

    def __get_test_cards(self):
        for face, suit in product(self.constants.FACES, self.constants.SUITS):
            yield mock(dict(face=face, suit=suit), spec=card.Card, strict=True)

    def test_draw_card(self):
        actual = self.deck.draw_card()
        self.assertIsInstance(actual, card.Card)
        self.assertCountEqual(self.cards - {actual}, self.deck.cards)

    def test_draw_cards(self):
        count = randint(1, len(self.cards))
        actual = set(self.deck.draw_cards(count=count))
        self.assertEquals(count, len(actual))
        self.assertTrue(all(isinstance(a, card.Card) and a not in self.deck.cards for a in actual))
        self.assertCountEqual(self.cards - actual, self.deck.cards)
