import importlib
from argparse import ArgumentParser
from itertools import islice
from timeit import timeit
from typing import Tuple
from tabulate import tabulate


def run_day(day: int, times: int) -> Tuple[str, float, float, float]:
    print(f'Running day {day} {times} times')
    key = f'd{str(day).zfill(2)}'
    with open(f'data/{key}.txt', 'r') as fi:
        input_ = tuple(fi)
    module = importlib.import_module(f'adventofcode2024.{key}', key)
    solution1_time = timeit(lambda: module.part1(input_), number=times) / times
    solution2_time = timeit(lambda: module.part2(input_), number=times) / times
    return key, solution1_time, solution2_time, solution1_time + solution2_time


if __name__ == '__main__':
    arg_parser = ArgumentParser('Run all')
    arg_parser.add_argument('-n', required=False, type=int, default=3)
    arg_parser.add_argument('-o', required=False, type=str, default='./solution_times.txt')
    args = arg_parser.parse_args()
    days = []
    for d in range(1, 26):
        try:
            days.append(run_day(d, args.n))
        except (ImportError, FileNotFoundError):
            print(f'Day {d} missing')
    totals = ('total', *(sum(col) for col in islice(zip(*days), 1, None)))
    days.append(totals)
    with open(args.o, 'w') as fi:
        fi.write(tabulate(days, headers=['day', 'part1 time (s)', 'part2 time (s)', 'total time (s)']))
