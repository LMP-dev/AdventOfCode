from enum import Enum, auto
from typing import Protocol, Iterable


class HandType(Enum):
    HIGHCARD = auto()
    PAIR = auto()
    TWOPAIR = auto()
    TRIPLE = auto()
    FULLHOUSE = auto()
    POKER = auto()
    REPOKER = auto()


class Hand(Protocol):
    def points(self) -> int:
        ...


class HighCardHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        ...

    def points(self) -> int:
        ...


class PairHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        ...

    def points(self) -> int:
        ...


class TwoPairHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        ...

    def points(self) -> int:
        ...


class TripleHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        self.triple_card: int = None
        self.high_card: int = None
        self.low_card: int = None

        for card in hand:
            if 3 == hand.count(card):
                self.triple_card = card
            elif 1 == hand.count(card):
                ### TODO
                ...

    def points(self) -> int:
        ...


class FullHouseHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        self.triple_card: int = None
        self.pair_card: int = None

        for card in hand:
            if 3 == hand.count(card):
                self.triple = card
            elif 2 == hand.count(card):
                self.pair_card = card
            if self.triple_card and self.pair_card:
                break

    def points(self) -> int:
        ...


class PokerHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        self.poker_card: int = None
        self.high_card: int = None

        for card in hand:
            if 4 == hand.count(card):
                self.poker = card
            elif 1 == hand.count(card):
                self.high_card = card
            if self.poker and self.high_card:
                break

    def points(self) -> int:
        ...


class RePokerHand:
    def __init__(self, hand: tuple[int, int, int]) -> None:
        self.reporker_card = hand[0]

    def points(self) -> int:
        ...


def convert_to_numerical_hand(hand: str) -> tuple[int, int, int, int, int]:
    mapping = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    converted_hand = []
    for card in hand:
        converted_hand.append(mapping[card])
    return tuple(converted_hand)


def find_hand_category(hand: Iterable) -> HandType:
    counting = [hand.count(x) for x in hand]
    if 5 in counting:
        return HandType.REPOKER
    elif 4 in counting:
        return HandType.POKER
    elif 3 in counting:
        if 2 in counting:
            return HandType.FULLHOUSE
        else:
            return HandType.TRIPLE
    elif 2 in counting:
        if 2 == counting.count(2):
            return HandType.TWOPAIR
        else:
            return HandType.PAIR
    elif 1 in counting:
        return HandType.HIGHCARD


def create_hand_object(
    hand: tuple[int, int, int, int, int], hand_type: HandType
) -> Hand:
    if hand_type == HandType.HIGHCARD:
        return HighCardHand(hand)
    elif hand_type == HandType.PAIR:
        return PairHand(hand)
    elif hand_type == HandType.TWOPAIR:
        return TwoPairHand(hand)
    elif hand_type == HandType.TRIPLE:
        return TripleHand(hand)
    elif hand_type == HandType.FULLHOUSE:
        return FullHouseHand(hand)
    elif hand_type == HandType.POKER:
        return PokerHand(hand)
    elif hand_type == HandType.REPOKER:
        return RePokerHand(hand)
    else:
        raise Exception("Not found known hand type!")
