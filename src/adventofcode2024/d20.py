from typing import Iterable, Tuple, Set, Mapping, Iterator


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


def get_path(start: complex, end: complex, walls: Set[complex]) -> Iterator[complex]:
    prev, current = None, start
    yield start
    while current != end:
        prev, current = current, next(adjacent for d in (-1, 1, 1j, -1j) if (adjacent := d + current) not in walls and adjacent != prev)
        yield current


def get_dists_along_path(start: complex, end: complex, walls: Set[complex]) -> Mapping[complex, int]:
    return {node: dist for dist, node in enumerate(node for node in get_path(start, end, walls) if node is not None)}


def part1(input_: Iterable[str]) -> int:
    dists = get_dists_along_path(*parse_input(input_))
    cheats = 0
    for node1, dist1 in dists.items():
        for node2, dist2 in ((node2, dists[node2]) for d in (1, 1j) if (node2 := node1 + 2 * d) in dists and node1 + 1 * d not in dists):
            cheats += abs(dist1 - dist2) - 2 >= 100
    return cheats


def part2(input_: Iterable[str]) -> int:
    threshold, radius = 100, 20
    start, end, walls = parse_input(input_)
    path = tuple(get_path(start, end, walls))
    dists = {node: dist for dist, node in enumerate(node for node in path if node is not None)}

    def cdist(n: complex) -> int:
        return int(abs(n.real) + abs(n.imag))

    def update_window(pos1: complex, pos2: complex) -> int:
        window.remove(pos2)
        dir_ = pos2 - pos1
        for i in range(-radius, radius + 1):
            offset = (radius - abs(i) + i * 1j) * dir_
            back, front = pos1 - offset, pos2 + offset
            window.discard(back)
            if dists.get(front, 0) > dists[pos2]:
                window.add(front)

    window = {node for row in range(-radius, radius + 1) for col in range(abs(row) - radius, radius + 1 - abs(row)) if dists.get(node := start + complex(row, col), 0) > 0}
    cheats = 0
    for pos1, pos2 in zip(path, path[1:]):
        cheats += sum(dists[node] - dists[pos1] - cdist(node - pos1) >= threshold for node in window)
        update_window(pos1, pos2)
    return cheats


if __name__ == '__main__':
    with open('../../data/d20.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
