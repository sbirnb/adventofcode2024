from collections import defaultdict, Counter
from typing import Iterable, Sequence, Mapping


def parse_input(input_: Iterable[str]) -> Sequence[int]:
    return tuple(map(int,next(iter(input_)).strip().split()))


def get_next_stones(stone: int) -> Iterable[int]:
    if stone == 0:
        return (1,)
    elif (l := len(s := str(stone))) % 2 == 0:
        return (int(s[:l//2]), int(s[l//2:]))
    else:
        return (stone * 2024,)


def get_next_state(state: Mapping[int, int]) -> Mapping[int, int]:
    next_state = defaultdict(int)
    for stone, qty in state.items():
        for next_stone in get_next_stones(stone):
            next_state[next_stone] += qty
    return next_state


def get_stones_after(state0: Mapping[int, int], iterations: int) -> int:
    state = state0
    for _ in range(iterations):
        state = get_next_state(state)
    return sum(state.values())


def part1(input_: Iterable[str]) -> int:
    return get_stones_after(Counter(parse_input(input_)), 25)


def part2(input_: Iterable[str]) -> int:
    return get_stones_after(Counter(parse_input(input_)), 75)


if __name__ == '__main__':
    with open('../../data/d11.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
