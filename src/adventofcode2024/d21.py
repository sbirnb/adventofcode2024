from functools import lru_cache
from itertools import permutations
from typing import Iterable, Sequence, Iterator, Tuple
import re

NUMPAD = dict(zip('789456123x0A', (complex(row, col) for row in range(4) for col in range(3))))
ARROWS = {-1j: 1 + 0j, -1: 1j, 1: 1 + 1j, 1j: 1 + 2j, 0: 2j}


def parse_input(input_: Iterable[str]) -> Iterator[str]:
    return map(str.strip, input_)


def sign(value) -> int:
    return (value > 0) - (value < 0)


def count_presses(code: str, n_robots: int) -> int:

    @lru_cache(maxsize=None)
    def press_button(start: complex, button: complex, presses: int, depth: int, dead_space: complex) -> int:
        if depth == 0:
            return int(abs((start - button).imag) + abs((start - button).real)) + presses
        return min(expand_sequence_length(sequence, presses, depth) for sequence in get_move_sequences(start, button, dead_space))

    def get_move_sequences(start: complex, target: complex, dead: complex) -> Iterable[Sequence[Tuple[int, complex]]]:
        delta = target - start
        moves = []
        if delta.real:
            moves.append((int(abs(delta.real)), sign(delta.real)))
        if delta.imag:
            moves.append((int(abs(delta.imag)), sign(delta.imag) * 1j))
        return (p for p in permutations(moves) if start + p[0][0] * p[0][1] != dead)

    def expand_sequence_length(sequence: Iterable[Tuple[int, complex]], presses: int, depth: int) -> int:
        length = 0
        pos = 2j
        for count, dir_ in sequence:
            target_pos = ARROWS[dir_]
            length += press_button(pos, target_pos, count, depth - 1, 0)
            pos = target_pos
        return length + press_button(pos, 2j, presses, depth - 1, 0)

    return sum(press_button(NUMPAD[p1], NUMPAD[p2], 1, n_robots, 3) for p1, p2 in zip('A' + code, code))


def part1(input_: Iterable[str]) -> int:
    return sum(int(re.match(r'\d+', code).group(0)) * count_presses(code, 2) for code in parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    return sum(int(re.match(r'\d+', code).group(0)) * count_presses(code, 25) for code in parse_input(input_))


if __name__ == '__main__':
    with open('../../data/d21.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))


