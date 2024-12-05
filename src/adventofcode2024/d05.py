import re
from collections import defaultdict
from typing import Tuple, Sequence, Iterable, Iterator, Mapping, Set
from itertools import takewhile


def parse_input(input_: Iterator[str]) -> Tuple[Mapping[str, Set[str]], Sequence[str]]:
    return get_rules((row.split('|') for row in takewhile(bool, map(str.strip, input_)))), tuple(input_)


def get_rules(rules: Iterable[Sequence[str]]) -> Mapping[str, Set[str]]:
    rule_map = defaultdict(set)
    for first, second in rules:
        rule_map[second].add(first)
    return rule_map


def part1(input_: Iterable[str]) -> int:
    rule_map, updates = parse_input(iter(input_))
    rule_regex = re.compile('|'.join(f'{second},.*({'|'.join(firsts)}).*' for second, firsts in rule_map.items()))
    return sum(int(update[(index := len(update)//2 - 1):index + 2]) for update in updates if not rule_regex.search(update))


def part2(input_: Iterable[str]) -> int:
    rule_map, updates = parse_input(iter(input_))
    rule_regex = re.compile('|'.join(f'{second},.*({'|'.join(firsts)}).*' for second, firsts in rule_map.items()))
    invalid_update_pages = tuple(set(update.strip().split(',')) for update in updates if rule_regex.search(update))
    return sum(int(sorted((len(pages & rule_map[page]), page) for page in pages)[len(pages) // 2][1]) for pages in invalid_update_pages)


if __name__ == '__main__':
    with open('../../data/d05.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
