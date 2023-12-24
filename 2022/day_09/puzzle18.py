from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
# INPUT_FILE = Path(__file__).parent / "large_test_input.txt"


def update_head_pos(direction: str, head: tuple[int]) -> tuple[int]:
    """Returns the updated head position"""
    xh, yh = head
    if direction == "R":
        head = (xh + 1, yh)
    elif direction == "L":
        head = (xh - 1, yh)
    elif direction == "U":
        head = (xh, yh + 1)
    elif direction == "D":
        head = (xh, yh - 1)
    return head


def update_tail_pos(head: tuple[int], tail: tuple[int]) -> tuple[int]:
    xh, yh = head
    xt, yt = tail
    # WS, W, WN
    if xh < xt - 1:
        if yh < yt:
            tail = (xt - 1, yt - 1)
        elif yh == yt:
            tail = (xt - 1, yt)
        elif yh > yt:
            tail = (xt - 1, yt + 1)
    # NW, N, NE
    if yh > yt + 1:
        if xh < xt:
            tail = (xt - 1, yt + 1)
        elif xh == xt:
            tail = (xt, yt + 1)
        elif xh > xt:
            tail = (xt + 1, yt + 1)
    # ES, E, EN
    if xh > xt + 1:
        if yh < yt:
            tail = (xt + 1, yt - 1)
        elif yh == yt:
            tail = (xt + 1, yt)
        elif yh > yt:
            tail = (xt + 1, yt + 1)
    # SW, S, SE
    elif yh < yt - 1:
        if xh < xt:
            tail = (xt - 1, yt - 1)
        elif xh == xt:
            tail = (xt, yt - 1)
        elif xh > xt:
            tail = (xt + 1, yt - 1)
    return tail


def move_rope(
    direction: str, steps: int, rope: list[tuple[int]]
) -> tuple[list[tuple[int]], list[tuple[int]]]:
    tail_positions = list()
    for _ in range(steps):
        rope[0] = update_head_pos(direction, rope[0])
        for i, knot in enumerate(rope[1:]):
            rope[i + 1] = update_tail_pos(rope[i], knot)
        tail_positions.append(rope[-1])
    return rope, tail_positions


def main() -> None:
    rope = [
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
    ]  # x axis lef and right, y axis up and down
    tail_positions = list()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            dir, steps = line.split()
            rope, t_positions = move_rope(dir, int(steps), rope)
            tail_positions.extend(t_positions)
    tail_unique_positions = set(tail_positions)
    print(len(tail_unique_positions))


if __name__ == "__main__":
    main()
