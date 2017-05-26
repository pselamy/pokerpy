import unittest
from itertools import product
from random import randint

from mockito import expect
from mockito import mock

from pokerpy.models import card
from pokerpy.models.card_deck import CardDeck
from pokerpy.models.joker import Joker


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.jokers = [mock(spec=Joker, strict=True) for _ in range(2)]
        self.deck = CardDeck(jokers=self.jokers)

    def test_cards(self):
        expected = [] + list(self.jokers)
        faces = list(str(i) for i in range(1, 11)) + ['Jack', 'Queen', 'King', 'Ace']
        suits = {'club', 'diamond', 'heart', 'spade'}
        for face, suit in product(faces, suits):
            mock_card = mock(spec=card.Card, strict=True)
            expect(card, strict=True, times=1).Card(face=face, suit=suit).thenReturn(mock_card)
            expected.append(mock_card)

        actual = self.deck.cards
        self.assertCountEqual(expected, actual)

    def test_get_card(self):
        cards = set(self.deck.cards)
        actual = self.deck.get_card()
        self.assertIsInstance(actual, card.Card)
        self.assertCountEqual(cards - {actual}, set(self.deck.cards))

    def test_get_cards(self):
        cards = set(self.deck.cards)
        total_card_count = 52 + len(self.jokers)
        count = randint(1, total_card_count + 1)
        actual = set(self.deck.get_cards(count=count))
        self.assertEquals(count, len(actual))
        self.assertTrue(all(isinstance(c, card.Card) for c in actual))
        self.assertCountEqual(cards - actual, set(self.deck.cards))
