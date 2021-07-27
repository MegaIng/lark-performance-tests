from contextlib import contextmanager
from dataclasses import dataclass
from time import time

import scipy.optimize
from labellines import labelLines

import lark
from csv_utils import write_csv
from lark import Lark
import numpy as np
import matplotlib.pyplot as plt

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


def get_state_count(parser: Lark) -> int:
    return len(parser.parser.parser._parse_table.states)


def main():
    # for thresholds in [10, 20, 30, 40, 50, 60, 70, 80]:
    #     print(f"{thresholds=}")
    #     lark.load_grammar.REPEAT_BREAK_THRESHOLD = thresholds
    #     for n in [10, 20, 30, 40, 50, 60, 70, 80]:
    #         with timeit() as td:
    #             parser = Lark(f'start: "a"~{max(n-50,0)}..{n}', parser='lalr')
    #         print(n, td.delta)

    # data = []
    # for n in range(1000):
    #     with timeit() as td:
    #         parser = Lark(f'start: "a"~{max(n // 2, 0)}..{n}', parser='lalr')
    #     sc = get_state_count(parser)
    #     if n % 10 == 0:
    #         print(n, td.delta)
    #     data.append((n, sc, td.delta))
    # N, S, T = map(np.array, zip(*data))
    # write_csv("state_count.0.csv", list(zip(N, S)))
    # plt.plot(N, T)
    # plt.plot(N, S)
    # plt.show()

    def func(x, a, b):
        return a * np.log(x) + b

    datas = []
    X = np.linspace(1, 10000, 10000)
    for thresholds in range(3, 20):
        datas.append((thresholds, data := []))
        print(f"{thresholds=}")
        lark.utils.SMALL_FACTOR_THRESHOLD = thresholds
        for n in range(1, 1001*10, 50):
            with timeit() as td:
                parser = Lark(f'start: "a"~{0}..{n}', parser='lalr')
            data.append((n, td.delta, get_state_count(parser)))
            # print(n, td.delta, get_state_count(parser))
        N, TD, S = map(np.array, zip(*data))
        # plt.plot(N, TD, label=thresholds)
        popt, pcov = scipy.optimize.curve_fit(func, N, TD)
        # z = np.polyfit(N, TD, 1)

        # p = np.poly1d(z)
        plt.plot(X, func(X, *popt), label=thresholds)
    plt.legend()
    labelLines(plt.gca().get_lines(), zorder=2.5)
    plt.show()


if __name__ == '__main__':
    main()
