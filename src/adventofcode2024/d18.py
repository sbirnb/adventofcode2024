import heapq
from itertools import islice, count
from typing import Iterable, Iterator, Any, Collection, Sequence


def parse_input(input_: Iterable[str]) -> Iterator[complex]:
    return (complex(*map(int, row.strip().split(','))) for row in input_)


def estimator(dist: int, pos: complex, end: complex) -> Any:
    delta = end - pos
    return dist + int(abs(delta.real) + abs(delta.imag) - 1), pos.real, pos.imag


def get_adjacent(pos: complex, dim: int, bytes_: Collection[complex]) -> Iterator[complex]:
    return (apos for dir_ in (-1, 1, -1j, 1j) if (apos := pos + dir_) not in bytes_ and 0 <= apos.imag < dim and 0 <= apos.real < dim)


def get_dist(start: complex, end: complex, dim: int, bytes_: Collection[complex]) -> Sequence[complex]:
    heap = [(estimator(0, start, end), (0, start))]
    parents = dict()
    visited = {start}

    def backtrack(pos: complex) -> Sequence[complex]:
        path = [pos]
        while path[-1] in parents:
            path.append(parents[path[-1]])
        return path

    while heap:
        _, (dist, pos) = heapq.heappop(heap)
        for apos in set(get_adjacent(pos, dim, bytes_)) - visited:
            parents[apos] = pos
            if apos == end:
                return backtrack(end)
            visited.add(apos)
            heapq.heappush(heap, (estimator(dist + 1, apos, end), (dist + 1, apos)))


def part1(input_: Iterable[str]) -> int:
    dim = 71
    bytes_ = set(islice(parse_input(input_), 1024))
    start, end = 0, complex(dim - 1, dim - 1)
    return len(get_dist(start, end, dim, bytes_)) - 1


def part2(input_: Iterable[str]) -> str:
    dim = 71
    bytes_ = tuple(parse_input(input_))
    start, end = 0, complex(dim - 1, dim - 1)
    left, right = 1, len(bytes_) + 1
    while left < right:
        mid = (left + right) // 2
        byte_set = set(bytes_[:mid])
        path_bytes = get_dist(start, end, dim, byte_set)
        if path_bytes is None:
            right = mid - 1
        else:
            path_bytes_set = set(path_bytes)
            left = next(index for index, byte_ in enumerate(bytes_[mid:], mid) if byte_ in path_bytes_set)
    return f'{int(bytes_[left].real)},{int(bytes_[left].imag)}'


if __name__ == '__main__':
    with open('../../data/d18.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
