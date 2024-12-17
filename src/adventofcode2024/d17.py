from itertools import chain, starmap, zip_longest
from operator import eq
from typing import Iterable, Tuple, Sequence
import re


def parse_input(input_: Iterable[str]) -> Tuple[Tuple[int, int, int], Sequence[int]]:
    *registers, program = re.search(r'Register A: (\d+)\s*Register B: (\d+)\s*Register C: (\d+)\s*Program: ((?:\d+,?)+)', '\n'.join(input_), re.DOTALL).groups()
    return tuple(map(int, registers)), tuple(map(int, program.split(',')))


def combo(o: int, registers: Tuple[int, int, int]) -> int:
    if o < 4:
        return o
    return registers[o - 4]

def div(a: int, b: int, c: int, o: int) -> int:
    return a // (1 << combo(o, (a, b, c)))


OPS = [
    lambda a, b, c, p, o: (div(a, b, c, o), b, c, p + 2, None),
    lambda a, b, c, p, o: (a, b ^ o, c, p + 2, None),
    lambda a, b, c, p, o: (a, combo(o, (a, b, c)) & 7, c, p + 2, None),
    lambda a, b, c, p, o: (a, b, c, p + 2 if not a else o, None),
    lambda a, b, c, p, o: (a, b ^ c, c, p + 2, None),
    lambda a, b, c, p, o: (a, b, c, p + 2, combo(o, (a, b, c)) % 8),
    lambda a, b, c, p, o: (a, div(a, b, c, o), c, p + 2, None),
    lambda a, b, c, p, o: (a, b, div(a, b, c, o), p + 2, None),
]


def part1(input_: Iterable[str]) -> str:
    registers, program = parse_input(input_)

    a, b, c, p = *registers, 0
    output = []
    while p < len(program):
        a, b, c, p, pr = OPS[program[p]](a, b, c, p, program[p + 1])
        if pr is not None:
            output.append(pr)
    return ','.join(map(str, output))


def part2(input_: Iterable[str]) -> int:
    _, program = parse_input(input_)

    def run(a0: int) -> Tuple[int]:
        a, b, c, p = a0, 0, 0, 0
        while p < len(program):
            a, b, c, p, pr = OPS[program[p]](a, b, c, p, program[p + 1])
            if pr is not None:
                yield pr
    a0_candidates = [0]

    for l in range(1, len(program) + 1):
        a0_candidates = tuple(chain.from_iterable((a0 for a0 in range(c << 3, (c << 3) + 8) if all(starmap(eq, zip_longest(run(a0), program[-l:])))) for c in a0_candidates))

    return min(a0_candidates)


if __name__ == '__main__':
    with open('../../data/d17.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))