import cProfile
from collections import Counter, defaultdict
from functools import reduce
from operator import mul
from typing import Tuple, Iterator, Iterable, Collection, Sequence
import re


def parse_input(input_: Iterable[str]) -> Iterator[Tuple[Tuple[int, int], Tuple[int, int]]]:
    return (((x, y), (dx, dy)) for x, y, dx, dy in (map(int, re.findall(r'-?\d+', row)) for row in input_))


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def part1(input_: Iterable[str], dims: Tuple[int, int] = (101, 103)) -> int:
    quadrant_counts = Counter(tuple(sign((x + 100 * dx) % dim - dim // 2) for x, dx, dim in zip(p, d, dims)) for p, d in parse_input(input_))
    return reduce(mul, (count for quad, count in quadrant_counts.items() if 0 not in quad))


def part2(input_: Iterable[str], dims: Tuple[int, int] = (101, 103)) -> int:
    width, height = dims
    robot_states = defaultdict(list)
    for p, d in parse_input(input_):
        robot_states[p].append(d)

    def contains_christmas_tree(robots: Collection[Tuple[int, int]], h: int = 9) -> bool:
        for x, y in robots:
            for offset in range(1, h + 1):
                if (x - offset, y + offset) not in robots or (x + offset, y + offset) not in robots:
                    break
            else:
                return True
        return False

    def get_next_robots(robots: Iterable[Tuple[Tuple[int, int], Sequence[Tuple[int, int]]]]) -> Iterator[Tuple[Tuple[int, int], Tuple[int, int]]]:
        for (x, y), d in robots:
            for dx, dy in d:
                yield ((x + dx) % width, (y + dy) % height), (dx, dy)


    for t in range(101 * 103):
        if contains_christmas_tree(robot_states):
            print('\n'.join(''.join('.x'[(col, row) in robot_states] for col in range(dims[0])) for row in range(dims[1])))
            return t
        next_states = defaultdict(list)
        for p, d in get_next_robots(robot_states.items()):
            next_states[p].append(d)
        robot_states = next_states


if __name__ == '__main__':
    with open('../../data/d14.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
