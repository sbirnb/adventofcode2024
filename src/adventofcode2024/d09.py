from collections import deque
from heapq import heappush, heappop
from itertools import chain, accumulate
from typing import Iterable, Sequence, Tuple, Iterator


def parse_input(input_: Iterable[str]) -> Sequence[int]:
    return tuple(map(int, next(iter(input_))))


def sum_range(start: int, width: int) -> int:
    return ((start + width - 1) * (start + width) - ((start - 1) * start)) // 2


def part1(input_: Iterable[str]) -> int:
    widths = parse_input(input_)
    free_space = deque()
    fragmented_blocks = []
    for i, (width, fs_ptr) in enumerate(zip(widths, accumulate(chain((0,), widths)))):
        if i % 2:
            free_space.append((fs_ptr, width))
        else:
            fragmented_blocks.append((i // 2, fs_ptr, width))
    free_space.append((float('inf'), float('inf')))

    def defragment() -> Iterator[Tuple[int, int, int]]:
        iter_blocks = reversed(fragmented_blocks)
        for index, start, width in iter_blocks:
            if width == 0:
                continue
            while width > 0:
                if start > free_space[0][0]:
                    free_start, free_width = free_space.popleft()
                    segment_width = min(width, free_width)
                    yield index, free_start, segment_width
                    width -= segment_width
                else:
                    yield index, start, width
                    yield from iter_blocks
                    return
            free_start += segment_width
            free_width -= segment_width
            if free_width > 0:
                free_space.appendleft((free_start, free_width))

    return sum(index * sum_range(start, width) for index, start, width in defragment())


def part2(input_: Iterable[str]) -> int:
    widths = parse_input(input_)
    free_heaps = [([float('inf')], i) for i in range(10)]
    fragmented_blocks = []

    for i, (width, fs_ptr) in enumerate(zip(widths, accumulate(chain((0,), widths)))):
        if i % 2:
            heappush(free_heaps[width][0], fs_ptr)
        else:
            fragmented_blocks.append((i // 2, fs_ptr, width))

    def defragment() -> Iterator[Tuple[int, int, int]]:
        for index, start, width in reversed(fragmented_blocks):
            free_heap, free_width = min(free_heaps[width:])
            if free_heap[0] > start:
                yield index, start, width
            else:
                free_start = heappop(free_heap)
                if width < free_width:
                    heappush(free_heaps[free_width - width][0], free_start + width)
                yield index, free_start, width

    return sum(index * sum_range(start, width) for index, start, width in defragment())


if __name__ == '__main__':
    with open('../../data/d09.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
