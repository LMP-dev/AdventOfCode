from pathlib import Path
from enum import Enum, auto

INPUT_FILE = Path(__file__).parent / "input.txt"

class Hand(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

class Result(Enum):
    WIN = auto()
    DRAW = auto()
    LOSE = auto()

DECRYPTION_OPPONENT = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS
}

DECRYPTION_RESULT = {
    "X": Result.LOSE,
    "Y": Result.DRAW,
    "Z": Result.WIN
}

def discover_your_hand(opponent_hand: Hand, result: Result) -> Hand:
    if opponent_hand == Hand.ROCK:
        if result == Result.LOSE:
            return Hand.SCISSORS
        elif result == Result.DRAW:
            return Hand.ROCK
        elif result == Result.WIN:
            return Hand.PAPER
    elif opponent_hand == Hand.PAPER:
        if result == Result.LOSE:
            return Hand.ROCK
        elif result == Result.DRAW:
            return Hand.PAPER
        elif result == Result.WIN:
            return Hand.SCISSORS
    elif opponent_hand == Hand.SCISSORS:
        if result == Result.LOSE:
            return Hand.PAPER
        elif result == Result.DRAW:
            return Hand.SCISSORS
        elif result == Result.WIN:
            return Hand.ROCK

def calculate_score(opponent_hand: Hand, your_hand:Hand) -> int:
    if your_hand == Hand.ROCK:
        shape_score = 1
        if opponent_hand == Hand.ROCK:
            outcome_score = 3
        elif opponent_hand == Hand.PAPER:
            outcome_score = 0
        elif opponent_hand == Hand.SCISSORS:
            outcome_score = 6
    if your_hand == Hand.PAPER:
        shape_score = 2
        if opponent_hand == Hand.ROCK:
            outcome_score = 6
        elif opponent_hand == Hand.PAPER:
            outcome_score = 3
        elif opponent_hand == Hand.SCISSORS:
            outcome_score = 0
    if your_hand == Hand.SCISSORS:
        shape_score = 3
        if opponent_hand == Hand.ROCK:
            outcome_score = 0
        elif opponent_hand == Hand.PAPER:
            outcome_score = 6
        elif opponent_hand == Hand.SCISSORS:
            outcome_score = 3
    return shape_score + outcome_score

def main() -> None:
    total_score = 0
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            opponent, result = line.split()
            opponent_hand = DECRYPTION_OPPONENT[opponent]
            round_result = DECRYPTION_RESULT[result]
            your_hand = discover_your_hand(opponent_hand, round_result)
            total_score += calculate_score(opponent_hand, your_hand)  
    
    print(total_score)

if __name__ == "__main__":
    main()
