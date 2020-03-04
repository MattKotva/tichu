from typing import Optional

suits = ("Hearts", "Spades", "Clubs", "Diamonds")

JACK = "Jack"
QUEEN = "Queen"
KING = "King"
ACE = "Ace"
DRAGON = "Dragon"
MAHJON = "Mahjon"
DOG = "Dog"
PHOENIX = "Phoenix"

CARD_RANKS = {
    JACK: 11,
    QUEEN: 12,
    KING: 13,
    ACE: 14,
    DRAGON: 15,
    MAHJON: 1,
    DOG: 0,
    PHOENIX: 1.5
}


class Card:

    def __init__(self, name: str, rank: float, suit: Optional[str] = None):
        self.__rank = rank
        self.__name = name
        self.__suit = suit
        self.__point_value = None

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    @property
    def name(self):
        return self.__name

    @property
    def point_value(self):
        return self.__point_value

    @point_value.setter
    def point_value(self, value: int):
        self.__point_value = value

    def __hash__(self):
        return hash((self.rank, self.name, self.suit))

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __repr__(self) -> str:
        return f"[{self.name}, {self.suit}]"


class SpecialCard(Card):

    def __init__(self, name: str, rank: float, point_value: Optional[int] = None):
        super().__init__(name, rank, None)
        self.point_value = point_value

    def __repr__(self) -> str:
        return f"[{self.name}]"


class Deck(list):

    def __init__(self):
        super().__init__()
        self.extend([Card(str(rank), rank=rank, suit=suit) for rank in range(2, 11) for suit in suits])
        self.extend([Card(name, rank=CARD_RANKS[name], suit=suit) for name in (JACK, QUEEN, KING, ACE) for suit in suits])
        for card in self:
            if card.rank == 5 or card.rank == 10:
                card.point_value = card.rank
            elif card.name == KING:
                card.point_value = 10
        self.append(SpecialCard(MAHJON, rank=1))
        self.append(SpecialCard(DOG, rank=CARD_RANKS[DOG]))
        self.append(SpecialCard(PHOENIX, rank=CARD_RANKS[PHOENIX], point_value=-25))
        self.append(SpecialCard(DRAGON, rank=CARD_RANKS[DRAGON], point_value=25))

