import random


class Deck(object):
    def __init__(self, cards):
        self.__cards = cards

    def draw_card(self):
        return next(iter(self.draw_cards(count=1)))

