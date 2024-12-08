from collections import defaultdict
from itertools import chain, starmap, combinations, takewhile, count
from typing import Tuple, Mapping, Sequence, Iterable, Collection, Iterator, Callable
from math import gcd


def parse_input(input_: Sequence[str]) -> Tuple[Callable[[complex], bool], Mapping[str, Collection[complex]]]:
    height, width = len(input_), len(input_[0]) - 1
    nodes = defaultdict(list)
    for row, col, cell  in ((row, *c) for row, cells in enumerate(input_) for c in enumerate(cells)):
        if cell.isalnum():
            nodes[cell].append(complex(row, col))
    return lambda cell: 0 <= cell.real < height and 0 <= cell.imag < width, nodes


def part1(input_: Iterable[str]) -> int:
    in_bounds, nodes = parse_input(tuple(input_))

    def get_antinodes(antenna1: complex, antenna2: complex) -> Iterator[complex]:
        return (an for first, second in ((antenna1, antenna2), (antenna2, antenna1)) if in_bounds(an := first + (first - second)))

    return len(set(chain.from_iterable(chain.from_iterable(starmap(get_antinodes, combinations(antennae, 2)) for antennae in nodes.values()))))


def part2(input_: Iterable[str]) -> int:
    in_bounds, nodes = parse_input(tuple(input_))

    def get_antinodes(antenna1: complex, antenna2: complex) -> Iterator[complex]:
        delta = antenna1 - antenna2
        normalized = delta / gcd(int(delta.real), int(delta.imag))
        return chain(takewhile(in_bounds, (antenna1 + normalized * c for c in count())), takewhile(in_bounds, (antenna1 - normalized * c for c in count())))

    return len(set(chain.from_iterable(chain.from_iterable(starmap(get_antinodes, combinations(antennae, 2)) for antennae in nodes.values()))))


if __name__ == '__main__':
    with open('../../data/d08.txt', 'r') as fi:
        input_ = tuple(fi)

    print(part1(input_))
    print(part2(input_))
