from typing import Tuple, Sequence, Collection, Iterable


def parse_input(input_: Sequence[str]) -> Tuple[Sequence[str], int]:
    width = len(input_[0].strip()) + 1
    return '.' * width + '.'.join(map(str.strip, input_)) + '.' * width, width


def get_adjacent(index: int, width: int) -> Sequence[int]:
    return index - width, index + 1, index + width, index - 1


def part1(input_: Iterable[str]) -> int:
    plotmap, width = parse_input(input_)
    seen = set()
    cost = 0

    def get_region_cost(start: int) -> Tuple[int, Collection[int]]:
        stack = [start]
        region = {start}
        perimeter = 0
        while stack:
            index = stack.pop()
            for adjacent in get_adjacent(index, width):
                if 0 <= adjacent < len(plotmap) and adjacent not in region:
                    if plotmap[index] == plotmap[adjacent]:
                        region.add(adjacent)
                        stack.append(adjacent)
                    else:
                        perimeter += 1
        return perimeter, region

    for index, plot in enumerate(plotmap):
        if index not in seen and 'A' <= plot <= 'Z':
            perimeter, region = get_region_cost(index)
            cost += perimeter * len(region)
            seen.update(region)
    return cost


def part2(input_: Iterable[str]) -> int:
    plotmap, width = parse_input(input_)

    def get_region(start: int, char: str) -> Collection[int]:
        stack = [start]
        region = {start}
        while stack:
            index = stack.pop()
            for adjacent_index in get_adjacent(index, width):
                if adjacent_index not in region and plotmap[adjacent_index] == char:
                    stack.append(adjacent_index)
                    region.add(adjacent_index)
        return region

    regions = dict()
    region_sizes = list()
    for index, plot in enumerate(plotmap):
        if index not in regions and 'A' <= plot <= 'Z':
            region = get_region(index, plot)
            regions.update(((r_index, len(region_sizes)) for r_index in region))
            region_sizes.append(len(region))
    cost = 0
    for index, plot in regions.items():
        adjacent = get_adjacent(index, width)
        for adjacent1, adjacent2 in zip(adjacent, (*adjacent[1:], adjacent[0])):
            if (adjacent_plot1 := regions.get(adjacent1)) != plot and (adjacent_plot2 := regions.get(adjacent2)) != plot:
                cost += region_sizes[plot]
                adjacent3 = adjacent1 + adjacent2 - index
                if adjacent_plot1 == adjacent_plot2 == regions.get(adjacent3) and adjacent_plot1 is not None:
                    cost += region_sizes[adjacent_plot2]
    return cost


if __name__ == '__main__':
    with open('../../data/d12.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
