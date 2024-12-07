from itertools import chain
from math import log
from typing import Iterator, Iterable, Sequence, Tuple, Collection, Callable
from operator import mul, add


def parse_input(input_: Iterable[str]) -> Iterator[Tuple[Sequence[int], int]]:
    return ((tuple(int(term) for term in terms.split()), int(total)) for total, terms in (line.strip().split(': ') for line in input_))


def can_solve(terms: Sequence[int], total: int, ops: Collection[Callable[[int, int], int]]) -> int:
    if not terms:
        return total == 0
    partials = {terms[0]}
    for term in terms[1:]:
        partials = {partial for partial in chain.from_iterable((op(partial, term) for op in ops) for partial in partials) if partial <= total}
    return total in partials


def part1(input_: Iterable[str]) -> int:
    return sum(can_solve(terms, total, (add, mul)) * total for terms, total in parse_input(input_))


def part2(input_: Iterable[str]) -> int:

    def concat(term1: int, term2: int) -> int:
        return term1 * pow(10, int(1 + log(term2, 10))) + term2

    return sum(can_solve(terms, total, (add, mul, concat)) * total for terms, total in parse_input(input_))

if __name__ == '__main__':
    with open('../../data/d07.txt', 'r') as fi:
        input_ = tuple(fi)

    print(part1(input_))
    print(part2(input_))
