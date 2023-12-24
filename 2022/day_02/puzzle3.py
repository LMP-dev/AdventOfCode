from pathlib import Path
from enum import Enum, auto

INPUT_FILE = Path(__file__).parent / "input.txt"

class Hand(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

DECRYPTION_OPPONENT = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS
}

DECRYPTION_YOURS = {
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS
}

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
            opponent, you = line.split()
            opponent_hand = DECRYPTION_OPPONENT[opponent]
            your_hand = DECRYPTION_YOURS[you]  
            total_score += calculate_score(opponent_hand, your_hand)  
    
    print(total_score)

if __name__ == "__main__":
    main()
