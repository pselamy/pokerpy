import random


class Deck(object):
    def __init__(self, cards):
        self.__cards = cards

    def draw_card(self):
        return next(iter(self.draw_cards(count=1)))

    def draw_cards(self, count):
        for i in range(count):
            yield self.__cards.pop()

    def shuffle_cards(self):
        random.shuffle(self.__cards)

