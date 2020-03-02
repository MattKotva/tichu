import itertools
from typing import Generator, List, Optional

from deck import Deck, Card
import random

from exceptions import IllegalPlayError
from play import Play
from player import Player, Team


class Game:

    WINNING_SCORE = 1000

    def __init__(self, player_1: Player, player_2: Player, player_3: Player, player_4: Player):
        player_1.next_player = player_2
        player_2.next_player = player_3
        player_3.next_player = player_4
        player_4.next_player = player_1
        self.team1 = Team(player_1, player_3)
        self.team2 = Team(player_2, player_4)

    @property
    def players(self) -> Generator:
        for player in itertools.chain(self.team1, self.team2):
            yield player

    def start(self):
        while self.team1.score < self.WINNING_SCORE and self.team2.score < self.WINNING_SCORE:
            hand = Hand(self)
            hand.play_hand()


class Hand:

    def __init__(self, game: Game):
        self.game = game

    def play_hand(self):
        self.deal_hand()
        self.find_majong()
        self.hand_loop()

    def find_majong(self):
        for player in self.game.players:
            if player.has_majong():
                player.is_turn = True
                break

    def __hand_finished(self):
        players_out = 0
        for player in self.game.players:
            if player.cards_in_hand() == 0:
                players_out += 1
        if players_out == 3:
            return True
        elif self.game.team1.is_out() or self.game.team2.is_out():
            return True
        else:
            return False

    def hand_loop(self):
        while not self.__hand_finished():
            trick = Trick(self)
            trick.play_trick()

    def __deal_cards(self, deck: Deck):
        for player in self.game.players:
            player.add_card(deck.pop())

    def deal_hand(self):
        deck = Deck()
        random.shuffle(deck)
        while len(deck) > 24:
            self.__deal_cards(deck)
        # TODO: Add big tichu call
        while deck:
            self.__deal_cards(deck)


class Trick:

    def __init__(self, hand: Hand):
        self.hand = hand
        self.cards: List[Card] = []
        self.__pass_counter = 0
        self.__last_play: Optional[Play] = None

    def player_passed(self, passed: Optional[bool]):
        if passed:
            self.__pass_counter += 1
        else:
            self.__pass_counter = 0

    @property
    def pass_counter(self):
        return self.__pass_counter

    @property
    def last_play(self):
        return self.__last_play

    @last_play.setter
    def last_play(self, play: Play):
        if play > self.last_play:
            self.__last_play = play
        else:
            raise IllegalPlayError("Illegal Play attempted")

    def find_first_player(self) -> Player:
        for player in self.hand.game.players:
            if player.is_turn:
                return player

    def play_trick(self):
        current_player = self.find_first_player()
        pass_counter = 0
        while pass_counter < 3:
            self.player_plays(current_player)

    def player_plays(self, current_player: Player):
        print(f"Player {current_player}'s turn")
        print(f"{current_player}'s cards:\n {current_player.cards}")
        cards_played = Play(current_player.read_play())
        if cards_played:
            current_player.is_turn = False
            current_player = current_player.next_player
            current_player.is_turn = True
            self.last_play = cards_played
            self.player_passed(False)
        else:
            self.player_passed(True)

    def __iter__(self):
        for card in self.cards:
            yield card


