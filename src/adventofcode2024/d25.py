from functools import reduce
from itertools import groupby
from typing import Iterable, Tuple, Sequence


def parse_input(input_: Iterable[str]) -> Tuple[Sequence[Sequence[int]], Sequence[Sequence[int]]]:
    keys = []
    locks = []
    for matrix in (tuple(group) for is_group, group in groupby(map(str.strip, input_), bool) if is_group):
        component = tuple((sum(c == '#' for c in column) - 1) for column in zip(*matrix))
        if all(c == '#' for c in matrix[0]):
            locks.append(component)
        else:
            keys.append(component)
    return locks, keys


def part1(input_: Iterable[str]) -> int:
    locks, keys = parse_input(input_)
    lock_lookups = [[set() for _ in range(7)] for _ in range(5)]
    for lock in locks:
        for lock_height, column_lookup in zip(lock, lock_lookups):
            for lookup in column_lookup[:-1-lock_height]:
                lookup.add(lock)
    return sum(len(reduce(set.intersection, (lookup[height] for lookup, height in zip(lock_lookups, key)))) for key in keys)


def part2(input_: Iterable[str]) -> int:
    pass


if __name__ == '__main__':
    input_ = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####'''.split('\n')
    with open('../../data/d25.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
