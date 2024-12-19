from collections import deque, defaultdict
from dataclasses import dataclass, field
from functools import reduce
from itertools import islice, accumulate, takewhile
from typing import Sequence, Tuple, Iterable, Self, Mapping
import re


@dataclass
class Trie:
    count: int = 0
    next_: Mapping[str, Self] = field(default_factory=lambda: defaultdict(Trie))

    def add(self, string: str):
        reduce(lambda node, char: node.next_[char], string, self).count += 1

    def match_prefix(self, string: str) -> Iterable[int]:
        return (i for i, node in enumerate(takewhile(bool, islice(accumulate(string, (lambda node, char: node.next_[char] if char in node.next_ else None), initial=self), 1, None))) if node.count)


def parse_input(input_: Iterable[str]) -> Tuple[Sequence[str], Iterable[str]]:
    iter_input = map(str.strip, input_)
    return next(iter_input).split(', '), islice(iter_input, 1, None)


def part1(input_: Iterable[str]) -> int:
    towels, patterns = parse_input(input_)
    possible_patterns_regex = re.compile(rf'^({'|'.join(towels)})*$')
    return sum(possible_patterns_regex.match(pattern) is not None for pattern in patterns)


def part2(input_: Iterable[str]) -> int:
    towels, patterns = parse_input(input_)
    trie = Trie()
    for towel in towels:
        trie.add(towel)

    def count_ways_to_build(pattern: str) -> int:
        match_counts = deque((1, *((0,) * (len(pattern) + 1))))
        for i in range(len(pattern)):
            match_count = match_counts.popleft()
            for length in trie.match_prefix(pattern[i:]):
                match_counts[length] += match_count
        return match_counts[0]

    return sum(map(count_ways_to_build, patterns))


if __name__ == '__main__':
    with open('../../data/d19.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))