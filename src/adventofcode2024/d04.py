import re
from typing import Sequence


def part1(input_: Sequence[str]) -> int:
    patterns = r'XMAS', r'SAMX', *(f'.{{{len(input_[0]) + offset - 1}}}'.join(rf'{l}' for l in word) for word in ('XMAS', 'SAMX') for offset in (-1, 0, 1))
    return sum(len(re.findall(fr'(?={p})', ''.join(input_), re.DOTALL)) for p in patterns)


def part2(input_: Sequence[str]) -> int:
    skip = len(input_[0]) - 3
    return len(re.findall(fr'(?=M\wS.{{{skip}}}\wA\w.{{{skip}}}M\wS|S\wS.{{{skip}}}\wA\w.{{{skip}}}M\wM|S\wM.{{{skip}}}\wA\w.{{{skip}}}S\wM|M\wM.{{{skip}}}\wA\w.{{{skip}}}S\wS)', ''.join(input_), re.DOTALL))


if __name__ == '__main__':
    with open('../../data/d04.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
