import csv
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cache
from operator import getitem, itemgetter
from pprint import pprint
from time import time
from typing import Iterable
from progressbar import ProgressBar

import matplotlib.pyplot as plt

from csv_utils import write_csv
from lark import Lark
import numpy
import matplotlib.pyplot as plt

from lark.utils import small_factors


@dataclass
class TimeData:
    start: float = None
    end: float = None

    @property
    def delta(self):
        return self.end - self.start


@contextmanager
def timeit():
    td = TimeData()
    td.start = time()
    yield td
    td.end = time()


def generate_rules(atom, factors) -> tuple[str, list[str]]:
    rules = []
    base = atom
    name = None
    for i, (a, b) in enumerate(factors):
        name = f"_a{a}_b{b}_i{i}"
        r = f"{name}: {' '.join([base] * a)} {' '.join([atom] * b)}"
        rules.append(r)
        base = name
    return name, rules


def generate_rule_opt(name, a, b, target, target_opt, atom) -> str:
    expansion = []
    for i in range(a):
        expansion.append(f"{' '.join([target] * i)} {target_opt}")
    for i in range(b):
        expansion.append(f"{' '.join([target] * a)} {' '.join([atom] * i)}")
    return '\n'.join(
        f"{' ' * len(name)}| {e}" if i != 0 else f"{name}: {e}"
        for i, e in enumerate(expansion)
    )


def generate_rules_opt(atom, factors) -> tuple[str, list[str]]:
    rules = []
    target = atom
    target_opt = ''
    name_opt = None
    for i, (a, b) in enumerate(factors):
        name = f"_a{a}_b{b}_i{i}"
        r = f"{name}: {' '.join([target] * a)} {' '.join([atom] * b)}"
        rules.append(r)
        name_opt = f"_a{a}_b{b}_i{i}_opt"
        r_opt = generate_rule_opt(name_opt, a, b, target, target_opt, atom)
        rules.append(r_opt)
        target = name
        target_opt = name_opt
    return name_opt, rules


def get_state_count(parser: Lark) -> int:
    return len(parser.parser.parser._parse_table.states)


# MAX_FACTOR = 50


@cache
def all_options(n: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if n < 2:
        return (((n, 0),),)
    out = []
    for a in range(2, n + 1):
        b = n % a
        r = n // a
        if r == 1:
            out.append(((a, b),))
        else:
            out.extend((
                (*children, (a, b))
                for children in all_options(r)
            ))
    return tuple(out)


def bucketize(n, i):
    buckets = [n // i] * i
    assert sum(buckets) <= n
    for j in range(n % i):
        buckets[j] += 1
    return [(buckets[0], 0),
            *((1, buckets[j]) for j in range(1, i))]


def main():
    for N in range(100, 1001, 100):
        data = []

        # N = 300

        # o = all_options(N)
        # print(len(o))
        # Throw away the case where we have (a, b) instead of (a+b, 0) as the base case.
        # o = tuple(f for f in o if f[0][1] == 0)
        o = [bucketize(N, i) for i in range(int(N**0.5)//2, N)]
        print(len(o))
        progress = ProgressBar()
        for factors in progress(o):
            # name, rules = generate_rules_opt('"a"', factors)
            name, rules = generate_rules('"a"', factors)
            rules = '\n'.join(rules)
            grammar = fr"""
    start: {name}
    {rules}
    """
            # print(grammar)
            with timeit() as creation:
                parser = Lark(grammar, parser='lalr')
            with timeit() as parsing:
                # for i in range(1, N):
                #     parser.parse("a" * i)
                parser.parse("a" * N)
            states = get_state_count(parser)
            data.append((len(data), len(factors), max(map(sum, factors)), sum(map(sum, factors)) / len(factors),
                         str(factors), sum(map(sum, factors)), states, creation.delta, parsing.delta))

        data.sort(key=itemgetter(-3))
        write_csv(f"data.{N}.csv", data,
                  ["i", "rule_count", "max_size", "avg_size", "factors", "factor_sum", "states", "creation_time",
                   "parsing_time"])
        I, RC, MS, AS, L, F, S, C, P = zip(*data)
        # plt.plot(F, S, label="states")
        plt.plot(F, C, label="creation")
        plt.plot(F, P, label="parsing")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    main()
