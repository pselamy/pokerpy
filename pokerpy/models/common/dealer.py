from random import shuffle

from pokerpy.models.common.player import Player


class Dealer(Player):
    def __init__(self, deck):
        self._deck = deck
        self.__sort_attributes = ['suit', 'rank']
        super().__init__()

    def deal_card(self, player):
        player.receive_card(card=self._deck.draw_card())

    def shuffle_deck(self):
        shuffle(self._deck.cards)

    def sort_deck(self):
        self._deck.cards.sort(key=lambda card: tuple(getattr(card, attr) for attr in self.__sort_attributes))
