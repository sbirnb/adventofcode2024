import cProfile
from heapq import heappush, heappop
from itertools import chain, accumulate
from typing import Iterable, Sequence, Tuple, Iterator


def parse_input(input_: Iterable[str]) -> Sequence[int]:
    return tuple(map(int, next(iter(input_))))


def part1(input_: Iterable[str]) -> int:
    expand = tuple(chain.from_iterable([i // 2 if i % 2 == 0 else None] * v for i, v in enumerate(parse_input(input_))))
    left = 0
    right = len(expand) - 1
    total = 0
    compacted = []
    while left <= right:
        if expand[left] is not None:
            total += left * expand[left]
            compacted.append(expand[left])
            left += 1
        elif expand[right] is not None:
            total += left * expand[right]
            compacted.append(expand[right])
            right -= 1
            left += 1
        else:
            right -= 1
    return total


def part2(input_: Iterable[str]) -> int:
    widths = parse_input(input_)
    free_heaps = [[] for _ in range(11)]
    fragmented_blocks = []

    for i, (width, fs_ptr) in enumerate(zip(widths, accumulate(chain((0,), widths)))):
        if i % 2:
            heappush(free_heaps[width], fs_ptr)
        else:
            fragmented_blocks.append((i // 2, fs_ptr, width))

    def defragment() -> Iterator[Tuple[int, int, int]]:
        for index, start, width in reversed(fragmented_blocks):
            try:
                free_width, free_heap = min(((w, heap) for w, heap in enumerate(free_heaps[width:], width) if heap and heap[0] < start), key=lambda wh: wh[1][0])
            except ValueError:
                yield index, start, width
            else:
                free_start = heappop(free_heap)
                if width < free_width:
                    heappush(free_heaps[free_width - width], free_start + width)
                yield index, free_start, width
    return sum(index * sum(range(start, start + width)) for index, start, width in defragment())


if __name__ == '__main__':
    with open('../../data/d09.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
