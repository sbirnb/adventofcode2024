from collections import defaultdict
from typing import Iterable, Tuple, Collection, Sequence, Set, Mapping


def parse_input(input_: Iterable[str]) -> Tuple[complex, complex, Set[complex]]:
    walls = set()
    for row, cells in enumerate(input_):
        for col, cell in enumerate(cells):
            if cell == 'S':
                start = complex(row, col)
            elif cell == 'E':
                end = complex(row, col)
            elif cell == '#':
                walls.add(complex(row, col))
    return start, end, walls


def get_dists_along_path(start: complex, end: complex, walls: Set[complex]) -> Mapping[complex, int]:
    path = [None, start]
    while path[-1] != end:
        path.append(next(
            adjacent for d in (-1, 1, 1j, -1j) if (adjacent := d + path[-1]) not in walls and adjacent != path[-2]))
    return {node: dist for dist, node in enumerate(node for node in path if node is not None)}


def part1(input_: Iterable[str]) -> int:
    dists = get_dists_along_path(*parse_input(input_))
    cheats = 0
    for node1, dist1 in dists.items():
        for node2, dist2 in ((node2, dists[node2]) for d in (1, 1j) if (node2 := node1 + 2 * d) in dists and node1 + 1 * d not in dists):
            cheats += abs(dist1 - dist2) - 2 >= 100
    return cheats


def part2(input_: Iterable[str]) -> int:
    dists = get_dists_along_path(*parse_input(input_))

    def cdist(n: complex) -> int:
        return int(abs(n.real) + abs(n.imag))

    cheats = 0
    for node1, dist1 in dists.items():
        for c_rows in range(0, 21):
            for c_cols in range(abs(c_rows) - 20 if c_rows else 0, 21 - abs(c_rows)):
                node2 = complex(c_rows, c_cols) + node1
                cheats += node2 in dists and abs(dists[node2] - dist1) - cdist(node1 - node2) >= 100

    return cheats

if __name__ == '__main__':
    with open('../../data/d20.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))

