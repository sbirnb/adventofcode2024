from functools import reduce
from itertools import takewhile, chain, count
from typing import Tuple, Set, Sequence, Iterable, Dict


def parse_input(input_: Iterable[str]) -> Tuple[complex, Set[complex], Set[complex], Sequence[complex]]:
    iter_input = map(str.strip, input_)
    boxes, walls = set(), set()
    start = None
    for row, cells in enumerate(takewhile(bool, iter_input)):
        for col, cell in enumerate(cells):
            if cell == '#':
                walls.add(complex(row, col))
            elif cell == 'O':
                boxes.add(complex(row, col))
            elif cell == '@':
                start = complex(row, col)
    return start, walls, boxes, tuple(map({'<': -1j, '>': 1j, '^': -1, 'v': 1}.get, chain.from_iterable(iter_input)))


def stretch_input(start: complex, walls: Set[complex], boxes: Set[complex]) -> Tuple[complex, Set[complex], Dict[complex, complex]]:
    return start + start.imag * 1j, \
        set(chain.from_iterable((wall + wall.imag * 1j, wall + (wall.imag + 1) * 1j) for wall in walls)), \
        dict(chain.from_iterable(((box + box.imag * 1j, 1j), (box + (box.imag + 1) * 1j, -1j)) for box in boxes))


def part1(input_: Iterable[str]):
    start, walls, boxes, moves = parse_input(input_)

    def push_box(pos: complex, dir_:complex):
        new_pos = next(new_pos for dist in count(1) if (new_pos := pos + dir_ * dist) not in boxes)
        if new_pos in walls:
            return False
        boxes.remove(pos)
        boxes.add(new_pos)
        return True

    def move_robot(pos: complex, dir_: complex) -> complex:
        new_pos = pos + dir_
        if new_pos not in walls and (new_pos not in boxes or push_box(new_pos, dir_)):
            return new_pos
        return pos

    reduce(move_robot, moves, start)
    return int(sum(box.imag + 100 * box.real for box in boxes))


def part2(input_: Iterable[str]) -> int:
    *unstretched, moves = parse_input(input_)
    start, walls, boxes = stretch_input(*unstretched)

    def get_box(pos: complex) -> Tuple[complex, complex]:
        return pos, pos + boxes[pos]

    def push_box(pos: complex, dir_:complex):
        return (dir_.real == 0 and push_box_h(pos, dir_)) or (dir_.imag == 0 and push_box_v(pos, dir_))

    def push_box_h(pos: complex, dir_: complex) -> bool:
        new_pos, dist = next((new_pos, dist) for dist in count(1) if (new_pos := pos + dir_ * dist) not in boxes)
        if new_pos in walls:
            return False
        for d in range(dist):
            boxes[pos + d * dir_] *= -1
        boxes[new_pos] = boxes.pop(pos)
        return True

    def push_box_v(pos: complex, dir_: complex) -> bool:
        seen = set(get_box(pos))
        queue = list(get_box(pos))
        queue_index = 0
        while queue_index < len(queue):
            next_cell = queue[queue_index] + dir_
            queue_index += 1
            if next_cell in seen:
                continue
            elif next_cell in walls:
                return False
            elif next_cell in boxes:
                box = get_box(next_cell)
                seen.update(box)
                queue.extend(get_box(next_cell))
        for cell in reversed(queue):
            boxes[cell + dir_] = boxes.pop(cell)
        return True

    def move_robot(pos: complex, dir_: complex) -> complex:
        new_pos = pos + dir_
        if new_pos not in walls and (new_pos not in boxes or push_box(new_pos, dir_)):
            return new_pos
        return pos

    reduce(move_robot, moves, start)
    return int(sum(box.imag + 100 * box.real for box in boxes if boxes[box] == 1j))


if __name__ == '__main__':
    with open('../../data/d15.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
