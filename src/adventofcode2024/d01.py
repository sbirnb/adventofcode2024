from collections import Counter
from typing import Iterable, Tuple, Iterator


def parse_input(input_: Iterable[str]) -> Iterator[Tuple[int, int]]:
    return ((int(v1), int(v2)) for v1, v2 in (row.strip().split() for row in input_))


def part1(input_: Iterable[str]) -> int:
    return sum(abs(v1 - v2) for v1, v2 in zip(*map(sorted, zip(*parse_input(input_)))))


def part2(input_: Iterable[str]) -> int:
    list1, list2 = zip(*parse_input(input_))
    list2_counts = Counter(list2)
    return sum(value * list2_counts[value] for value in list1)


if __name__ == '__main__':
    with open('../../data/d01.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))