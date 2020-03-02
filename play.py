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
            suits = set([card.suit for card in self])
            if len(suits) > 1:
                return PlayType.Straight
            else:
                return PlayType.BombRun

    def is_legal_play(self):
        if self.play_type == PlayType.Single:
            return True
        elif self.play_type == PlayType.Pair:
            if self[0] == self[1]:
                return True
        elif self.play_type == PlayType.ThreeOfAKind:
            if self[0] == self[1] == self[2]:
                return True
        ...

    def __gt__(self, other):
        if self.play_type != other.play_type:
            raise IllegalPlayError("Play doesn't match the last play type")
        ...