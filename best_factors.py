from functools import cache
from pprint import pprint


@cache
def all_options(n: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if n < 2:
        return (((n, 0),),)
    out = []
    for a in range(2, n + 1):
        b = n % a
        r = n // a
        if r == 1:
            if b != 0:
                continue
            out.append(((a, b),))
        else:
            out.extend((
                (*children, (a, b))
                for children in all_options(r)
            ))
    return tuple(out)


SMALL_FACTOR_THRESHOLD = 5


def small_factors(n):
    """
    Splits n up into smaller factors and summands <= SMALL_FACTOR_THRESHOLD.
    Returns a list of [(a, b), ...]
    so that the following code returns n:

    n = 1
    for a, b in values:
        n = n * a + b

    Currently, we also keep a + b <= SMALL_FACTOR_THRESHOLD, but that might change
    """
    assert n >= 0
    if n < SMALL_FACTOR_THRESHOLD:
        return [(n, 0)]
    # TODO: Think of better algorithms (Prime factors should minimize the number of steps)
    for a in range(SMALL_FACTOR_THRESHOLD, 1, -1):
        b = n % a
        if a + b > SMALL_FACTOR_THRESHOLD:
            continue
        r = n // a
        assert r * a + b == n  # Sanity check
        if r <= SMALL_FACTOR_THRESHOLD:
            return [(r, 0), (a, b)]
        else:
            return small_factors(r) + [(a, b)]
    assert False, "Failed to factorize %s" % n


def main():
    for n in range(8191,8191+1):
        options = all_options(n)
        options = [(sum(map(sum, o)), len(o), o) for o in options if o[0][1] == 0]
        options.sort()
        best = [t for t in options if t[:2] == options[0][:2]]
        f = small_factors(n)
        f = (sum(map(sum, f)), len(f), f)
        # if best[0][:2] != f[:2]:
        print(n)
        pprint(best)
        print(f)
        print(n.bit_length(), bin(n).count("1"))
        if all(any(a > 5 and b != 0 for a, b in o[2]) for o in best):
            print(n)
            pprint(best)
            print(f)
            print(n.bit_length(), bin(n).count("1"))


if __name__ == '__main__':
    main()
