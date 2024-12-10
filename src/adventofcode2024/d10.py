from functools import lru_cache, reduce
from typing import Iterable, Mapping, Collection


def parse_input(input_: Iterable[str]) -> Mapping[complex, int]:
    return {complex(row, col): int(height) for row, heights in enumerate(input_) for col, height in enumerate(heights.strip())}


def part1(input_: Iterable[str]) -> int:
    heightmap = parse_input(input_)

    @lru_cache(maxsize=None)
    def get_trailends(start: complex) -> Collection[complex]:
        height = heightmap[start] + 1
        if height == 10:
            return {start}
        return reduce(set.union, (get_trailends(adj) for dir_ in (-1, 1, -1j, 1j) if heightmap.get(adj := start + dir_) == height), set())

    return sum(map(len, (get_trailends(start) for start, height in heightmap.items() if height == 0 )))


def part2(input_: Iterable[str]) -> int:
    heightmap = parse_input(input_)

    @lru_cache(maxsize=None)
    def get_rating(start: complex) -> int:
        height = heightmap[start] + 1
        if height == 10:
            return 1
        return sum(get_rating(adj) for dir_ in (-1, 1, -1j, 1j) if heightmap.get(adj := start + dir_) == height)

    return sum(get_rating(start) for start, height in heightmap.items() if height == 0 )


if __name__ == '__main__':
    with open('../../data/d10.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
