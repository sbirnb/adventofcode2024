from collections import defaultdict
from functools import lru_cache
from typing import Iterable, Mapping, Set, Sequence, Collection


def parse_input(input_: Iterable[str]) -> Mapping[str, Set[str]]:
    graph = defaultdict(set)
    for node1, node2 in (line.strip().split('-') for line in input_):
        graph[node1].add(node2)
        graph[node2].add(node1)
    return graph


def part1(input_: Iterable[str]) -> int:
    graph = parse_input(input_)

    @lru_cache(maxsize=None)
    def count_cliques_of_size(nodes: Sequence[str], size: int, t_node: bool) -> int:
        if size == 1:
            return len(nodes)
        return sum(count_cliques_of_size(tuple(n for n in nodes[i:] if n in graph[node]), size - 1, False) for i, node in enumerate(nodes, 1) if node[0] == 't' or not t_node)

    return count_cliques_of_size(tuple(sorted(graph, key=lambda c: -1 if c[0] == 't' else ord(c[0]))), 3, True)


def part2(input_: Iterable[str]) -> str:
    graph = parse_input(input_)

    @lru_cache(maxsize=None)
    def get_max_clique(nodes: Sequence[str]) -> Collection[str]:
        if len(nodes) <= 1:
            return nodes
        return max((((node,) + get_max_clique(tuple(n for n in nodes[i:] if n in graph[node]))) for i, node in enumerate(nodes, 1)), key=len)

    return ','.join(get_max_clique(tuple(sorted(graph))))


if __name__ == '__main__':
    with open('../../data/d23.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))