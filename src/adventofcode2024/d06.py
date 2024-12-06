from typing import Iterable, Tuple, Mapping, Iterator


def parse_input(input_: Iterable[str]) -> Mapping[complex, str]:
    return {row + col * 1j: cell for row, cells in enumerate(input_) for col, cell in enumerate(cells.strip())}


def get_guard_states(map_: Mapping[complex, str], state0: Tuple[complex, complex]) -> Iterator[Tuple[complex, complex]]:
    pos, dir_ = state0
    while pos in map_:
        yield pos, dir_
        while map_.get(pos + dir_) == '#':
            dir_ *= -1j
        pos += dir_


def part1(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    pos0 = next(iter(coord for coord, cell in map_.items() if cell == '^'))
    return len(set(pos for pos, _ in get_guard_states(map_, (pos0, -1))))


def part2(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    pos0 = next(iter(coord for coord, cell in map_.items() if cell == '^'))
    path = tuple(get_guard_states(map_, (pos0, -1)))
    visited_states = set()
    visited_pos = {pos0}
    obstacle_count = 0

    def has_cycle(test_map: Mapping[complex, str], test_state0: Tuple[complex, complex]) -> bool:
        test_visited_states = set()
        for state in get_guard_states(test_map, test_state0):
            if state in visited_states or state in test_visited_states:
                return True
            test_visited_states.add(state)
        return False

    for (pos, dir_), last_state in zip(path[1:], path):
        obstacle_count += pos not in visited_pos and has_cycle({**map_, pos: '#'}, last_state)
        visited_states.add(last_state)
        visited_pos.add(last_state[0])

    return obstacle_count


if __name__ == '__main__':
    with open('../../data/d06.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
