import re
from typing import Iterable


def parse_input(input_: Iterable[str]) -> str:
    return ''.join(input_)


def sum_muls(s: str) -> int:
    return sum(int(v1) * int(v2) for v1, v2 in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', s))


def part1(input_: Iterable[str]) -> int:
    return sum_muls(parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    return sum(sum_muls(do.split('don\'t()', 1)[0]) for do in parse_input(input_).split('do()'))


if __name__ == '__main__':
    with open('../../data/d03.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))

