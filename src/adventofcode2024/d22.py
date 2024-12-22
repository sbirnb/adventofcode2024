from collections import defaultdict, deque
from functools import reduce
from itertools import islice, pairwise
from operator import xor
from typing import Iterable, Iterator, Sequence, Set


def parse_input(input_: Iterable[str]) -> Iterator[int]:
    return (int(row.strip()) for row in input_)


def identity_transform(bits: int) -> Sequence[Set[int]]:
    return tuple({index} for index in range(bits))


def repeat_transform(transform: Sequence[Set[int]], times: int) -> Sequence[Set[int]]:

    def compose_transforms(t1: Sequence[Set[int]], t2: Sequence[Set[int]]) -> Sequence[Set[int]]:
        return tuple(reduce(lambda s1, i: (s1 | t2[i]) - (s1 & t2[i]), s2, set()) for j, s2 in enumerate(t1))

    res = identity_transform(len(transform))
    squaring = transform
    while times > 0:
        if times & 1:
            res = compose_transforms(squaring, res)
        squaring = compose_transforms(squaring, squaring)
        times >>= 1
    return res


def apply_to_bit_array(transform: Sequence[Set[int]], bit_array: Sequence[int]) -> Sequence[int]:
    return tuple(reduce(xor, (bit_array[i] for i in n), 0) for n in transform)


def to_bit_array(value: int, length: int) -> Sequence[int]:
    bit_array = tuple(map(int, bin(value)[2:]))
    return *((0,) * (length - len(bit_array))), *bit_array


def from_bit_array(bit_array: Sequence[int]) -> int:
    return int(''.join(map(str, bit_array)), 2)


def get_base_transform():
    def lshift(bits: Sequence[Set[int]], d: int) -> Sequence[Set[int]]:
        return *bits[d:], *((set(),) * d)

    def rshift(bits: Sequence[Set[int]], d: int) -> Sequence[Set[int]]:
        return *((set(),) * d), *bits[:-d]

    def add_transforms(t1: Sequence[Set[int]], t2: Sequence[Set[int]]) -> Sequence[Set[int]]:
        return tuple((s1 | s2) - (s1 & s2) for s1, s2 in zip(t1, t2))

    transform = identity_transform(24)
    transform = add_transforms(lshift(transform, 6), transform)
    transform = add_transforms(rshift(transform, 5), transform)
    transform = add_transforms(lshift(transform, 11), transform)
    return transform


def part1(input_: Iterable[str]) -> int:
    transform = repeat_transform(get_base_transform(), 2000)
    total = 0
    for i in parse_input(input_):
        total += from_bit_array(apply_to_bit_array(transform, to_bit_array(i, len(transform))))
    return total


def part2(input_: Iterable[str]) -> int:

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
