from itertools import starmap
from typing import Iterator, Tuple, Iterable, Optional
import re

BUTTON = re.compile(r'Button \w: X\+(\d+), Y\+(\d+)')
PRIZE = re.compile(r'Prize: X=(\d+), Y=(\d+)')


def parse_input(input_: Iterable[str]) -> Iterator[Tuple[Tuple[Tuple[int, int],Tuple[int, int]], Tuple[int, int]]]:
    iter_input = iter(input_)
    while True:
        yield tuple(map(int, BUTTON.search(next(iter_input)).groups())), \
            tuple(map(int, BUTTON.search(next(iter_input)).groups())), \
            tuple(map(int, PRIZE.search(next(iter_input)).groups()))
        try:
            next(iter_input)
        except StopIteration:
            return


def det(m: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    (x1, y1), (x2, y2) = m
    return x1 * y2 - y1 * x2


def solve_unique(a: Tuple[int, int], b: Tuple[int, int], t: Tuple[int, int]) -> int:
    d, d1, d2 = det((a, b)), det((t, b)), det((a, t))
    if d1 % d != 0 or d2 % d != 0:
        return 0
    n, m = d1 // d, d2 // d
    if 0 <= n and 0 <= m:
        return n * 3 + m
    return 0


def part1(input_: Iterable[str]) -> int:
    return sum(starmap(solve_unique, parse_input(input_)))


def part2(input_: Iterable[str]) -> int:
    def add_offset(t1, t2) -> Tuple[int, int]:
        return 10000000000000 + t1, 10000000000000 + t2
    return sum(solve_unique(a, b, add_offset(*t)) for a, b, t in parse_input(input_))


if __name__ == '__main__':
    with open('../../data/d13.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
