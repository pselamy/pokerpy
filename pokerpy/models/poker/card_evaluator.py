from collections import Counter
from itertools import groupby, combinations
from operator import itemgetter

from pokerpy.models.common.rank import Rank
from pokerpy.models.poker.hand import Hand


class CardEvaluator(object):
    @staticmethod
    def __get_four_of_a_kind(cards, rank_counter):
        four_of_a_kind = [c for c in cards if rank_counter[c.rank] == 4]
        return (Hand.FOUR_OF_A_KIND, four_of_a_kind) if four_of_a_kind else None

    @staticmethod
    def __get_full_house(cards, rank_counter):
        is_full_house = {2, 3} - set(rank_counter.values()) == set()
        return (Hand.FULL_HOUSE, cards) if is_full_house else None

    @staticmethod
    def __get_pairs(cards, rank_counter):
        pairs = [c for c in cards if rank_counter[c.rank] == 2]
        if not pairs:
            return None

        pair_count = len(pairs) / 2
        return Hand.TWO_PAIR if pair_count == 2 else Hand.PAIR, pairs

    @staticmethod
    def __get_straight_flush(cards):
        if set(card.rank for card in cards) == {Rank.ACE, Rank.KING, Rank.QUEEN, Rank.JACK, Rank.TEN}:
            return Hand.ROYAL_FLUSH, cards

        return Hand.STRAIGHT_FLUSH, cards

    @staticmethod
    def __get_three_of_a_kind(cards, rank_counter):
        three_of_a_kind = [c for c in cards if rank_counter[c.rank] == 3]
        if not three_of_a_kind:
            return None

        return Hand.THREE_OF_A_KIND, three_of_a_kind

    @staticmethod
    def __is_flush(cards):
        return len(cards) == 5 and all(card.suit == cards[0].suit for card in cards[1:])

    @staticmethod
    def __is_straight(cards):
        ranks = sorted((card.rank for card in cards), key=lambda rank: rank.value)
        for k, g in groupby(enumerate(ranks), lambda x: x[0] - x[1].value):
            straight = set(map(itemgetter(1), g))
            if len(straight) == 5:
                return True

        return False

    def get_best_hand(self, cards):
        return sorted(self.get_possible_hands(cards=cards), key=lambda hand_data: hand_data[0].value)[-1]

    def get_hand(self, cards):
        is_flush = self.__is_flush(cards=cards)
        is_straight = self.__is_straight(cards=cards)
        if is_flush and is_straight:
            return self.__get_straight_flush(cards)

        rank_counter = Counter(card.rank for card in cards)
        return next((tuple(hand_data)
                     for hand_data in (self.__get_four_of_a_kind(cards=cards, rank_counter=rank_counter),
                                       self.__get_full_house(cards=cards, rank_counter=rank_counter),
                                       (Hand.FLUSH, cards) if is_flush else None,
                                       (Hand.STRAIGHT, cards) if is_straight else None,
                                       self.__get_three_of_a_kind(cards=cards, rank_counter=rank_counter),
                                       self.__get_pairs(cards=cards, rank_counter=rank_counter))
                     if hand_data), (Hand.HIGH_CARD, [cards[0]]))

    def get_possible_hands(self, cards):
        return map(self.get_hand, combinations(cards, 5))
