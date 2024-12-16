from typing import Iterable, Tuple, Set, Collection, Mapping
import heapq
from random import random


def parse_input(input_: Iterable[str]) -> Tuple[Tuple[complex, complex], Set[complex]]:
    walls = set()
    for row, cells in enumerate(input_):
        for col, cell in enumerate(cells):
            if cell == '#':
                walls.add(complex(row, col))
            elif cell == 'S':
                start = complex(row, col)
            elif cell == 'E':
                end = complex(row, col)
    return (start, end), walls


def dist(p1: complex, p2: complex) -> int:
    d = p1 - p2
    return int(abs(d.real) + abs(d.imag))


def get_next_states(cost: int, pos: complex, dir_: complex, walls: Collection[complex]) -> Iterable[Tuple[int, Tuple[complex, complex]]]:
    if pos + dir_ not in walls:
        yield cost + 1, (pos + dir_, dir_)
    yield from ((cost + 1000, (pos, dir_ * r)) for r in (-1j, 1j))


def est_cost(cost: int, state: Tuple[complex, complex], target:complex) -> Tuple[int, float]:
    return cost + int(dist(state[0], target)), random()


def part1(input_: Iterable[str]) -> int:
    (start, end), walls = parse_input(input_)
    state0 = start, 1j
    heap = [(est_cost(0, state0, end), (0, state0))]
    seen = {state0}
    while heap:
        _, (cost, state) = heapq.heappop(heap)
        for next_cost, next_state in get_next_states(cost, *state, walls):
            if next_state[0] == end:
                return next_cost
            if next_state not in seen:
                seen.add(state)
                heapq.heappush(heap, (est_cost(next_cost, next_state, end), (next_cost, next_state)))


def part2(input_: Iterable[str]) -> int:
    (start, end), walls = parse_input(input_)
    end_states = {(end, dir_) for dir_ in (-1, 1, 1j, -1j)}
    state0 = start, 1j

    def find_paths(
            state0 : Tuple[complex, complex],
            end_states: Collection[Tuple[complex, complex]]
    ) -> Mapping[Tuple[complex, complex], Tuple[int, Collection[complex]]]:
        heap = [(est_cost(0, state0, end), (0, state0))]
        seen = {state0: (0, [])}
        while heap:
            _, (cost, state) = heapq.heappop(heap)
            for next_cost, next_state in get_next_states(cost, *state, walls):
                if next_state not in seen:
                    seen[next_state] = (next_cost, [state])
                    heapq.heappush(heap, (est_cost(next_cost, next_state, end), (next_cost, next_state)))
                else:
                    min_cost, parent_states = seen[next_state]
                    if min_cost == next_cost:
                        parent_states.append(state)
                    elif next_state in end_states:
                        return seen

    def get_visited_states_to(seen: Mapping[Tuple[complex, complex], Tuple[int, Collection[complex]]], end_states: Collection[Tuple[complex, complex]]) -> Collection[Tuple[complex, complex]]:
        min_cost, _ = min(seen.get(end_state, (float('inf'), None)) for end_state in end_states)
        mark_stack = [end_state for end_state in end_states if seen.get(end_state, (float('inf'), None))[0] == min_cost]
        marked = set(mark_stack)
        while mark_stack:
            state = mark_stack.pop()
            for prev_state in seen[state][1]:
                if prev_state not in marked:
                    marked.add(prev_state)
                    mark_stack.append(prev_state)
        return marked

    seen = find_paths(state0, end_states)
    visited_states = get_visited_states_to(seen, end_states)
    return len(set(pos for pos, _ in visited_states))


if __name__ == '__main__':
    with open('../../data/d16.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
