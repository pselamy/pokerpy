import random
import unittest
from itertools import product

from mockito import expect
from mockito import mock
from mockito import verify
from mockito import verifyNoMoreInteractions

from pokerpy.models.common.card import Card
from pokerpy.models.common.deck import Deck
from pokerpy.models.common.rank import Rank
from pokerpy.models.common.suit import Suit


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.cards = [mock(dict(rank=rank, suit=suit), spec=Card, strict=True) for rank, suit in product(Rank, Suit)]
        self.deck = Deck(cards=self.cards)

    def test_draw_card(self):
        expected = random.choice(self.cards)
        expect(self.deck, strict=True, times=1).draw_cards(count=1).thenReturn([expected])
        actual = self.deck.draw_card()
        self.assertIs(expected, actual)
        verify(self.deck, times=1).draw_cards(count=1)
        verifyNoMoreInteractions(self.deck)

    def test_draw_cards(self):
        count = random.randint(1, 5)
        expected = self.cards[-count:]
        actual = self.deck.draw_cards(count=count)
        self.assertCountEqual(expected, actual)

    def test_shuffle_cards(self):
        expect(random, strict=True, times=1).shuffle(self.cards)
        self.deck.shuffle_cards()
        verify(random, times=1).shuffle(self.cards)
        verifyNoMoreInteractions(random)

    def test_sort_cards(self):
        expected = sorted(self.cards, key=lambda card: (card.suit.value, card.rank.value))
        self.deck.sort_cards()
        self.assertEquals(expected, self.cards)
