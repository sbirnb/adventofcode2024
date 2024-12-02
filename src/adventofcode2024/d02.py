from collections import defaultdict
from typing import Iterable, Sequence


def parse_input(input_: Iterable[str]) -> Iterable[Sequence[int]]:
    return (tuple(map(int, row.strip().split())) for row in input_)


def check_sequence(seq: Sequence[int]) -> bool:
    return all(0 < v2 - v1 <= 3 if seq[0] < seq[1] else 0 < v1 - v2 <= 3 for v1, v2 in zip(seq, seq[1:]))


def part1(input_: Iterable[str]) -> int:
    return sum(map(check_sequence, parse_input(input_)))


def part2(input_: Iterable[str]) -> int:
    def can_fix_sequence(seq: Sequence[int]) -> bool:
        tails = [(seq[0], True, False), (seq[0], False, False)]
        for val in seq[1:]:
            new_tails = (
                *((val, is_ascending, value_dropped) for tail, is_ascending, value_dropped in tails if (0 < val - tail <= 3 if is_ascending else 0 < tail - val <= 3)),
                *((tail, is_ascending, True) for tail, is_ascending, value_dropped in tails if not value_dropped)
            )
            dedupe = defaultdict(lambda: True)
            for tail, is_ascending, value_dropped in new_tails:
                dedupe[tail, is_ascending] &= value_dropped
            tails = tuple((*key, value) for key, value in dedupe.items())

            if not tails:
                return False
        return True
    
    return sum(len(row) <= 2 or check_sequence(row[1:]) or can_fix_sequence(row) for row in parse_input(input_))


if __name__ == '__main__':
    with open('../../data/d02.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
