from typing import Iterable, Tuple, Iterator, Sequence, FrozenSet


def parse_input(input_: Sequence[str]) -> Tuple[int, int, complex, FrozenSet[complex]]:
    return len(input_), len(input_[0]), \
        next(row + col * 1j for row, cells in enumerate(input_) for col, cell in enumerate(cells) if cell == '^'), \
        frozenset(row + col * 1j for row, cells in enumerate(input_) for col, cell in enumerate(cells) if cell == '#')


def get_guard_states(height: int, width: int, obstacles: FrozenSet[complex], state0: Tuple[complex, complex]) -> Iterator[Tuple[complex, complex]]:
    pos, dir_ = state0
    while 0 <= pos.real < height and 0 <= pos.imag < width:
        yield pos, dir_
        while pos + dir_ in obstacles:
            dir_ *= -1j
        pos += dir_


def part1(input_: Iterable[str]) -> int:
    height, width, pos0, obstacles = parse_input(tuple(input_))
    return len(set(pos for pos, _ in get_guard_states(height, width, obstacles, (pos0, -1))))


def part2(input_: Iterable[str]) -> int:
    height, width, pos0, obstacles = parse_input(tuple(input_))
    path = tuple(get_guard_states(height, width, obstacles, (pos0, -1)))
    visited_states = set()
    visited_pos = {pos0}
    obstacle_count = 0

    def has_cycle(test_obstacles: FrozenSet[complex], state0: Tuple[complex, complex]) -> bool:
        test_visited_states = set()
        for state in get_guard_states(height, width, test_obstacles, state0):
            if state in visited_states or state in test_visited_states:
                return True
            test_visited_states.add(state)
        return False

    for (pos, dir_), last_state in zip(path[1:], path):
        obstacle_count += pos not in visited_pos and has_cycle(obstacles | {pos}, last_state)
        visited_states.add(last_state)
        visited_pos.add(last_state[0])

    return obstacle_count


if __name__ == '__main__':
    with open('../../data/d06.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
