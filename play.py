from enum import Enum
from typing import List

import deck
from exceptions import IllegalPlayError


class PlayType(Enum):
    '''
    Legal Plays:
        - single card
        - pair
        - consecutive pairs
        - three of a kind
        - full house
        - straight of at least length 5
        - four cards of the same rank (bomb)
        - run of 5 or more in the same suit
    :return:
    '''
    Dog = 0,
    Single = 1,
    Pair = 2,
    ThreeOfAKind = 3,
    ConsecutivePairs = 4,
    FullHouse = 5,
    Straight = 6,
    BombKind = 7,
    BombRun = 8


class Play(list):

    def __init__(self, cards: List[deck.Card]):
        super().__init__()
        self.extend(cards)
        self.play_type = self.determine_playtype()

    def determine_playtype(self) -> PlayType:
        ranks = [card.rank for card in self]
        if len(self) == 1:
            card: deck.Card = self[0]
            if card.name == deck.DOG:
                return PlayType.Dog
            else:
                return PlayType.Single
        elif len(self) == 2:
            return PlayType.Pair
        elif len(self) == 3:
            return PlayType.ThreeOfAKind
        elif len(self) == 4:
            if ranks.count(ranks[0]) != 4:
                return PlayType.ConsecutivePairs
            else:
                return PlayType.BombKind
        elif len(self) == 5:
            if ranks[0] in ranks[1:]:
                return PlayType.FullHouse
            else:
                return PlayType.Straight
        else:
            if ranks.count(ranks[0] == 2):
                return PlayType.ConsecutivePairs
            else:
                suits = set([card.suit for card in self])
                if len(suits) > 1:
                    return PlayType.Straight
                else:
                    return PlayType.BombRun

    def is_legal_play(self) -> bool:
        if self.play_type == PlayType.Single:
            return True
        elif self.play_type == PlayType.Pair:
            return self[0] == self[1]
        elif self.play_type == PlayType.ThreeOfAKind:
            return self[0] == self[1] == self[2]
        elif self.play_type == PlayType.ConsecutivePairs:
            return self.__is_legal_consecutive_pair()
        elif self.play_type == PlayType.FullHouse:
            return self.__is_legal_fullhouse()
        elif self.play_type == PlayType.Straight:
            return self.__is_legal_straight()
        elif self.play_type == PlayType.BombKind:
            return self[0] == self[1] == self[2] == self[3]
        elif self.play_type == PlayType.BombRun:
            # Already checked for number of suits
            return self.__is_legal_straight()
        else:
            # Shouldn't get here
            return False

    def __is_legal_straight(self):
        current = self[0].rank
        for card in self[1:]:
            if card.rank != current + 1:
                return False
            current = card.rank
        return True

    def __is_legal_fullhouse(self):
        for card in self:
            if self.count(card) != 2 or self.count(card) != 3:
                return False
        return True

    def __is_legal_consecutive_pair(self):
        if len(self) % 2 != 0:
            return False
        else:
            for i in range(0, len(self), 2):
                if self[i] != self[i + 1]:
                    return False
                elif i + 1 != len(self) - 1 and self[i].rank != self[i].rank - 1:
                    return False
            return True

    def __gt__(self, other):
        if self.play_type != other.play_type:
            raise IllegalPlayError("Play doesn't match the last play type")
        else:
            if self.play_type == PlayType.Single or self.play_type == PlayType.Pair or \
                    self.play_type == PlayType.ThreeOfAKind or self.play_type == PlayType.ConsecutivePairs:
                return self[0] > other[0]
            if self.play_type == PlayType.FullHouse:
                pass