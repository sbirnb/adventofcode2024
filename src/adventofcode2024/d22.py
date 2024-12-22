from collections import defaultdict, deque
from itertools import islice, pairwise
from typing import Iterable, Iterator


def parse_input(input_: Iterable[str]) -> Iterator[int]:
    return (int(row.strip()) for row in input_)


def gen_secrets(seed: int, iters: int = 2000) -> Iterator[int]:

    def next_secret(s: int) -> int:
        s = (s ^ (s << 6)) & ((1 << 24) - 1)
        s = (s ^ (s >> 5)) & ((1 << 24) - 1)
        s = (s ^ (s << 11)) & ((1 << 24) - 1)
        return s

    prev = seed
    yield seed
    for _ in range(iters):
        current = next_secret(prev)
        yield current
        prev = current


def part1(input_: Iterable[str]) -> int:
    return sum(next(islice(gen_secrets(seed, 2000), 2000, None)) for seed in parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    prefix_vals = defaultdict(int)
    for seed in parse_input(input_):
        seen = set()
        pairwise_secrets = pairwise(v % 10 for v in gen_secrets(seed, 2000))
        window = deque(v2 - v1 for v1, v2 in islice(pairwise_secrets, 3))
        for v1, v2 in pairwise_secrets:
            window.append(v2 - v1)
            tuple_window = tuple(window)
            if tuple_window not in seen:
                prefix_vals[tuple_window] += v2
                seen.add(tuple_window)
            window.popleft()
    return max(prefix_vals.values())


if __name__ == '__main__':
    with open('../../data/d22.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
