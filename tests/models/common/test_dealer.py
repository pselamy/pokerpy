import unittest

from mockito import expect
from mockito import mock
from mockito import verify
from mockito import verifyNoMoreInteractions

from pokerpy.models.common.card import Card
from pokerpy.models.common.deck import Deck
from pokerpy.models.common.dealer import Dealer
from pokerpy.models.common.player import Player


class TestDealer(unittest.TestCase):
    def setUp(self):
        self.deck = mock(spec=Deck)
        self.dealer = Dealer(deck=self.deck)

    def test_deal_card(self):
        card = mock(spec=Card, strict=True)
        player = mock(spec=Player, strict=True)
        expect(self.deck, strict=True, times=1).draw_card().thenReturn(card)
        expect(player, strict=True, times=1).receive_card(card=card)
        self.dealer.deal_card(player=player)
        verify(self.deck, times=1).draw_card()
        verify(player, times=1).receive_card(card=card)
        verifyNoMoreInteractions(self.deck)
        verifyNoMoreInteractions(player)
