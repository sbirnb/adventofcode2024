from typing import Iterable, Tuple, Set
import heapq
from random import random

def parse_input(input_: Iterable[str]) -> Tuple[Tuple[complex, complex], Set[complex]]:
    walls = set()
    for row, cells in enumerate(input_):
        for col, cell in enumerate(cells):
            if cell == '#':
                walls.add(complex(row, col))
            elif cell == 'S':
                start = complex(row, col)
            elif cell == 'E':
                end = complex(row, col)
    return (start, end), walls


def part1(input_: Iterable[str]) -> int:
    (start, end), walls = parse_input(input_)

    def dist(p1: complex, p2: complex) -> int:
        d = p1 - p2
        return int(abs(d.real) + abs(d.imag))

    def get_next_states(cost: int, pos: complex, dir_: complex) -> Iterable[Tuple[int, complex, complex]]:
        if pos + dir_ not in walls:
            yield cost + 1, pos + dir_, dir_
        yield from ((cost + 1000, pos, dir_ * r) for r in (-1j, 1j))


    heap = [(dist(start, end), random(), (0, start, 1j))]
    seen = {(start, 1j)}
    while heap:
        _, _, state = heapq.heappop(heap)
        for next_cost, next_pos, next_dir in get_next_states(*state):
            if next_pos == end:
                return next_cost
            if (next_pos, next_dir) not in seen:
                seen.add((next_pos, next_dir))
                heapq.heappush(heap, (next_cost + dist(next_pos, end), random(), (next_cost, next_pos, next_dir)))


if __name__ == '__main__':
    with open('../../data/d16.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))

