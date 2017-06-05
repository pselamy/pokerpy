import unittest
from itertools import combinations, groupby, count
from operator import itemgetter
from random import choice

from mockito import expect
from mockito import mock

from pokerpy.models.common.card import Card
from pokerpy.models.common.rank import Rank
from pokerpy.models.common.suit import Suit
from pokerpy.models.poker.card_evaluator import CardEvaluator
from pokerpy.models.poker.hand import Hand


class TestCardEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = CardEvaluator()
        self.hands = list(h for h in Hand)
        self.ranks = list(r for r in Rank)
        self.suits = list(s for s in Suit)
        self.cards = {rank: [mock(dict(rank=rank, suit=suit), spec=Card) for suit in self.suits] for rank in self.ranks}

    def __get_all_hands(self):
        for hand in self.hands:
            yield hand, self.__get_cards(hand_name=hand.name)

    def __get_cards(self, hand_name, **kwargs):
        return getattr(self, 'get_test_{0}'.format(hand_name.lower()))(**kwargs)

    def get_straight_ranks(self):
        for k, g in groupby(enumerate(sorted(self.cards.keys(), key=lambda rank: rank.value)),
                            key=lambda x: x[0] - x[1].value):
            ranks = list(map(itemgetter(1), g))
            if len(ranks) >= 5:
                return ranks[:5]

    def get_test_flush(self):
        suit = choice(self.suits)
        ranks = choice(list(combinations(self.ranks, 5)))
        return [mock(dict(rank=rank, suit=suit), spec=Card) for rank in ranks]

    def get_test_four_of_a_kind(self, rank=None):
        if rank is None:
            rank = next(k for k, v in self.cards.items() if len(v) == 4)

        return self.cards.pop(rank)

    def get_test_full_house(self):
        return self.get_test_pair() + self.get_test_three_of_a_kind()

    def get_test_high_card(self):
        return [self.cards[choice(list(k for k, v in self.cards.items() if v))].pop()]

    def get_test_pair(self):
        rank = next(k for k, v in self.cards.items() if len(v) >= 2)
        return [card for card in [self.cards[rank].pop() for _ in range(2)]]

    def get_test_royal_flush(self):
        return [self.cards[rank].pop() for rank in [Rank.ACE, Rank.KING, Rank.QUEEN, Rank.JACK, Rank.TEN]]

    def get_test_straight(self):
        return [self.cards[rank].pop(self.cards[rank].index(choice(self.cards[rank])))
                for rank in self.get_straight_ranks()]

    def get_test_straight_flush(self):
        straight_flush = [self.cards[rank].pop() for rank in self.get_straight_ranks()]
        return straight_flush

    def get_test_three_of_a_kind(self):
        rank = next(k for k, v in self.cards.items() if len(v) >= 3)
        return [card for card in [self.cards[rank].pop() for _ in range(3)]]

    def get_test_two_pair(self):
        return self.get_test_pair() + self.get_test_pair()

    def test_get_best_hand(self):
        hands = sorted(((hand, tuple(cards)) for hand, cards in self.__get_all_hands()
                        if choice([True, False])), key=lambda hand_cards: hand_cards[0].value)
        expected = hands[-1]
        cards = [c for hand, cards in hands for c in cards]
        expect(self.evaluator, strict=True, times=1).get_possible_hands(cards=cards).thenReturn(hands)
        actual = self.evaluator.get_best_hand(cards=cards)
        self.assertEquals(expected, actual)

    def test_get_hand(self):
        for expected in self.__get_all_hands():
            hand, cards = expected
            actual = self.evaluator.get_hand(cards=cards)
            self.assertEquals(expected, actual)

    def test_get_possible_hands(self):
        card_count = count()
        cards = [c for rank, cards in self.cards.items()
                 for c in cards if choice([True, False]) and next(card_count) < 7]
        expected = []
        for combination in combinations(cards, 5):
            hand = choice(self.hands)
            expect(self.evaluator, strict=True, times=1).get_hand(
                    combination).thenReturn(hand, combination)
            expected.append(hand)

        actual = self.evaluator.get_possible_hands(cards=cards)
        self.assertCountEqual(expected, actual)
