from collections import defaultdict
from functools import lru_cache
from itertools import takewhile
from operator import and_, or_, xor
from typing import Iterable, Tuple
import re

OPERATORS = {'AND': and_, 'OR': or_, 'XOR': xor}

def parse_input(input_: Iterable[str]) -> Tuple[Iterable[Tuple[str, int]], Tuple[Tuple[str, str, str, str]]]:
    iter_input = map(str.strip, input_)
    initial_values = tuple((key, int(value)) for key, value in (re.match(r'(\w+): ([01])', line).groups() for line in takewhile(bool, iter_input)))
    operations = tuple(tuple(re.match(r'(\w+) (\w+) (\w+) -> (\w+)', line).groups() for line in iter_input))
    return initial_values, operations


def part1(input_: Iterable[str]) -> int:
    initial_values, operations = parse_input(input_)
    op_map = defaultdict(list)
    for node1, operator, node2, out in operations:
        node = (operator, [-1, -1], out)
        op_map[node1].append((0, node))
        op_map[node2].append((1, node))
    calculated_values = dict()
    op_queue = list(initial_values)

    def set_value(key: str, value: int):
        calculated_values[key] = value
        for index, (operator, values, out) in op_map[key]:
            values[index] = value
            if values[1 - index] != -1:
                op_queue.append((out, OPERATORS[operator](*values)))

    while op_queue:
        set_value(*op_queue.pop())

    return int(''.join(map(str, (value for key, value in reversed(sorted(calculated_values.items())) if key.startswith('z')))), 2)


def part2(input_: Iterable[str]) -> str:
    _,operations = parse_input(input_)
    operations_map = {out: (operator, frozenset({v1, v2})) for v1, operator, v2, out in operations}
    inv_map = {operation: out for out, operation in operations_map.items()}
    bad_wires = []

    def rpad(n):
        return f'0{n}'[-2:]

    @lru_cache
    def generate_carry(n: int):
        if n == 0:
            return ('AND', frozenset((f'x{rpad(n)}', f'y{rpad(n)}')))
        return ('OR', frozenset((
            ('AND', frozenset((f'x{rpad(n)}', f'y{rpad(n)}'))),
            ('AND', frozenset((
                ('XOR', frozenset((f'x{rpad(n)}', f'y{rpad(n)}'))),
                generate_carry(n - 1)
            )))
        )))

    def generate_term(n: int):
        if n == 0:
            return ('XOR', frozenset((f'x{rpad(n)}', f'y{rpad(n)}')))

        return ('XOR', frozenset((('XOR', frozenset((f'x{rpad(n)}', f'y{rpad(n)}'))), generate_carry(n - 1))))

    def swap_wires(name1, name2):
        bad_wires.extend((name1, name2))
        expr1 = operations_map[name1]
        expr2 = operations_map[name2]
        operations_map[name1], operations_map[name2] = expr2, expr1
        inv_map[expr1], inv_map[expr2] = inv_map[expr2], inv_map[expr1]

    def traverse(expr, expected):
        if isinstance(expr, str):
            return expr
        operator, operands = expr
        if expr in inv_map:
            ret = inv_map[expr]
        else:
            expected_operator, children = operations_map.get(expected, (None, set()))
            if expected_operator == operator:
                children = set(children)
            else:
                children = set()
            if not children:
                op1_name, op2_name = (traverse(operand, None) for operand in operands)
            else:
                operand1, operand2 = operands
                op1_name = traverse(operand1, None)
                if op1_name in children:
                    children.remove(op1_name)
                    op2_name = traverse(operand2, next(iter(children)))
                else:
                    op2_name = traverse(operand2, None)
                    children.remove(op2_name)
                    op1_name = traverse(operand1, next(iter(children)))

            mapped = operator, frozenset((op1_name, op2_name))
            ret = inv_map.get(mapped)

        if expected is not None and ret != expected:
            swap_wires(expected, ret)
            ret = expected

        return ret

    for i in range(45):
        term = generate_term(i)
        traverse(term, f'z{rpad(i)}')

    return ','.join(sorted(bad_wires))


if __name__ == '__main__':
    with open('../../data/d24.txt', 'r') as fi:
        input_ = tuple(fi)
    print(part1(input_))
    print(part2(input_))
