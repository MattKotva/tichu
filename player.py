from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple

from deck import Card, CARD_RANKS, MAHJON
import game


class Player(ABC):

    def __init__(self, name):
        self.name = name
        self.cards: List[Card] = []
        self.partner: Optional[Player] = None
        self.tricks_taken: Set[game.Trick] = set()
        self.is_turn: bool = False
        self.__tichu_called = False
        self.__big_tichu_called = False
        self.next_player: Optional[Player] = None

    def add_card(self, card: Card):
        self.cards.append(card)

    def play_cards(self, cards: List[Card]):
        for card in cards:
            self.cards.remove(card)
        return cards

    def reset(self):
        self.cards = set()
        self.tricks_taken = set()
        self.is_turn = False

    @property
    def tichu_called(self):
        return self.__tichu_called

    def call_tichu(self):
        if self.cards_in_hand() == 14:
            self.__tichu_called = True

    def tally_card_points(self):
        points = 0
        for trick in self.tricks_taken:
            for card in trick:
                points += card.point_value
        return points

    def has_majong(self):
        for card in self.cards:
            if card.rank == CARD_RANKS[MAHJON]:
                return True
        return False

    def cards_in_hand(self):
        return len(self.cards)

    @abstractmethod
    def read_play(self):
        pass

    def __repr__(self):
        return self.name


class HumanPlayer(Player):

    def read_play(self):
        card_indexes = input("Choose cards by index to play or pass\n")
        if card_indexes == 'pass':
            return
        try:
            cards = [self.cards[int(index)] for index in card_indexes.split(',')]
        except (TypeError, ValueError):
            print("Invalid selection. Select again:")
            return self.read_play()
        return self.play_cards(cards)


class AIPlayer(Player):

    def read_play(self):
        pass


class Team:

    def __init__(self, player_1: Player, player_2: Player):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score = 0

    def add_player_card_scores(self):
        self.score += self.player_1.tally_card_points()
        self.score += self.player_2.tally_card_points()

    def players(self) -> Tuple[Player, Player]:
        return self.player_1, self.player_2

    def is_out(self) -> bool:
        if self.player_1.cards_in_hand() == 0 and self.player_2.cards_in_hand() == 0:
            return True
        else:
            return False

    def __iter__(self):
        for player in (self.player_1, self.player_2):
            yield player
