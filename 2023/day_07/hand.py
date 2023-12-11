from enum import Enum, auto
from typing import Protocol


class HandType(Enum):
    NORMAL = auto()
    PAIR = auto()
    TWOPAIR = auto()
    TRIPLE = auto()
    FULLHOUSE = auto()
    POKER = auto()
    REPOKER = auto()


class Hand(Protocol):
    def get_points(self) -> int:
        ...


class NormalHand:
    ...


class PairHand:
    ...


class TwoPairHand:
    ...


class TripletHand:
    ...


class FullHouseHand:
    ...


class PokerHand:
    ...


class RePokerHand:
    ...


def create_hand_object(
    hand: tuple[int, int, int, int, int], hand_type: HandType
) -> Hand:
    if hand_type == hand.HandType.NORMAL:
        ...
    elif hand_type == hand.HandType.PAIR:
        ...
    elif hand_type == hand.HandType.TWOPAIR:
        ...
    elif hand_type == hand.HandType.TRIPLE:
        ...
    elif hand_type == hand.HandType.FULLHOUSE:
        ...
    elif hand_type == hand.HandType.POKER:
        ...
    elif hand_type == hand.HandType.REPOKER:
        ...
    else:
        raise Exception("Not found known hand type!")
    return
